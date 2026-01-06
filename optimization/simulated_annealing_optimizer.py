"""
Implementação do algoritmo Simulated Annealing para otimização de rotas.

Simulated Annealing é uma meta-heurística que aceita soluções piores
com probabilidade decrescente (temperatura), permitindo escapar de mínimos locais.
"""

import time
import random
import math
from typing import List, Dict, Tuple

from hospital_routes.core.interfaces import (
    BaseOptimizer,
    Delivery,
    VehicleConstraints,
    OptimizationConfig,
    RouteSolution,
    OptimizationResult,
)
from hospital_routes.core.exceptions import OptimizationError
from hospital_routes.utils.distance import calculate_distance
from hospital_routes.utils.validators import validate_deliveries, validate_vehicles
from hospital_routes.optimization.fitness.composite_fitness import CompositeFitness
from hospital_routes.utils.config import FitnessWeights


class SimulatedAnnealingOptimizer(BaseOptimizer):
    """
    Otimizador de rotas usando Simulated Annealing.
    
    Estratégia: Aceita soluções piores com probabilidade decrescente,
    permitindo explorar o espaço de busca e escapar de mínimos locais.
    """
    
    def __init__(
        self,
        fitness_weights: FitnessWeights = None,
        initial_temperature: float = 1000.0,
        cooling_rate: float = 0.95,
        min_temperature: float = 0.1,
    ):
        """
        Args:
            fitness_weights: Pesos da função de fitness
            initial_temperature: Temperatura inicial
            cooling_rate: Taxa de resfriamento (0-1)
            min_temperature: Temperatura mínima (critério de parada)
        """
        self.fitness_weights = fitness_weights or FitnessWeights()
        self.composite_fitness = CompositeFitness(self.fitness_weights)
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.min_temperature = min_temperature
    
    def optimize(
        self,
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
        config: OptimizationConfig,
        depot_location: Tuple[float, float],
    ) -> OptimizationResult:
        """
        Otimiza rotas usando Simulated Annealing.
        
        Args:
            deliveries: Lista de entregas
            vehicles: Lista de veículos disponíveis
            config: Configuração (usa generations como iterações)
            depot_location: Localização do depósito
        
        Returns:
            OptimizationResult: Resultado da otimização
        """
        start_time = time.time()
        
        try:
            # Validar inputs
            validate_deliveries(deliveries)
            validate_vehicles(vehicles)
            
            # Construir matriz de distâncias
            distance_matrix = self._build_distance_matrix(
                deliveries, depot_location
            )
            
            # Solução inicial (Greedy)
            current_solution = self._initial_solution(
                deliveries, vehicles, depot_location, distance_matrix
            )
            current_fitness = self._calculate_fitness(
                current_solution, deliveries, vehicles, depot_location, distance_matrix
            )
            
            # Melhor solução encontrada
            best_solution = current_solution
            best_fitness = current_fitness
            best_fitness_history = [best_fitness]
            
            # Simulated Annealing
            temperature = self.initial_temperature
            iterations = config.generations if config.generations > 0 else 1000
            
            for iteration in range(iterations):
                # Gerar solução vizinha
                neighbor = self._generate_neighbor(current_solution, deliveries, vehicles)
                neighbor_fitness = self._calculate_fitness(
                    neighbor, deliveries, vehicles, depot_location, distance_matrix
                )
                
                # Calcular diferença de fitness
                delta = neighbor_fitness - current_fitness
                
                # Aceitar solução se for melhor ou com probabilidade baseada em temperatura
                if delta < 0 or random.random() < math.exp(-delta / temperature):
                    current_solution = neighbor
                    current_fitness = neighbor_fitness
                    
                    # Atualizar melhor solução
                    if current_fitness < best_fitness:
                        best_solution = current_solution
                        best_fitness = current_fitness
                        best_fitness_history.append(best_fitness)
                
                # Resfriar
                temperature *= self.cooling_rate
                
                # Parar se temperatura muito baixa
                if temperature < self.min_temperature:
                    break
            
            # Converter melhor solução para RouteSolution
            solution = self._routes_to_solution(
                best_solution, deliveries, vehicles, depot_location, distance_matrix
            )
            
            execution_time = time.time() - start_time
            
            return OptimizationResult(
                solution=solution,
                execution_time=execution_time,
                generations_evolved=iteration + 1,
                best_fitness_history=best_fitness_history,
                config=config,
                statistics={
                    "algorithm": "simulated_annealing",
                    "initial_temperature": self.initial_temperature,
                    "final_temperature": temperature,
                    "iterations": iteration + 1,
                },
            )
        
        except Exception as e:
            raise OptimizationError(
                f"Erro durante otimização Simulated Annealing: {str(e)}"
            ) from e
    
    def validate_solution(
        self,
        solution: RouteSolution,
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
    ) -> bool:
        """Valida se uma solução atende todas as restrições."""
        delivery_dict = {d.id: d for d in deliveries}
        
        # Verificar se todas as entregas estão nas rotas
        all_delivery_ids = set(d.id for d in deliveries)
        solution_delivery_ids = set()
        for route in solution.routes:
            solution_delivery_ids.update(route)
        
        if all_delivery_ids != solution_delivery_ids:
            return False
        
        # Verificar restrições de capacidade
        for route_idx, route in enumerate(solution.routes):
            if route_idx >= len(vehicles):
                return False
            
            vehicle = vehicles[route_idx]
            route_weight = sum(
                delivery_dict[d_id].weight
                for d_id in route
                if d_id in delivery_dict
            )
            if route_weight > vehicle.max_capacity:
                return False
        
        return True
    
    def _build_distance_matrix(
        self,
        deliveries: List[Delivery],
        depot_location: Tuple[float, float],
    ) -> Dict[Tuple[str, str], float]:
        """Constrói matriz de distâncias."""
        matrix = {}
        depot_key = "depot"
        
        for d1 in deliveries:
            for d2 in deliveries:
                if d1.id != d2.id:
                    matrix[(d1.id, d2.id)] = calculate_distance(
                        d1.location, d2.location
                    )
        
        for d in deliveries:
            matrix[(depot_key, d.id)] = calculate_distance(
                depot_location, d.location
            )
            matrix[(d.id, depot_key)] = calculate_distance(
                d.location, depot_location
            )
        
        return matrix
    
    def _initial_solution(
        self,
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
        depot_location: Tuple[float, float],
        distance_matrix: Dict[Tuple[str, str], float],
    ) -> List[List[str]]:
        """Gera solução inicial usando Greedy."""
        from hospital_routes.optimization.greedy_optimizer import GreedyOptimizer
        
        greedy = GreedyOptimizer()
        result = greedy.optimize(
            deliveries, vehicles,
            OptimizationConfig(population_size=1, generations=1),
            depot_location
        )
        return result.solution.routes
    
    def _generate_neighbor(
        self,
        current_routes: List[List[str]],
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
    ) -> List[List[str]]:
        """
        Gera solução vizinha aplicando operadores de mutação.
        
        Operadores:
        - Swap: Troca duas entregas
        - Move: Move entrega de uma rota para outra
        - Reverse: Inverte ordem de uma rota
        """
        neighbor = [route.copy() for route in current_routes]
        
        # Escolher operador aleatório
        operator = random.choice(["swap", "move", "reverse"])
        
        if operator == "swap":
            # Trocar duas entregas aleatórias
            all_deliveries = [
                (r_idx, d_idx, d_id)
                for r_idx, route in enumerate(neighbor)
                for d_idx, d_id in enumerate(route)
            ]
            if len(all_deliveries) >= 2:
                (r1, d1_idx, d1), (r2, d2_idx, d2) = random.sample(all_deliveries, 2)
                neighbor[r1][d1_idx] = d2
                neighbor[r2][d2_idx] = d1
        
        elif operator == "move":
            # Mover entrega de uma rota para outra
            all_deliveries = [
                (r_idx, d_idx, d_id)
                for r_idx, route in enumerate(neighbor)
                for d_idx, d_id in enumerate(route)
            ]
            if all_deliveries:
                r1, d1_idx, d1 = random.choice(all_deliveries)
                r2 = random.randint(0, len(neighbor) - 1)
                
                neighbor[r1].pop(d1_idx)
                if not neighbor[r1]:
                    neighbor.pop(r1)
                    if r2 >= len(neighbor):
                        r2 = len(neighbor) - 1
                
                if r2 < len(neighbor):
                    insert_pos = random.randint(0, len(neighbor[r2]))
                    neighbor[r2].insert(insert_pos, d1)
        
        elif operator == "reverse":
            # Inverter ordem de uma rota
            if neighbor:
                route_idx = random.randint(0, len(neighbor) - 1)
                if neighbor[route_idx]:
                    neighbor[route_idx].reverse()
        
        return neighbor
    
    def _calculate_fitness(
        self,
        routes: List[List[str]],
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
        depot_location: Tuple[float, float],
        distance_matrix: Dict[Tuple[str, str], float],
    ) -> float:
        """Calcula fitness de uma solução."""
        solution = self._routes_to_solution(
            routes, deliveries, vehicles, depot_location, distance_matrix
        )
        return self.composite_fitness.calculate(
            solution, deliveries, vehicles, depot_location, distance_matrix
        )
    
    def _routes_to_solution(
        self,
        routes: List[List[str]],
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
        depot_location: Tuple[float, float],
        distance_matrix: Dict[Tuple[str, str], float],
    ) -> RouteSolution:
        """Converte rotas em RouteSolution."""
        delivery_dict = {d.id: d for d in deliveries}
        depot_key = "depot"
        
        # Calcular distância total
        total_distance = 0.0
        for route in routes:
            if not route:
                continue
            total_distance += distance_matrix.get((depot_key, route[0]), 0.0)
            for i in range(len(route) - 1):
                total_distance += distance_matrix.get((route[i], route[i + 1]), 0.0)
            total_distance += distance_matrix.get((route[-1], depot_key), 0.0)
        
        # Calcular custo
        total_cost = 0.0
        for route_idx, route in enumerate(routes):
            if route_idx < len(vehicles):
                vehicle = vehicles[route_idx]
                route_distance = 0.0
                if route:
                    route_distance += distance_matrix.get((depot_key, route[0]), 0.0)
                    for i in range(len(route) - 1):
                        route_distance += distance_matrix.get((route[i], route[i + 1]), 0.0)
                    route_distance += distance_matrix.get((route[-1], depot_key), 0.0)
                total_cost += route_distance * vehicle.fuel_cost_per_km
                total_cost += (route_distance / 50.0) * vehicle.driver_cost_per_hour
        
        # Calcular violações
        violations = {}
        capacity_violation = 0.0
        autonomy_violation = 0.0
        
        for route_idx, route in enumerate(routes):
            if route_idx >= len(vehicles):
                continue
            vehicle = vehicles[route_idx]
            route_weight = sum(
                delivery_dict[d_id].weight
                for d_id in route
                if d_id in delivery_dict
            )
            if route_weight > vehicle.max_capacity:
                capacity_violation += route_weight - vehicle.max_capacity
            
            route_distance = 0.0
            if route:
                route_distance += distance_matrix.get((depot_key, route[0]), 0.0)
                for i in range(len(route) - 1):
                    route_distance += distance_matrix.get((route[i], route[i + 1]), 0.0)
                route_distance += distance_matrix.get((route[-1], depot_key), 0.0)
            if route_distance > vehicle.max_range:
                autonomy_violation += route_distance - vehicle.max_range
        
        violations["capacity"] = capacity_violation
        violations["autonomy"] = autonomy_violation
        
        solution = RouteSolution(
            routes=routes,
            total_distance=total_distance,
            total_cost=total_cost,
            fitness_score=0.0,
            violations=violations,
            metadata={"algorithm": "simulated_annealing"},
        )
        
        fitness = self.composite_fitness.calculate(
            solution, deliveries, vehicles, depot_location, distance_matrix
        )
        solution.fitness_score = fitness
        
        return solution

