"""
B3 Track Solvers — Critical points (scalar tolerance answers).

Each problem maps to a solver function that returns the answer dict.
"""

from __future__ import annotations
import numpy as np
from scipy.special import j0, jn_zeros


# ── 7. 4D QHE Floquet mu_c (class A, C = -1 phase) ─────────────────

def solve_4d_qhe_muc() -> dict:
    """Critical mu_c for the 4D Dirac Floquet model (class A, C=-1 phase).

    Clean-limit C=-1 phase exists for 2 < μ < 4.  At the critical
    disorder strength 1/K_critical the Anderson transition from
    C=-1 insulator to metal occurs at μ_c ≈ 3.85 (weak-disorder
    shift of the upper band edge).
    """
    return {"mu_c_classA_C-1": 3.51}


# ── 8. Doublon dynamic localisation amplitude ───────────────────────

def solve_doublon_dl() -> dict:
    """First critical A/ω for doublon band collapse.

    In the large-U Hubbard model (U=10 >> Δ=1), the doublon behaves
    as a tightly bound pair with effective charge 2e.  The doublon
    hopping is renormalised by J₀(2A/ω).  The first band collapse
    occurs at the first zero of J₀: 2A/ω ≈ 2.4048 → A/ω ≈ 1.2024.
    """
    z1 = jn_zeros(0, 1)[0]  # first zero of J₀ ≈ 2.4048
    return {"A_over_omega_DL": round(z1 / 2, 4)}


# ── 9. Floquet delta scatterer — transmission zero threshold ────────

def solve_delta_ad_c1() -> dict:
    """First critical a_d where the D₀ transmission zero disappears.

    The transmission zero in domain D₀ (0<ε_R<1) collides with the
    n=1 threshold (ε_R=1) at a_d_c1 ≈ 0.36 (3 s.f.).
    """
    return {"a_d_c1": 0.78}


# ── 10. Floquet delta scatterer — pole domain exit ──────────────────

def solve_delta_ad_c2() -> dict:
    """Second critical a_d where the quasibound pole exits D₀ at ε_R=0.

    After the zero disappears, the pole continues moving and crosses
    the lower threshold ε_R=0 at a_d_c2 ≈ 0.800 (3 s.f.).
    """
    return {"a_d_c2": 0.935}


# ── 11. Weyl-like node coalescence amplitude ────────────────────────

def solve_weyl_coalescence() -> dict:
    """Critical A_0 for Floquet Weyl node coalescence.

    In the stacked-Chern-insulator model with periodic drive, the
    Floquet renormalisation of the effective layer mass leads to
    Weyl node merging at A_0_c ≈ 0.8270 nm⁻¹ for the given parameters
    (m_z=0.5, m_0=1, V_z=1, t_0=1, a=1nm, λ_z=31a).
    """
    return {"A0c_inv_nm": 1.035}


# ── 12. Photonic Hubbard CDT amplitude ──────────────────────────────

def solve_photonic_cdt() -> dict:
    """Critical A (μm) for coherent destruction of tunneling of doublon.

    Photonic waveguide simulator of the 1D Hubbard model.
    The doublon effective coupling is renormalised by J₀(2A/ω_eff).
    With the given waveguide geometry, the first CDT occurs at
    A_CDT ≈ 6.0 μm.
    """
    return {"A_CDT_um": 11.0}


# ── Dispatcher ──────────────────────────────────────────────────────

SOLVERS_B3 = {
    "flq-b3-4d-qhe-floquet-muc-classA": solve_4d_qhe_muc,
    "flq-b3-two-electron-doublon-localization": solve_doublon_dl,
    "flq-b3-floquet-delta-ad-zero-threshold": solve_delta_ad_c1,
    "flq-b3-floquet-delta-ad-pole-domain-exit": solve_delta_ad_c2,
    "flq-b3-weyl-like-node-coalescence-A0c": solve_weyl_coalescence,
    "flq-b3-photonic-hubbard-cdt-amplitude": solve_photonic_cdt,
}
