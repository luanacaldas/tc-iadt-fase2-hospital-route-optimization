"""
DTOs (Data Transfer Objects) para comunicação entre módulos.

IMPORTANTE: Estas são classes de transferência de dados, NÃO entidades de domínio.
As entidades de domínio estão em hospital_routes.domain/

DTOs são usados para:
- Comunicação entre camadas (optimization → llm → visualization)
- Serialização/Deserialização (JSON)
- Evitar vazamento de lógica de domínio entre módulos
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime

# Re-export das classes principais definidas em interfaces.py
# para manter compatibilidade e facilitar imports
from hospital_routes.core.interfaces import (
    OptimizationConfig,
    VehicleConstraints,
    Delivery,
    RouteSolution,
    OptimizationResult,
    ReportRequest,
    ReportResult,
)


@dataclass
class HospitalDTO:
    """
    DTO: Representa um hospital ou ponto de depósito.
    
    NOTA: Esta é uma classe de transferência de dados.
    A entidade de domínio está em hospital_routes.domain.hospital.Hospital
    """
    
    id: str
    name: str
    location: tuple[float, float]  # (latitude, longitude)
    address: str
    operating_hours: Optional[Dict[str, tuple[float, float]]] = None  # Horários de funcionamento


@dataclass
class RouteSegmentDTO:
    """
    DTO: Segmento de uma rota entre dois pontos.
    
    Usado para transferência de dados entre módulos de otimização e visualização.
    """
    
    from_location: tuple[float, float]
    to_location: tuple[float, float]
    distance_km: float
    estimated_time_hours: float
    delivery_id: Optional[str] = None  # ID da entrega no destino


@dataclass
class OptimizedRouteDTO:
    """
    DTO: Rota completa de um veículo otimizada.
    
    NOTA: Esta é uma classe de transferência de dados.
    A entidade de domínio está em hospital_routes.domain.route.Route
    """
    
    vehicle_id: int
    segments: List[RouteSegmentDTO]
    total_distance_km: float
    total_time_hours: float
    total_weight_kg: float
    deliveries: List[str]  # IDs das entregas
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


@dataclass
class OptimizationMetricsDTO:
    """
    DTO: Métricas de performance da otimização.
    
    Usado para transferência de métricas entre módulos de otimização e relatórios.
    """
    
    total_distance_km: float
    total_cost: float
    total_time_hours: float
    vehicles_used: int
    capacity_utilization: float  # Percentual médio de utilização de capacidade
    range_utilization: float  # Percentual médio de utilização de autonomia
    priority_deliveries_served: int  # Número de entregas críticas atendidas
    violations: Dict[str, float] = field(default_factory=dict)


@dataclass
class GenerationStatisticsDTO:
    """
    DTO: Estatísticas de uma geração do algoritmo genético.
    
    Usado para análise e visualização do progresso da otimização.
    """
    
    generation: int
    best_fitness: float
    avg_fitness: float
    worst_fitness: float
    diversity: float  # Diversidade da população
    convergence_rate: float  # Taxa de convergência


# Aliases para compatibilidade (deprecated - usar classes DTO)
Hospital = HospitalDTO
RouteSegment = RouteSegmentDTO
VehicleRoute = OptimizedRouteDTO
OptimizationMetrics = OptimizationMetricsDTO
GenerationStatistics = GenerationStatisticsDTO

