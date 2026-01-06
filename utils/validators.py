"""
Validações de dados do sistema.

Este módulo contém funções de validação para garantir integridade dos dados.
"""

from typing import List
from hospital_routes.core.interfaces import Delivery, VehicleConstraints
from hospital_routes.core.exceptions import DataValidationError


def validate_deliveries(deliveries: List[Delivery]) -> None:
    """
    Valida lista de entregas.
    
    Args:
        deliveries: Lista de entregas a validar
    
    Raises:
        DataValidationError: Se houver dados inválidos
    """
    if not deliveries:
        raise DataValidationError("Lista de entregas não pode estar vazia")
    
    delivery_ids = set()
    for delivery in deliveries:
        if not delivery.id:
            raise DataValidationError("Entrega deve ter ID")
        
        if delivery.id in delivery_ids:
            raise DataValidationError(f"ID duplicado: {delivery.id}")
        delivery_ids.add(delivery.id)
        
        if delivery.weight <= 0:
            raise DataValidationError(f"Peso inválido para entrega {delivery.id}")
        
        if delivery.priority not in [1, 2]:
            raise DataValidationError(
                f"Prioridade inválida para entrega {delivery.id}. "
                "Deve ser 1 (crítico) ou 2 (normal)"
            )


def validate_vehicles(vehicles: List[VehicleConstraints]) -> None:
    """
    Valida lista de veículos.
    
    Args:
        vehicles: Lista de veículos a validar
    
    Raises:
        DataValidationError: Se houver dados inválidos
    """
    if not vehicles:
        raise DataValidationError("Lista de veículos não pode estar vazia")
    
    for vehicle in vehicles:
        if vehicle.max_capacity <= 0:
            raise DataValidationError("Capacidade máxima deve ser positiva")
        
        if vehicle.max_range <= 0:
            raise DataValidationError("Autonomia máxima deve ser positiva")
        
        if vehicle.fuel_cost_per_km < 0:
            raise DataValidationError("Custo de combustível não pode ser negativo")
        
        if vehicle.driver_cost_per_hour < 0:
            raise DataValidationError("Custo do motorista não pode ser negativo")

