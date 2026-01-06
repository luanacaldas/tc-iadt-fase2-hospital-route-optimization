"""
Entidade de domínio: Hospital/Depósito.

Representa um hospital ou ponto de depósito no domínio.
Esta é uma entidade de domínio, não um DTO.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Tuple


@dataclass
class Hospital:
    """
    Entidade de domínio: Hospital/Depósito.
    
    Representa um hospital ou ponto de depósito onde as rotas começam/terminam.
    """
    
    id: str
    name: str
    location: Tuple[float, float]  # (latitude, longitude)
    address: str
    operating_hours: Optional[Dict[str, Tuple[float, float]]] = None  # Horários de funcionamento
    
    def is_open_at(self, day: str, hour: float) -> bool:
        """
        Verifica se o hospital está aberto em um determinado dia e hora.
        
        Args:
            day: Dia da semana (ex: "monday", "tuesday")
            hour: Hora do dia (0-24)
        
        Returns:
            bool: True se estiver aberto, False caso contrário
        """
        if self.operating_hours is None:
            return True  # Assume sempre aberto se não especificado
        
        if day.lower() not in self.operating_hours:
            return False
        
        start, end = self.operating_hours[day.lower()]
        return start <= hour <= end

