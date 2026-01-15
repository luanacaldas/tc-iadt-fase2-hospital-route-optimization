"""
Função de fitness composta (multiobjetivo).

Combina todos os componentes de fitness em uma única função.
"""

from typing import List
from hospital_routes.core.interfaces import (
    Delivery,
    RouteSolution,
    VehicleConstraints,
)
from hospital_routes.optimization.fitness.distance_fitness import DistanceFitness
from hospital_routes.optimization.fitness.capacity_penalty import CapacityPenalty
from hospital_routes.optimization.fitness.autonomy_penalty import AutonomyPenalty
from hospital_routes.optimization.fitness.priority_penalty import PriorityPenalty
from hospital_routes.optimization.fitness.load_balance_penalty import LoadBalancePenalty
from hospital_routes.utils.config import FitnessWeights


class CompositeFitness:
    """
    Função de fitness composta que combina múltiplos objetivos.
    
    Fórmula:
    fitness = α * total_distance
           + β * capacity_violation
           + γ * autonomy_violation
           + δ * priority_delay
           + ε * vehicle_count
    
    Onde os pesos (α, β, γ, δ, ε) são configuráveis.
    """
    
    def __init__(self, weights: FitnessWeights):
        """
        Args:
            weights: Pesos para cada componente da função de fitness
        """
        self.weights = weights
        
        # Inicializar componentes
        self.distance_fitness = DistanceFitness(weights.distance_weight)
        self.capacity_penalty = CapacityPenalty(weights.capacity_penalty)
        self.autonomy_penalty = AutonomyPenalty(weights.autonomy_penalty)
        self.priority_penalty = PriorityPenalty(weights.priority_penalty)
        self.load_balance_penalty = LoadBalancePenalty(
            getattr(weights, 'load_balance_penalty', 0.5)
        )
    
    def calculate(
        self,
        solution: RouteSolution,
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
        depot_location: tuple[float, float],
        distance_matrix: dict[tuple[str, str], float],
    ) -> float:
        """
        Calcula o fitness total da solução.
        
        Args:
            solution: Solução de rota
            deliveries: Lista de entregas
            vehicles: Lista de veículos com restrições
            depot_location: Localização do depósito
            distance_matrix: Matriz de distâncias entre pontos
        
        Returns:
            float: Fitness total (quanto menor, melhor)
        """
        # Componente de distância
        distance_component = self.distance_fitness.calculate(
            solution, deliveries, depot_location
        )
        
        # Penalidade de capacidade
        capacity_component = self.capacity_penalty.calculate(
            solution, deliveries, vehicles
        )
        
        # Penalidade de autonomia
        autonomy_component = self.autonomy_penalty.calculate(
            solution, deliveries, vehicles, depot_location, distance_matrix
        )
        
        # Penalidade de prioridade
        priority_component = self.priority_penalty.calculate(
            solution, deliveries
        )
        
        # Penalidade por desbalanceamento de carga
        load_balance_component = self.load_balance_penalty.calculate(
            solution, deliveries, vehicles
        )
        
        # Penalidade por número de veículos (ε * vehicle_count)
        vehicle_component = self.weights.vehicle_penalty * len(solution.routes)
        
        # Fitness total (soma de todos os componentes)
        total_fitness = (
            distance_component
            + capacity_component
            + autonomy_component
            + priority_component
            + load_balance_component
            + vehicle_component
        )
        
        return total_fitness
    
    def get_components_breakdown(
        self,
        solution: RouteSolution,
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
        depot_location: tuple[float, float],
        distance_matrix: dict[tuple[str, str], float],
    ) -> dict[str, float]:
        """
        Retorna breakdown detalhado de cada componente do fitness.
        
        Útil para análise e debugging.
        
        Returns:
            dict: Dicionário com cada componente e seu valor
        """
        return {
            "distance": self.distance_fitness.calculate(
                solution, deliveries, depot_location
            ),
            "capacity_penalty": self.capacity_penalty.calculate(
                solution, deliveries, vehicles
            ),
            "autonomy_penalty": self.autonomy_penalty.calculate(
                solution, deliveries, vehicles, depot_location, distance_matrix
            ),
            "priority_penalty": self.priority_penalty.calculate(
                solution, deliveries
            ),
            "load_balance_penalty": self.load_balance_penalty.calculate(
                solution, deliveries, vehicles
            ),
            "vehicle_penalty": self.weights.vehicle_penalty * len(solution.routes),
        }

