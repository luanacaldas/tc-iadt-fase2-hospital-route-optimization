"""
Entidade de domínio: Rota.

Representa uma rota no domínio do problema de otimização.
Esta é uma entidade de domínio, não um DTO.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime, timedelta


@dataclass
class Route:
    """
    Entidade de domínio: Rota.
    
    Representa uma rota completa de um veículo.
    """
    
    vehicle_id: str
    delivery_ids: List[str] = field(default_factory=list)
    start_time: Optional[datetime] = None
    estimated_duration: Optional[timedelta] = None
    
    def add_delivery(self, delivery_id: str) -> None:
        """Adiciona uma entrega à rota."""
        if delivery_id not in self.delivery_ids:
            self.delivery_ids.append(delivery_id)
    
    def remove_delivery(self, delivery_id: str) -> None:
        """Remove uma entrega da rota."""
        if delivery_id in self.delivery_ids:
            self.delivery_ids.remove(delivery_id)
    
    def is_empty(self) -> bool:
        """Verifica se a rota está vazia."""
        return len(self.delivery_ids) == 0
