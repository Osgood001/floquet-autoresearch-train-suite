#!/usr/bin/env python3
"""
Numerically compute a_d_c1 and a_d_c2 for the Floquet delta scatterer.

The infinite tridiagonal matrix equation:
  sqrt(eps + n) * psi_n + i*sqrt(a_d)*(psi_{n-1} + psi_{n+1}) = 0

The determinant zero condition is given by the continued fraction:
  S(eps) = sqrt(eps) - a_d/(sqrt(eps+1) - a_d/(sqrt(eps+2) - a_d/(...)))
         - a_d/(sqrt(eps-1) - a_d/(sqrt(eps-2) - a_d/(...))) = 0

We truncate and solve numerically.
"""
import numpy as np
from scipy import linalg

def build_matrix(eps, a_d, N=100):
    """Build the truncated tridiagonal matrix."""
    size = 2 * N + 1
    diag = np.zeros(size, dtype=complex)
    off = np.ones(size - 1, dtype=complex) * 1j * np.sqrt(a_d)
    for i in range(size):
        n = i - N
        diag[i] = np.sqrt(eps + n)
    return np.diag(diag) + np.diag(off, 1) + np.diag(off, -1)

def det_zero_continued_fraction(eps, a_d, nmax=500):
    """
    Compute the function f(eps) = continued fraction value.
    The zeros of f(eps) correspond to transmission zeros / poles.
    
    f(eps) = sqrt(eps) - a_d/(sqrt(eps+1) - a_d/(sqrt(eps+2) - ...))
                    - a_d/(sqrt(eps-1) - a_d/(sqrt(eps-2) - ...))
    """
    # Upward CF: sqrt(eps+1) - a_d/(sqrt(eps+2) - a_d/(...))
    cf_up = np.sqrt(eps + nmax)
    for n in range(nmax - 1, 0, -1):
        cf_up = np.sqrt(eps + n) - a_d / cf_up
    
    # Downward CF: sqrt(eps-1) - a_d/(sqrt(eps-2) - a_d/(...))
    cf_down = np.sqrt(eps - nmax)
    for n in range(nmax - 1, 0, -1):
        cf_down = np.sqrt(eps - n) - a_d / cf_down
    
    return np.sqrt(eps) - a_d / cf_up - a_d / cf_down

def find_zero_tracking(a_d, guess=0.5, nmax=200):
    """Track the zero by following from small a_d."""
    from scipy.optimize import root_scalar
    
    def f_real(eps_R):
        """Real part of continued fraction just above the real axis."""
        eps = eps_R + 1e-8j
        return det_zero_continued_fraction(eps, a_d, nmax).real
    
    try:
        sol = root_scalar(f_real, bracket=(0.01, 0.99), method='bisect')
        if sol.converged:
            return sol.root
    except (ValueError, RuntimeError):
        pass
    return None

def main():
    print("=== Floquet Delta Scatterer Critical Values ===\n")
    
    # Track the transmission zero as a_d increases
    print("Tracking transmission zero in D₀ (0 < ε_R < 1):")
    print(f"{'a_d':>8s}  {'ε_R':>10s}")
    print("-" * 22)
    
    eps_vals = []
    for a_d in np.linspace(0.02, 0.35, 100):
        # Scan for the zero
        # For each a_d, find ε_R where the continued fraction has a zero
        from scipy.optimize import root_scalar
        
        def f_wrapper(eps_R):
            eps = eps_R + 1e-8j
            return det_zero_continued_fraction(eps, a_d, 300).real
        
        try:
            # The zero should be in (0, 1) for small a_d
            sol = root_scalar(f_wrapper, bracket=(0.05, 0.95), method='bisect')
            if sol.converged:
                eps_vals.append((a_d, sol.root))
                if len(eps_vals) <= 10 or len(eps_vals) % 10 == 0:
                    print(f"{a_d:8.4f}  {sol.root:10.6f}")
        except (ValueError, RuntimeError):
            pass
    
    if eps_vals:
        print(f"\nFound {len(eps_vals)} values. Last: a_d={eps_vals[-1][0]:.6f}, ε_R={eps_vals[-1][1]:.6f}")
    
    # Find a_d_c1 by interpolation
    a_ds = np.array([v[0] for v in eps_vals])
    eps_Rs = np.array([v[1] for v in eps_vals])
    
    # The zero approaches ε_R = 1. Find where it would cross 1.
    # Use extrapolation
    if len(eps_vals) >= 3:
        coeffs = np.polyfit(eps_Rs[-5:], a_ds[-5:], 2)
        a_d_c1 = np.polyval(coeffs, 1.0)
        print(f"\na_d_c1 ≈ {a_d_c1:.6f} (quadratic extrapolation to ε_R=1)")
        
        # Also try linear fit on last few points
        coeffs_lin = np.polyfit(eps_Rs[-3:], a_ds[-3:], 1)
        a_d_c1_lin = np.polyval(coeffs_lin, 1.0)
        print(f"a_d_c1 ≈ {a_d_c1_lin:.6f} (linear extrapolation to ε_R=1)")
    
    print("\nDone.")

if __name__ == "__main__":
    main()
