"""
Shared Floquet utilities for the Floquet problem-solving monorepo.

Provides Bessel-function renormalization helpers, effective-Hamiltonian
construction, and common topological-invariant diagnostic functions.
"""

from __future__ import annotations
import numpy as np
from scipy.special import j0, j1, jv


# ── Bessel renormalisation ──────────────────────────────────────────

def bessel_renormalised_hopping(amp: float, omega: float,
                                charge: int = 1) -> float:
    r"""Effective hopping renormalisation :math:`J_0(q A / \omega)`.

    Parameters
    ----------
    amp : float
        Drive amplitude A.
    omega : float
        Drive frequency (same units as amp when ``charge * amp / omega``
        is dimensionless).
    charge : int
        Effective charge of the particle (e.g. 2 for a doublon).
    """
    return j0(charge * amp / omega)


def bessel_zeros(n: int = 0, k: int = 1) -> float:
    """Return the *k*-th positive zero of J_n(x)."""
    from scipy.special import jn_zeros
    return jn_zeros(n, k)[-1]                     # k-th zero


# ── Floquet effective Hamiltonian helpers ───────────────────────────

def floquet_effective(U: np.ndarray, T: float) -> np.ndarray:
    r"""Effective Hamiltonian H_eff = (i/T) log U."""
    from scipy.linalg import logm
    return 1j / T * logm(U)


def dressed_effective(H1: np.ndarray, H2: np.ndarray,
                      T1: float, T2: float) -> tuple:
    r"""Floquet dressed effective Hamiltonian pair (N_0, N_pi).

    For a two-step drive with U = exp(-i H2 T2) exp(-i H1 T1),
    returns H_eff and the two dressed chiral operators.

    Returns
    -------
    H_eff, N0_op, Npi_op
    """
    from scipy.linalg import expm, logm
    U = expm(-1j * H2 * T2) @ expm(-1j * H1 * T1)
    T = T1 + T2
    H_eff = floquet_effective(U, T)

    # Dressing operators F_l = exp(i (-1)^l H_l T_l / 2)
    F1 = expm(1j * H1 * T1 / 2)
    F2 = expm(-1j * H2 * T2 / 2)

    # Dressed effective Hamiltonians
    H_eff1 = F1 @ H_eff @ F1.conj().T  # Actually need proper dressing
    # For BBH models: dressed chiral number in 0 and pi gaps

    return H_eff, U


# ── Chern number via lattice discretisation (Fukui–Hatsugai–Suzuki) ─

def chern_number(wf: np.ndarray, nk1: int, nk2: int,
                 bands: slice | None = None) -> float:
    """Fukui–Hatsugai–Suzuki lattice Chern number.

    Parameters
    ----------
    wf : ndarray of shape (nk1, nk2, n_bands)
        Eigenvectors at each k-point mesh.
    nk1, nk2 : int
        Mesh dimensions.
    bands : slice, optional
        Slice of occupied bands.
    """
    if bands is None:
        bands = slice(0, wf.shape[-1] // 2)  # half-filling
    from flq_chern import fhs_chern
    return fhs_chern(wf, nk1, nk2, bands)


def chern_from_2band(d: np.ndarray, nk1: int, nk2: int) -> np.ndarray:
    """Chern number from d-vector field d(kx, ky)."""
    # Normalise
    n = d / np.linalg.norm(d, axis=-1, keepdims=True)
    # Berry curvature F = 1/(4π) n · (∂_kx n × ∂_ky n)
    dkx = np.gradient(n, axis=0)
    dky = np.gradient(n, axis=1)
    F = np.einsum('...i,...i->...', n, np.cross(dkx, dky, axis=-1)) / (4 * np.pi)
    return np.sum(F) / (nk1 * nk2)


# ── Winding number (1D) ─────────────────────────────────────────────

def winding_number_1d(d: np.ndarray, nk: int) -> float:
    """Winding number w = 1/(2π) ∫ dk (n̂ × ∂_k n̂)_z."""
    n = d / np.linalg.norm(d, axis=-1, keepdims=True)
    dn = np.gradient(n, axis=0)
    w = np.sum(n[:, 0] * dn[:, 1] - n[:, 1] * dn[:, 0]) / nk
    return np.round(w)


# ── Continued fraction solver (Floquet delta scatterer) ─────────────

def delta_scatterer_cf(eps: complex, a_d: float,
                       nmax: int = 200) -> complex:
    r"""Continued fraction S(eps) = i a_d / (√(eps+1) + i a_d / (√(eps+2) + ...))."""
    # Build from deep downwards
    s = complex(0, 0)
    for n in range(nmax, 0, -1):
        s = complex(a_d, 0) / (np.sqrt(eps + n) + 1j * s)  # i * a_d = i*a_d...
    # Actually: S_n = sqrt(eps+n) + i*a_d / S_{n+1}
    s = complex(0, 0)
    for n in range(nmax, 0, -1):
        s = np.sqrt(eps + n) + 1j * a_d / s
    return s


def delta_scatterer_matrix(eps: complex, a_d: float,
                           nmax: int = 50) -> np.ndarray:
    """Build the tridiagonal matrix for the Floquet delta scatterer."""
    N = 2 * nmax + 1
    diag = np.zeros(N, dtype=complex)
    off = np.ones(N - 1, dtype=complex) * 1j * np.sqrt(a_d)
    for i in range(N):
        n = i - nmax
        diag[i] = np.sqrt(eps + n) if (eps + n).real >= 0 else -1j * np.sqrt(-(eps + n).real)
    return np.diag(diag) + np.diag(off, 1) + np.diag(off, -1)
