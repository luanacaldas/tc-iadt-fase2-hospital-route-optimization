"""
Comparador de Cenários de Otimização.

Compara a solução atual com outras abordagens (greedy, baseline, etc.).
"""

from typing import List, Dict, Optional
from dataclasses import dataclass

from hospital_routes.core.interfaces import (
    OptimizationResult,
    Delivery,
    VehicleConstraints,
    OptimizationConfig,
)
from hospital_routes.optimization.greedy_optimizer import GreedyOptimizer


@dataclass
class ScenarioComparison:
    """Comparação entre cenários."""
    metric: str
    current: float
    greedy: Optional[float] = None
    baseline: Optional[float] = None
    alternative: Optional[float] = None


class ScenarioComparator:
    """Compara diferentes cenários de otimização."""
    
    def __init__(self):
        self.greedy_optimizer = GreedyOptimizer()
    
    def compare_scenarios(
        self,
        current_result: OptimizationResult,
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
        config: OptimizationConfig,
        depot_location: tuple[float, float],
    ) -> Dict[str, ScenarioComparison]:
        """
        Compara a solução atual com outros cenários.
        
        Args:
            current_result: Resultado da otimização atual
            deliveries: Lista de entregas
            vehicles: Lista de veículos
            config: Configuração de otimização
            depot_location: Localização do depósito
        
        Returns:
            Dicionário com comparações de métricas
        """
        comparisons = {}
        
        # Solução atual
        current_solution = current_result.solution
        
        # Calcular métricas da solução atual
        current_distance = current_solution.total_distance
        current_cost = current_solution.total_cost
        current_vehicles = len([r for r in current_solution.routes if r])
        current_violations = sum(current_solution.violations.values())
        
        # Calcular tempo estimado (simplificado)
        current_time = self._estimate_delivery_time(current_solution, deliveries)
        
        # Solução Greedy
        try:
            greedy_result = self.greedy_optimizer.optimize(
                deliveries, vehicles, config, depot_location
            )
            greedy_solution = greedy_result.solution
            greedy_distance = greedy_solution.total_distance
            greedy_cost = greedy_solution.total_cost
            greedy_vehicles = len([r for r in greedy_solution.routes if r])
            greedy_violations = sum(greedy_solution.violations.values())
            greedy_time = self._estimate_delivery_time(greedy_solution, deliveries)
        except Exception:
            greedy_distance = greedy_cost = greedy_vehicles = greedy_violations = greedy_time = None
        
        # Solução Baseline (sem otimização - ordem sequencial)
        baseline_distance, baseline_cost, baseline_vehicles, baseline_violations, baseline_time = \
            self._calculate_baseline(deliveries, vehicles, depot_location)
        
        # Criar comparações
        comparisons['distance'] = ScenarioComparison(
            metric='Distância Total',
            current=current_distance,
            greedy=greedy_distance,
            baseline=baseline_distance,
        )
        
        comparisons['cost'] = ScenarioComparison(
            metric='Custo Total',
            current=current_cost,
            greedy=greedy_cost,
            baseline=baseline_cost,
        )
        
        comparisons['vehicles'] = ScenarioComparison(
            metric='Veículos Usados',
            current=float(current_vehicles),
            greedy=float(greedy_vehicles) if greedy_vehicles else None,
            baseline=float(baseline_vehicles),
        )
        
        comparisons['time'] = ScenarioComparison(
            metric='Tempo Entrega',
            current=current_time,
            greedy=greedy_time,
            baseline=baseline_time,
        )
        
        comparisons['violations'] = ScenarioComparison(
            metric='Violações',
            current=float(current_violations),
            greedy=float(greedy_violations) if greedy_violations else None,
            baseline=float(baseline_violations),
        )
        
        return comparisons
    
    def _estimate_delivery_time(
        self,
        solution: RouteSolution,
        deliveries: List[Delivery],
    ) -> float:
        """Estima tempo total de entrega em horas."""
        delivery_dict = {d.id: d for d in deliveries}
        total_time = 0.0
        
        for route in solution.routes:
            if not route:
                continue
            
            # Tempo de viagem (simplificado: 1h por 40km)
            route_distance = solution.total_distance / len([r for r in solution.routes if r])
            travel_time = route_distance / 40.0
            
            # Tempo de serviço
            service_time = sum(
                delivery_dict.get(did, Delivery(id='', location=(0, 0), priority=2, weight=0)).estimated_service_time
                for did in route
            )
            
            total_time += travel_time + service_time
        
        return total_time
    
    def _calculate_baseline(
        self,
        deliveries: List[Delivery],
        vehicles: List[VehicleConstraints],
        depot_location: tuple[float, float],
    ) -> tuple[float, float, int, float, float]:
        """Calcula métricas da solução baseline (sem otimização)."""
        from hospital_routes.utils.distance import calculate_distance
        
        # Baseline: distribuir entregas sequencialmente entre veículos
        num_vehicles = len(vehicles)
        deliveries_per_vehicle = len(deliveries) // num_vehicles
        
        total_distance = 0.0
        total_cost = 0.0
        violations = 0.0
        
        for vehicle_idx in range(num_vehicles):
            start_idx = vehicle_idx * deliveries_per_vehicle
            end_idx = start_idx + deliveries_per_vehicle if vehicle_idx < num_vehicles - 1 else len(deliveries)
            route_deliveries = deliveries[start_idx:end_idx]
            
            if not route_deliveries:
                continue
            
            vehicle = vehicles[vehicle_idx]
            
            # Calcular distância da rota
            route_distance = 0.0
            current_location = depot_location
            
            for delivery in route_deliveries:
                route_distance += calculate_distance(current_location, delivery.location)
                current_location = delivery.location
            
            # Voltar ao depósito
            route_distance += calculate_distance(current_location, depot_location)
            
            total_distance += route_distance
            
            # Custo
            route_cost = route_distance * vehicle.fuel_cost_per_km
            route_cost += (route_distance / 50.0) * vehicle.driver_cost_per_hour
            total_cost += route_cost
            
            # Verificar violações
            route_weight = sum(d.weight for d in route_deliveries)
            if route_weight > vehicle.max_capacity:
                violations += 1.0
            if route_distance > vehicle.max_range:
                violations += 1.0
        
        # Tempo estimado
        estimated_time = total_distance / 40.0 + len(deliveries) * 0.5
        
        return total_distance, total_cost, num_vehicles, violations, estimated_time
    
    def calculate_savings(self, comparisons: Dict[str, ScenarioComparison]) -> Dict[str, Dict]:
        """Calcula economia gerada comparando com outros cenários."""
        savings = {}
        
        # Comparação com Greedy
        if comparisons['cost'].greedy is not None:
            cost_diff = comparisons['cost'].greedy - comparisons['cost'].current
            cost_percent = (cost_diff / comparisons['cost'].greedy) * 100 if comparisons['cost'].greedy > 0 else 0
            
            distance_diff = comparisons['distance'].greedy - comparisons['distance'].current if comparisons['distance'].greedy else 0
            
            savings['vs_greedy'] = {
                'cost_savings': cost_diff,
                'cost_percent': cost_percent,
                'distance_savings': distance_diff,
            }
        
        # Comparação com Baseline
        if comparisons['cost'].baseline is not None:
            cost_diff = comparisons['cost'].baseline - comparisons['cost'].current
            cost_percent = (cost_diff / comparisons['cost'].baseline) * 100 if comparisons['cost'].baseline > 0 else 0
            
            distance_diff = comparisons['distance'].baseline - comparisons['distance'].current
            
            # Calcular CO2 evitado (aproximado: 0.24 kg CO2 por km)
            co2_avoided = distance_diff * 0.24
            
            savings['vs_baseline'] = {
                'cost_savings': cost_diff,
                'cost_percent': cost_percent,
                'distance_savings': distance_diff,
                'co2_avoided': co2_avoided,
            }
        
        return savings
