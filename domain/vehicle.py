"""
Entidade de domínio: Veículo.

Representa um veículo no domínio do problema de otimização de rotas.
Esta é uma entidade de domínio, não um DTO.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Vehicle:
    """
    Entidade de domínio: Veículo.
    
    Representa um veículo que pode realizar entregas.
    """
    
    id: str
    max_capacity: float  # Capacidade máxima de carga (kg)
    max_range: float  # Autonomia máxima (km)
    fuel_cost_per_km: float  # Custo de combustível por km
    driver_cost_per_hour: float  # Custo do motorista por hora
    vehicle_type: Optional[str] = None  # Tipo de veículo (ex: "van", "truck")
    
    def can_carry(self, weight: float) -> bool:
        """Verifica se o veículo pode carregar o peso especificado."""
        return weight <= self.max_capacity
    
    def can_travel(self, distance: float) -> bool:
        """Verifica se o veículo pode percorrer a distância especificada."""
        return distance <= self.max_range

