#!/usr/bin/env python3
"""
Properly compute a_d_c2 for the Floquet delta scatterer using
the correct tridiagonal matrix recurrence:

√(ε+n) ψ_n + i√(a_d)(ψ_{n-1} + ψ_{n+1}) = 0

→  ψ_{n+1} = i√(ε+n)/√(a_d) ψ_n - ψ_{n-1}

The quasibound state (pole) condition at n=0:
√(ε) + i√(a_d)(ψ_{-1}/ψ_0 + ψ₁/ψ₀) = 0

With r_n ≡ ψ_{n+1}/ψ_n and the CF:
  r_{n-1} = 1/(i√(ε+n)/√(a_d) - r_n)
"""
import numpy as np
from scipy.optimize import root_scalar

def r0_cf(eps, a_d, nmax=1000):
    """Compute r₀ = ψ₁/ψ₀ using the upward continued fraction.

    Recurrence: r_n = i√(ε+n)/√(a_d) - 1/r_{n-1}
    For large n: r_n → 0 (decaying solution)
    CF from top: r_{n-1} = 1/(i√(ε+n)/√(a_d) - r_n)

    Starting from r_N = 0:
    r_{N-1} = 1/(i√(ε+N)/√(a_d))
    r_{N-2} = 1/(i√(ε+N-1)/√(a_d) - r_{N-1})
    ...
    """
    r = 0.0j
    for n in range(nmax, 0, -1):
        r = 1.0 / (1j * np.sqrt(eps + n) / np.sqrt(a_d) - r)
    return r

def rminus1_inv_cf(eps, a_d, nmax=1000):
    """Compute 1/r_{-1} = ψ_{-1}/ψ_0.

    For the downward direction (n ≤ 0), the same recurrence applies.
    ψ_0 appears at the matching point.
    For n → -∞, ψ_n → 0, so r_{-(N+1)} → 0.

    Using symmetry: for negative n, we can transform the problem.
    The CF from below gives: ψ_{-1}/ψ_0 via the reversed recurrence.
    """
    # For n = 0, -1, -2, ... going down
    # Recurrence: ψ_{n-1} = i√(ε+n)/√(a_d) ψ_n - ψ_{n+1}
    # Or equivalently from the bottom up:
    # Let s_n = ψ_{n-1}/ψ_n. Then s_n = i√(ε+n)/√(a_d) - 1/s_{n+1}
    s = 0.0j
    for n in range(-nmax, 0):
        s = 1.0 / (1j * np.sqrt(eps + n) / np.sqrt(a_d) - s)
    return s  # This is s_0 = ψ_{-1}/ψ_0

def pole_condition(eps, a_d, nmax=1000):
    """The matching condition at n=0 for a quasibound state."""
    r0 = r0_cf(eps, a_d, nmax)
    inv_rminus1 = rminus1_inv_cf(eps, a_d, nmax)
    return np.sqrt(eps) + 1j * np.sqrt(a_d) * (inv_rminus1 + r0)

def find_pole_real(eps_guess, a_d):
    """Find the real part of the pole for given a_d.
    The pole is at ε = ε_R - iε_I with ε_I > 0.
    We search for ε just below the real axis.
    """
    def f_real(eps_R):
        eps = eps_R - 1e-6j  # just below the real axis for the pole
        val = pole_condition(eps, a_d)
        return val.real

    def f_imag(eps_R):
        eps = eps_R - 1e-6j
        val = pole_condition(eps, a_d)
        return val.imag

    # The pole condition is a complex equation.
    # At the pole, both real and imag parts vanish.
    # Search for a zero of |val| or track using either component.
    try:
        sol = root_scalar(f_real, bracket=(1e-8, 0.99), method='bisect', maxiter=200)
        if sol.converged:
            return sol.root
    except:
        pass
    return None

def find_zero_real(eps_guess, a_d):
    """Find the real ε of the transmission zero."""
    # The transmission zero is on the real axis (just above).
    def f_real(eps_R):
        eps = eps_R + 1e-8j  # just above the real axis
        val = pole_condition(eps, a_d)
        return val.real
    try:
        sol = root_scalar(f_real, bracket=(1e-8, 0.99), method='bisect', maxiter=200)
        if sol.converged:
            return sol.root
    except:
        pass
    return None

print("=== Pole tracking (ε just below real axis) ===")
print(f"{'a_d':>8s}  {'ε_R':>10s}")
for a_d in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.65, 0.7, 0.72, 0.74, 0.76, 0.78]:
    eps_r = find_pole_real(0.5, a_d)
    if eps_r is not None:
        print(f"{a_d:8.4f}  {eps_r:10.6f}")
    else:
        print(f"{a_d:8.4f}  {'not found':>10s}")

print("\n=== Critical a_d_c2 scan (pole near ε_R = 0) ===")
for a_d in np.linspace(0.7, 0.82, 13):
    eps_r = find_pole_real(0.1, a_d)
    if eps_r is not None:
        print(f"{a_d:8.4f}  {eps_r:10.6f}  {'in D₀' if 0 < eps_r < 1 else 'OUTSIDE'}")
    else:
        print(f"{a_d:8.4f}  {'not found':>10s}  {'—'}")

print("\n=== Zero tracking (ε just above real axis) ===")
print(f"{'a_d':>8s}  {'ε_R':>10s}")
for a_d in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.72, 0.74, 0.76, 0.78, 0.8]:
    eps_r = find_zero_real("dummy", a_d)
    if eps_r is not None:
        print(f"{a_d:8.4f}  {eps_r:10.6f}")
    else:
        print(f"{a_d:8.4f}  {'not found':>10s}")
