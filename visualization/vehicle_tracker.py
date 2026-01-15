"""
Rastreamento de Veículos em Tempo Real (Simulado).

Simula o rastreamento de veículos com atualizações periódicas.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

from hospital_routes.core.interfaces import (
    OptimizationResult,
    Delivery,
    RouteSolution,
)


class VehicleStatus(Enum):
    """Status do veículo."""
    WAITING = "Aguardando início"
    IN_TRANSIT = "Em trânsito"
    DELIVERING = "Entregando"
    RETURNING = "Retornando"
    COMPLETED = "Concluído"


@dataclass
class VehicleTracking:
    """Informações de rastreamento de um veículo."""
    vehicle_id: int
    status: VehicleStatus
    current_location: tuple[float, float]
    next_stop: Optional[str] = None
    next_stop_name: Optional[str] = None
    distance_to_next: float = 0.0
    eta: Optional[datetime] = None
    speed: float = 0.0  # km/h
    progress_percent: float = 0.0
    route: List[str] = None
    completed_deliveries: List[str] = None


class VehicleTracker:
    """Rastreia veículos em tempo real (simulado)."""
    
    def __init__(self, start_time: Optional[datetime] = None):
        """
        Args:
            start_time: Horário de início do rastreamento
        """
        if start_time is None:
            self.start_time = datetime.now()
        else:
            self.start_time = start_time
        
        self.trackings: Dict[int, VehicleTracking] = {}
        self._initialize_trackings()
    
    def _initialize_trackings(self):
        """Inicializa rastreamentos (será chamado quando houver dados)."""
        pass
    
    def initialize_from_solution(
        self,
        optimization_result: OptimizationResult,
        deliveries: List[Delivery],
        depot_location: tuple[float, float],
    ):
        """
        Inicializa rastreamentos a partir da solução de otimização.
        
        Args:
            optimization_result: Resultado da otimização
            deliveries: Lista de entregas
            depot_location: Localização do depósito
        """
        solution = optimization_result.solution
        delivery_dict = {d.id: d for d in deliveries}
        
        self.trackings = {}
        
        for vehicle_idx, route in enumerate(solution.routes):
            if not route:
                continue
            
            vehicle_id = vehicle_idx + 1
            
            # Determinar status inicial
            current_time = datetime.now()
            if current_time < self.start_time:
                status = VehicleStatus.WAITING
            else:
                status = VehicleStatus.IN_TRANSIT
            
            # Próxima parada
            next_stop = route[0] if route else None
            next_stop_name = None
            if next_stop and next_stop in delivery_dict:
                delivery = delivery_dict[next_stop]
                # Tentar obter nome do hospital (se disponível)
                next_stop_name = delivery.id
            
            tracking = VehicleTracking(
                vehicle_id=vehicle_id,
                status=status,
                current_location=depot_location,
                next_stop=next_stop,
                next_stop_name=next_stop_name,
                distance_to_next=0.0,
                eta=None,
                speed=0.0,
                progress_percent=0.0,
                route=route.copy(),
                completed_deliveries=[],
            )
            
            self.trackings[vehicle_id] = tracking
    
    def update_tracking(self, vehicle_id: int, current_time: datetime) -> VehicleTracking:
        """
        Atualiza informações de rastreamento de um veículo.
        
        Args:
            vehicle_id: ID do veículo
            current_time: Tempo atual (simulado)
        
        Returns:
            Informações atualizadas de rastreamento
        """
        if vehicle_id not in self.trackings:
            return None
        
        tracking = self.trackings[vehicle_id]
        
        # Simular progresso baseado no tempo
        elapsed = (current_time - self.start_time).total_seconds() / 3600.0  # horas
        
        # Calcular progresso (simplificado)
        if tracking.route:
            total_deliveries = len(tracking.route)
            completed = len(tracking.completed_deliveries)
            tracking.progress_percent = (completed / total_deliveries) * 100 if total_deliveries > 0 else 0
            
            # Atualizar status
            if tracking.progress_percent == 0:
                tracking.status = VehicleStatus.WAITING if current_time < self.start_time else VehicleStatus.IN_TRANSIT
            elif tracking.progress_percent < 100:
                tracking.status = VehicleStatus.IN_TRANSIT
            else:
                tracking.status = VehicleStatus.COMPLETED
            
            # Velocidade simulada
            tracking.speed = 45.0 if tracking.status == VehicleStatus.IN_TRANSIT else 0.0
        
        return tracking
    
    def get_all_trackings(self, current_time: Optional[datetime] = None) -> List[VehicleTracking]:
        """
        Obtém rastreamentos de todos os veículos.
        
        Args:
            current_time: Tempo atual (se None, usa datetime.now())
        
        Returns:
            Lista de rastreamentos
        """
        if current_time is None:
            current_time = datetime.now()
        
        return [
            self.update_tracking(vehicle_id, current_time)
            for vehicle_id in self.trackings.keys()
        ]
