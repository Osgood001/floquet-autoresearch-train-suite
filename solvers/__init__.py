"""
Floquet problem-solving monorepo solver package.

Usage:
    from solvers.b1_solvers import SOLVERS_B1
    from solvers.b3_solvers import SOLVERS_B3

    predictions = {}
    for rid, solver in {**SOLVERS_B1, **SOLVERS_B3}.items():
        predictions[rid] = solver()
"""

from .floquet import (
    bessel_renormalised_hopping,
    bessel_zeros,
    floquet_effective,
    dressed_effective,
    chern_number,
    winding_number_1d,
    delta_scatterer_cf,
)
from .b1_solvers import SOLVERS_B1
from .b3_solvers import SOLVERS_B3

__all__ = [
    "bessel_renormalised_hopping", "bessel_zeros",
    "floquet_effective", "dressed_effective",
    "chern_number", "winding_number_1d",
    "delta_scatterer_cf",
    "SOLVERS_B1", "SOLVERS_B3",
]
