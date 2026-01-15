"""
Gerador de Timeline Visual das Entregas.

Cria uma visualização temporal das entregas com horários estimados.
"""

from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass

from hospital_routes.core.interfaces import (
    OptimizationResult,
    Delivery,
    RouteSolution,
)
from hospital_routes.utils.distance import calculate_distance


@dataclass
class TimelineEvent:
    """Evento na timeline."""
    time: datetime
    vehicle_id: int
    delivery_id: str
    delivery: Delivery
    is_critical: bool
    status: str  # 'scheduled', 'in_transit', 'delivering', 'completed'
    estimated_arrival: datetime
    estimated_departure: datetime


class TimelineGenerator:
    """Gera timeline visual das entregas."""
    
    def __init__(self, start_time: Optional[datetime] = None):
        """
        Args:
            start_time: Horário de início das entregas. Se None, usa 09:00 do dia atual.
        """
        if start_time is None:
            today = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
            self.start_time = today
        else:
            self.start_time = start_time
    
    def generate_timeline(
        self,
        optimization_result: OptimizationResult,
        deliveries: List[Delivery],
        depot_location: Tuple[float, float],
        average_speed: float = 40.0,  # km/h
    ) -> List[TimelineEvent]:
        """
        Gera timeline de eventos das entregas.
        
        Args:
            optimization_result: Resultado da otimização
            deliveries: Lista de entregas
            depot_location: Localização do depósito
            average_speed: Velocidade média dos veículos (km/h)
        
        Returns:
            Lista de eventos ordenados por tempo
        """
        events = []
        delivery_dict = {d.id: d for d in deliveries}
        solution = optimization_result.solution
        
        for vehicle_idx, route in enumerate(solution.routes):
            if not route:
                continue
            
            vehicle_id = vehicle_idx + 1
            current_time = self.start_time
            current_location = depot_location
            
            for delivery_id in route:
                if delivery_id not in delivery_dict:
                    continue
                
                delivery = delivery_dict[delivery_id]
                
                # Calcular distância até a entrega
                distance = calculate_distance(current_location, delivery.location)
                
                # Calcular tempo de viagem (horas)
                travel_time_hours = distance / average_speed
                travel_time = timedelta(hours=travel_time_hours)
                
                # Horário de chegada
                arrival_time = current_time + travel_time
                
                # Tempo de serviço
                service_time = timedelta(hours=delivery.estimated_service_time)
                
                # Horário de saída
                departure_time = arrival_time + service_time
                
                # Criar evento
                event = TimelineEvent(
                    time=arrival_time,
                    vehicle_id=vehicle_id,
                    delivery_id=delivery_id,
                    delivery=delivery,
                    is_critical=delivery.priority == 1,
                    status='scheduled',
                    estimated_arrival=arrival_time,
                    estimated_departure=departure_time,
                )
                events.append(event)
                
                # Atualizar para próxima entrega
                current_time = departure_time
                current_location = delivery.location
        
        # Ordenar eventos por tempo
        events.sort(key=lambda e: e.time)
        
        return events
    
    def get_timeline_stats(self, events: List[TimelineEvent]) -> Dict:
        """Calcula estatísticas da timeline."""
        total_events = len(events)
        critical_events = sum(1 for e in events if e.is_critical)
        
        # Verificar janelas de tempo
        on_time = 0
        near_limit = 0
        late = 0
        
        for event in events:
            delivery = event.delivery
            if delivery.time_window_start is not None and delivery.time_window_end is not None:
                arrival_hour = event.estimated_arrival.hour + event.estimated_arrival.minute / 60.0
                window_start = delivery.time_window_start
                window_end = delivery.time_window_end
                
                if window_start <= arrival_hour <= window_end:
                    on_time += 1
                elif arrival_hour < window_start + 0.5:  # 30 minutos antes
                    near_limit += 1
                elif arrival_hour > window_end:
                    late += 1
        
        return {
            'total_events': total_events,
            'critical_events': critical_events,
            'on_time': on_time,
            'near_limit': near_limit,
            'late': late,
            'start_time': events[0].time if events else None,
            'end_time': events[-1].estimated_departure if events else None,
        }
