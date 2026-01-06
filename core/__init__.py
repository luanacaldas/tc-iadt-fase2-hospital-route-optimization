"""Core module with interfaces and base models."""

from hospital_routes.core.interfaces import (
    BaseOptimizer,
    BaseReporter,
    ReportType,
)
from hospital_routes.core.models import (
    RouteSolution,
    OptimizationResult,
    ReportRequest,
)

__all__ = [
    "BaseOptimizer",
    "BaseReporter",
    "ReportType",
    "RouteSolution",
    "OptimizationResult",
    "ReportRequest",
]

