"""
Módulo de funções de fitness modular.

Estrutura permite:
- Pesos dinâmicos
- Abordagem multiobjetivo
- Comparação clara de impacto de cada restrição
"""

from hospital_routes.optimization.fitness.composite_fitness import CompositeFitness
from hospital_routes.optimization.fitness.distance_fitness import DistanceFitness
from hospital_routes.optimization.fitness.capacity_penalty import CapacityPenalty
from hospital_routes.optimization.fitness.autonomy_penalty import AutonomyPenalty
from hospital_routes.optimization.fitness.priority_penalty import PriorityPenalty
from hospital_routes.optimization.fitness.load_balance_penalty import LoadBalancePenalty

__all__ = [
    "CompositeFitness",
    "DistanceFitness",
    "CapacityPenalty",
    "AutonomyPenalty",
    "PriorityPenalty",
    "LoadBalancePenalty",
]

