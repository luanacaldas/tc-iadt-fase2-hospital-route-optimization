"""
Entidade de domínio: Entrega.

Representa uma entrega no domínio do problema de otimização de rotas.
Esta é uma entidade de domínio, não um DTO.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Delivery:
    """
    Entidade de domínio: Entrega.
    
    Representa uma entrega que precisa ser realizada.
    """
    
    id: str
    location: tuple[float, float]  # (latitude, longitude)
    priority: int  # 1 = crítico (medicamentos), 2 = normal (insumos)
    weight: float  # Peso da entrega (kg)
    time_window_start: Optional[float] = None  # Janela de tempo início (horas)
    time_window_end: Optional[float] = None  # Janela de tempo fim (horas)
    estimated_service_time: float = 0.5  # Tempo de serviço em horas
    description: Optional[str] = None  # Descrição da entrega
    
    def is_critical(self) -> bool:
        """Verifica se a entrega é crítica (medicamentos)."""
        return self.priority == 1
    
    def has_time_window(self) -> bool:
        """Verifica se a entrega tem janela de tempo."""
        return (
            self.time_window_start is not None
            and self.time_window_end is not None
        )

