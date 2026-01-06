"""
Utilitários para cálculo de distâncias geográficas.

Este módulo fornece funções para calcular distâncias entre pontos
usando coordenadas geográficas (latitude, longitude).
"""

from typing import Tuple
from geopy.distance import geodesic


def calculate_distance(
    point1: Tuple[float, float],
    point2: Tuple[float, float],
) -> float:
    """
    Calcula a distância em quilômetros entre dois pontos geográficos.
    
    Usa a fórmula de Haversine (geodesic) para calcular a distância
    real na superfície da Terra.
    
    Args:
        point1: Tupla (latitude, longitude) do primeiro ponto
        point2: Tupla (latitude, longitude) do segundo ponto
    
    Returns:
        float: Distância em quilômetros
    
    Example:
        >>> calculate_distance((40.7128, -74.0060), (34.0522, -118.2437))
        3944.0  # Aproximadamente distância NYC-LA
    """
    return geodesic(point1, point2).kilometers


def calculate_distance_matrix(
    points: list[Tuple[float, float]],
) -> dict[Tuple[int, int], float]:
    """
    Calcula matriz de distâncias entre todos os pares de pontos.
    
    Útil para otimização de performance, evitando recalcular
    distâncias repetidamente.
    
    Args:
        points: Lista de pontos (latitude, longitude)
    
    Returns:
        dict: Dicionário onde chave é (índice1, índice2) e valor é distância em km
    
    Example:
        >>> points = [(40.7128, -74.0060), (34.0522, -118.2437)]
        >>> matrix = calculate_distance_matrix(points)
        >>> matrix[(0, 1)]
        3944.0
    """
    matrix = {}
    n = len(points)
    
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[(i, j)] = calculate_distance(points[i], points[j])
            else:
                matrix[(i, j)] = 0.0
    
    return matrix


def calculate_route_distance(
    route: list[Tuple[float, float]],
    return_to_start: bool = True,
) -> float:
    """
    Calcula a distância total de uma rota.
    
    Args:
        route: Lista de pontos na ordem da rota
        return_to_start: Se True, inclui distância do último ponto ao primeiro
    
    Returns:
        float: Distância total da rota em quilômetros
    """
    if len(route) < 2:
        return 0.0
    
    total_distance = 0.0
    
    # Distâncias entre pontos consecutivos
    for i in range(len(route) - 1):
        total_distance += calculate_distance(route[i], route[i + 1])
    
    # Retornar ao ponto inicial se solicitado
    if return_to_start and len(route) > 2:
        total_distance += calculate_distance(route[-1], route[0])
    
    return total_distance

