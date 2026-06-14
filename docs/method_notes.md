# Method notes — Floquet problem-solving monorepo

## Architecture

```
predictions.json        ← master prediction file (consumed by score.py)
solvers/
├── __init__.py          package exports
├── floquet.py           shared helpers (Bessel, Chern, winding, CF)
├── b1_solvers.py        B1 track solvers (topological invariants)
└── b3_solvers.py        B3 track solvers (critical points)
docs/
└── method_notes.md      this file
```

## B1 — Topological invariants (integers)

### 1. Non-Bloch winding number (quantum walk)
- Split-step quantum walk topologies: winding(θ₁, θ₂) = ±1 or 0.
- With loss (a = e^γ), non-Bloch winding on the GBZ equals Hermitian winding
  when the gap remains open.
- At θ₁=1.6π, θ₂=0.58π, a=0.82: **w = 1.**

### 2. BBH Floquet SOTI (N_0, N_pi)
- Dressed effective Hamiltonian approach: H_eff,l = i/T ln[F_l U_T F_l†].
- Two-step drive: m₁ = -0.36γ₀, m₂ = 3.6γ₀, T₁=1.2/γ₀, T₂=0.6/γ₀.
- π-gap topological (N_pi = 1), 0-gap trivial (N_0 = 0).
- 4 corners × |N_pi| = **4 corner states in the π gap.**

### 3. Kicked SSH — synthetic Chern number
- Synthetic 2D BZ (k, θ) from kicked SSH with Y-kicking.
- Parameters: t=1, δ=0.5, h=1, T=3, α_y=0.8.
- Scanning (g, φ): **max |C| = 2** in strong-kicking regime.

### 4. Kagome magnon Chern number transition
- Undriven: (-1, 0, +1). Circular drive renormalises BC hopping via J₀.
- At first J₀ zero, gap between lower and middle bands closes and reopens
  → Chern numbers redistribute: **(0, -1, +1).**
- **Key insight**: Bessel-function sign change drives topological transition.

### 5. Hofstadter lowest-band Chern number
- Flux Φ = π/2 → 4-site magnetic unit cell.
- Lowest band: **ν₁ = +1** (standard TKNN result).

### 6. Kicked-rotor Dirac edge states
- N=3 quantum resonance → 3×3 effective Bloch Hamiltonian.
- Two Dirac cones at k=π (bands 2–3 touching), each with π Berry phase.
- Half-infinite geometry: **2 edge states** connecting the cones.

## B3 — Critical points (float tolerances)

### 7. 4D QHE Floquet mu_c
- Clean C=-1 phase: 2 < μ < 4. Disorder pushes the metal-insulator
  transition inward. At critical disorder: **μ_c ≈ 3.85.**

### 8. Doublon dynamic localisation
- Large-U Hubbard (U=10 >> Δ=1): doublon as tightly bound pair.
- Effective hopping ∼ J₀(2A/ω). First band collapse at first J₀ zero.
  **A/ω ≈ 2.4048/2 = 1.2024.**

### 9–10. Floquet delta scatterer (a_d_c1, a_d_c2)
- Infinite tridiagonal outgoing-wave matrix:
  diag √(ε+n), off-diag i√(a_d).
- **a_d_c1** ≈ 0.250: transmission zero collides with n=1 threshold.
- **a_d_c2** ≈ 0.800: quasibound pole exits D₀ at ε_R = 0.

### 11. Weyl node coalescence (A_0_c)
- Stacked Chern insulator + high-frequency drive.
- Floquet mass renormalisation → Weyl nodes approach and merge.
- **A_0_c ≈ 0.8270 nm⁻¹** for given parameters.

### 12. Photonic Hubbard CDT
- Waveguide simulator: doublon CDT via Bessel renormalisation.
- Scan 1–15 μm: **A_CDT ≈ 6.0 μm** at first miniband collapse.

## Reusable patterns

| Pattern | Where used |
|---|---|
| Bessel J₀ renormalisation of hopping | 4, 8, 12 |
| Continued fraction eigenvalue search | 9, 10 |
| Fukui–Hatsugai–Suzuki Chern number | 3, 4, 5 |
| Winding number via (n̂ × ∂_k n̂)_z integral | 1 |
| Dressed effective Hamiltonian | 2 |

## Failed / discarded ideas

*(Record method-level dead ends here.)*
