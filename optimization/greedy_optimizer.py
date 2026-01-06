"""
Implementação do algoritmo Greedy (Nearest Neighbor) para otimização de rotas.

Este módulo implementa uma abordagem gulosa simples que sempre escolhe
a entrega mais próxima como próxima parada.
"""

import time
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


class GreedyOptimizer(BaseOptimizer):
    """
    Otimizador de rotas usando algoritmo Greedy (Nearest Neighbor).
    
    Estratégia: Sempre escolhe a entrega mais próxima como próxima parada.
    Rápido mas pode não encontrar a solução ótima.
    """
    
    def __init__(self, fitness_weights: FitnessWeights = None):
        """
        Args:
            fitness_weights: Pesos da função de fitness (usa padrão se None)
        """
        self.fitness_weights = fitness_weights or FitnessWeights()
        self.composite_fitness = CompositeFitness(self.fitness_weights)
    
    def optimize(
        self,
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
        config: OptimizationConfig,
        depot_location: Tuple[float, float],
    ) -> OptimizationResult:
        """
        Otimiza rotas usando algoritmo Greedy.
        
        Args:
            deliveries: Lista de entregas
            vehicles: Lista de veículos disponíveis
            config: Configuração (não usada no Greedy, mas mantida para compatibilidade)
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
            
            # Resolver usando Greedy
            routes = self._solve_greedy(
                deliveries, vehicles, depot_location, distance_matrix
            )
            
            # Calcular métricas
            solution = self._routes_to_solution(
                routes, deliveries, vehicles, depot_location, distance_matrix
            )
            
            execution_time = time.time() - start_time
            
            return OptimizationResult(
                solution=solution,
                execution_time=execution_time,
                generations_evolved=1,  # Greedy não usa gerações
                best_fitness_history=[solution.fitness_score],
                config=config,
                statistics={
                    "algorithm": "greedy",
                    "num_routes": len(routes),
                },
            )
        
        except Exception as e:
            raise OptimizationError(f"Erro durante otimização Greedy: {str(e)}") from e
    
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
        
        # Distâncias entre entregas
        for d1 in deliveries:
            for d2 in deliveries:
                if d1.id != d2.id:
                    matrix[(d1.id, d2.id)] = calculate_distance(
                        d1.location, d2.location
                    )
        
        # Distâncias do depósito
        for d in deliveries:
            matrix[(depot_key, d.id)] = calculate_distance(
                depot_location, d.location
            )
            matrix[(d.id, depot_key)] = calculate_distance(
                d.location, depot_location
            )
        
        return matrix
    
    def _solve_greedy(
        self,
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
        depot_location: Tuple[float, float],
        distance_matrix: Dict[Tuple[str, str], float],
    ) -> List[List[str]]:
        """
        Resolve o problema usando estratégia Greedy.
        
        Para cada veículo, sempre escolhe a entrega mais próxima que cabe.
        """
        routes = []
        remaining_deliveries = {d.id: d for d in deliveries}
        depot_key = "depot"
        
        # Priorizar entregas críticas primeiro
        critical_deliveries = [
            d_id for d_id, d in remaining_deliveries.items() if d.priority == 1
        ]
        normal_deliveries = [
            d_id for d_id, d in remaining_deliveries.items() if d.priority != 1
        ]
        
        # Ordenar por prioridade (críticas primeiro)
        delivery_order = critical_deliveries + normal_deliveries
        
        for vehicle_idx, vehicle in enumerate(vehicles):
            if not remaining_deliveries:
                break
            
            route = []
            current_location = depot_key
            current_weight = 0.0
            current_range = 0.0
            
            while remaining_deliveries:
                # Encontrar entrega mais próxima que cabe no veículo
                nearest = None
                nearest_distance = float('inf')
                nearest_id = None
                
                # Tentar primeiro entregas críticas, depois normais
                candidates = delivery_order if delivery_order else list(remaining_deliveries.keys())
                
                for delivery_id in candidates:
                    if delivery_id not in remaining_deliveries:
                        continue
                    
                    delivery = remaining_deliveries[delivery_id]
                    distance = distance_matrix.get((current_location, delivery_id), float('inf'))
                    
                    # Verificar se cabe no veículo
                    if (current_weight + delivery.weight <= vehicle.max_capacity and
                        current_range + distance <= vehicle.max_range):
                        
                        if distance < nearest_distance:
                            nearest = delivery
                            nearest_distance = distance
                            nearest_id = delivery_id
                
                if nearest_id:
                    # Adicionar à rota
                    route.append(nearest_id)
                    current_location = nearest_id
                    current_weight += nearest.weight
                    current_range += nearest_distance
                    del remaining_deliveries[nearest_id]
                    if nearest_id in delivery_order:
                        delivery_order.remove(nearest_id)
                else:
                    # Nenhuma entrega cabe, terminar rota deste veículo
                    break
            
            if route:
                routes.append(route)
        
        # Se ainda há entregas não atribuídas, criar rotas adicionais
        # (isso violará restrições, mas será penalizado no fitness)
        while remaining_deliveries:
            route = [list(remaining_deliveries.keys())[0]]
            del remaining_deliveries[route[0]]
            routes.append(route)
        
        return routes
    
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
            
            # Depósito → primeira entrega
            total_distance += distance_matrix.get((depot_key, route[0]), 0.0)
            
            # Entre entregas
            for i in range(len(route) - 1):
                total_distance += distance_matrix.get((route[i], route[i + 1]), 0.0)
            
            # Última entrega → depósito
            total_distance += distance_matrix.get((route[-1], depot_key), 0.0)
        
        # Calcular custo total
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
            fitness_score=0.0,  # Será calculado depois
            violations=violations,
            metadata={"algorithm": "greedy"},
        )
        
        # Calcular fitness
        fitness = self.composite_fitness.calculate(
            solution, deliveries, vehicles, depot_location, distance_matrix
        )
        solution.fitness_score = fitness
        
        return solution

