"""
Componente de fitness: Penalidade por atraso em entregas prioritárias.

Penaliza soluções que atrasam entregas críticas (medicamentos).
"""

from typing import List
from hospital_routes.core.interfaces import Delivery, RouteSolution


class PriorityPenalty:
    """
    Calcula a penalidade por atraso em entregas prioritárias.
    
    Entregas com priority=1 (críticas) devem ser atendidas primeiro.
    Quanto mais tarde uma entrega crítica é atendida, maior a penalidade.
    """
    
    def __init__(self, penalty_weight: float = 500.0):
        """
        Args:
            penalty_weight: Peso da penalidade por atraso
        """
        self.penalty_weight = penalty_weight
    
    def calculate(
        self,
        solution: RouteSolution,
        deliveries: List[Delivery],
    ) -> float:
        """
        Calcula a penalidade total por atraso em entregas prioritárias.
        
        A penalidade é baseada na posição da entrega crítica na rota.
        Entregas críticas no início da rota = menor penalidade.
        
        Args:
            solution: Solução de rota
            deliveries: Lista de entregas
        
        Returns:
            float: Penalidade total (já multiplicada pelo peso)
        """
        total_penalty = 0.0
        
        # Criar dicionário de entregas para acesso rápido
        delivery_dict = {d.id: d for d in deliveries}
        
        # Para cada rota, calcular penalidade baseada na posição das entregas críticas
        for route in solution.routes:
            for position, delivery_id in enumerate(route):
                if delivery_id in delivery_dict:
                    delivery = delivery_dict[delivery_id]
                    
                    # Se é entrega crítica (priority=1)
                    if delivery.priority == 1:
                        # Penalidade aumenta com a posição na rota
                        # Primeira entrega = 0, segunda = 1, etc.
                        penalty = position * self.penalty_weight
                        total_penalty += penalty
        
        return total_penalty

