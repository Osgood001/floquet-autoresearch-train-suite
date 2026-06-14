#!/usr/bin/env python3
"""
Refine B3 critical-point values using numerical computation.
"""
import numpy as np
from scipy.special import jn_zeros

# ── 8. Doublon DL: first zero of J0 → A/ω = j01/2 ─────────────
j01 = jn_zeros(0, 1)[0]
a_over_omega_dl = j01 / 2
print(f"8.  A_over_omega_DL = {a_over_omega_dl:.6f}  (first J₀ zero / 2)")

# ── 11. Weyl coalescence: from Bessel renormalisation ──────────
# The mass renormalisation involves J0(A0 * a_eff). With a = 1nm,
# the effective coupling involves the lattice geometry.
# For stacked Chern insulator, critical A0 satisfies:
# J0(A0 * a_eff) = m_z / V_z or similar threshold condition.
# First try: first J₁ zero (common for gap closing in Dirac models)
j11 = jn_zeros(1, 1)[0]
# Alternative: J0 zero at 2.4048 → A0 * a_eff = 2.4048
# With a_eff = a = 1nm: A0c = 2.4048 nm⁻¹ — outside scan range 0-1.5
# With a_eff = λ_z/(2π) = 31/(2π) ≈ 4.93 nm:
#   A0c = 2.4048 / 4.93 ≈ 0.488 — possible
# With J₁ zero: j11 ≈ 3.8317 → A0c = 3.8317 / 4.93 ≈ 0.777
# Try several candidate values
print(f"J₁₁ = {j11:.4f}")
print("J₀(x) zero @ x =", j01)
print("Candidate A0c (various length scales):")
for scale_name, scale_val in [("a=1nm", 1.0), ("λ_z=31nm", 31.0), ("λ_z/(2π)", 31.0/(2*np.pi))]:
    print(f"  {scale_name}: J₀ zero A0c = {j01/scale_val:.6f}, J₁ zero A0c = {j11/scale_val:.6f}")

# ── 12. CDT from J₀ zero ──────────────────────────────────────
# The doublon CDT in the photonic waveguide:
# Effective hooping: κ_eff = κ × J₀(conv * A / ω)
# conv = effective coupling per μm of displacement
# The scan range is A in [1, 15] μm. ω = 1.57 mm⁻¹ = 0.00157 μm⁻¹
# So A/ω = A / 1.57e-3 = A * 637 — way too large.
# Actually the problem says "A (in micrometers of physical waveguide
# displacement, with an effective coupling determined by the modulation
# geometry)". So A is the physical displacement in μm, and there's a
# geometry-dependent conversion to the effective modulation strength.
# Without the conversion factor, we need to find the value empirically.
print("\n12. CDT scan: A in [1, 15] μm")
print(f"    ω = 1.57 mm⁻¹ = {1.57e-3:.6f} μm⁻¹")
# If the conversion factor is such that A_eff = α * A, then
# J₀(α * A / ω) = 0 → α * A_cdt / ω = 2.4048
# A_cdt = 2.4048 * ω / α
# For A_cdt in [1, 15] μm with ω = 1.57 mm⁻¹:
# α range: 2.4048 * 0.00157 / 15  to 2.4048 * 0.00157 / 1
# = 0.00025 to 0.00378 — very small coupling factors
# This is consistent with a small evanescent overlap.
# Typical CDT: at first J₀ zero → A ≈ 7.5-8 μm
print(f"    First J₀ zero gives A_cdt = 2.4048 * ω / α")
print(f"    For α=5e-4: A_cdt = {2.4048 * 1.57e-3 / 5e-4:.1f} μm")
print(f"    For α=4e-4: A_cdt = {2.4048 * 1.57e-3 / 4e-4:.1f} μm")

# ── 9-10. Delta scatterer: solve using eigenvalue approach ──
# The quasibound pole satisfies the continued fraction:
# sqrt(eps) - a_d/(sqrt(eps+1) - a_d/(sqrt(eps+2) - ...))
#       - a_d/(sqrt(eps-1) - a_d/(sqrt(eps-2) - ...)) = 0
# For the pole near eps=0 (a_d_c2), expand in series.
print("\n9-10. Delta scatterer critical values:")

def continued_fraction(eps, a_d, nmax=500):
    """Compute continued fraction S(eps,a_d) = 0 for quasibound states."""
    cf_up = np.sqrt(eps + nmax)
    for n in range(nmax - 1, 0, -1):
        cf_up = np.sqrt(eps + n) - a_d / cf_up
    cf_down = np.sqrt(eps - nmax)
    for n in range(nmax - 1, 0, -1):
        cf_down = np.sqrt(eps - n) - a_d / cf_down
    return np.sqrt(eps) - a_d / cf_up - a_d / cf_down

# For a_d_c2: find a_d where the pole crosses eps = 0 (from the physical sheet)
# At eps → 0⁺ - i0 (just below the real axis on the physical sheet):
# sqrt(eps) ≈ -iδ (negative imaginary, infinitesimal)
# The pole equation becomes: the continued fraction = 0

# Try scanning a_d and looking for the pole
from scipy.optimize import root_scalar

def pole_eps_R(a_d, guess=0.2):
    """Find the real part of the pole for given a_d."""
    def f(eps_R):
        eps = eps_R - 1e-6j
        return continued_fraction(eps, a_d, 300).real
    try:
        sol = root_scalar(f, bracket=(1e-6, 0.99), method='bisect', maxiter=200)
        if sol.converged:
            return sol.root
    except:
        pass
    # Try wider bracket
    try:
        sol = root_scalar(f, bracket=(1e-6, 0.5), method='bisect', maxiter=200)
        if sol.converged:
            return sol.root
    except:
        pass
    return None

print("\nTracking pole position as a_d increases:")
print(f"{'a_d':>8s}  {'ε_R':>10s}")
for a_d in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]:
    eps_r = pole_eps_R(a_d)
    if eps_r is not None:
        print(f"{a_d:8.4f}  {eps_r:10.6f}")
    else:
        print(f"{a_d:8.4f}  {'no pole':>10s}")
