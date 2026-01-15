"""
Sistema de dados de acidentes de trânsito por via.

Fornece dados de acidentes para integração com otimização de rotas.
Pode usar dados reais de APIs públicas ou dados simulados.
"""

from typing import Dict, Tuple, List, Optional
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass
class AccidentData:
    """
    Dados de acidentes para um segmento de via.
    
    Attributes:
        location: Coordenadas (lat, lon) do ponto
        accidents_count: Número de acidentes no último ano
        severity: Severidade média (1-5, onde 5 é mais grave)
        risk_level: Nível de risco calculado (low, medium, high, critical)
        road_name: Nome da via (opcional)
    """
    location: Tuple[float, float]
    accidents_count: int
    severity: float  # 1-5
    risk_level: str  # low, medium, high, critical
    road_name: Optional[str] = None


class AccidentDataProvider:
    """
    Provedor de dados de acidentes.
    
    Pode usar dados reais de APIs ou dados simulados.
    """
    
    def __init__(self, data_file: Optional[str] = None):
        """
        Args:
            data_file: Arquivo JSON com dados de acidentes (opcional)
        """
        self.data_file = data_file
        self._accident_cache: Dict[Tuple[float, float], AccidentData] = {}
        self._load_data()
    
    def _load_data(self) -> None:
        """Carrega dados de acidentes do arquivo se existir."""
        if not self.data_file:
            return
        
        data_path = Path(self.data_file)
        if data_path.exists():
            try:
                with open(data_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for item in data.get("accidents", []):
                        loc = tuple(item["location"])
                        self._accident_cache[loc] = AccidentData(
                            location=loc,
                            accidents_count=item["accidents_count"],
                            severity=item["severity"],
                            risk_level=item["risk_level"],
                            road_name=item.get("road_name"),
                        )
            except Exception:
                # Se houver erro, usar dados simulados
                pass
    
    def get_accident_data(
        self, location: Tuple[float, float], radius_km: float = 0.1
    ) -> Optional[AccidentData]:
        """
        Obtém dados de acidentes para uma localização.
        
        Args:
            location: Coordenadas (lat, lon)
            radius_km: Raio de busca em km (padrão: 100m)
        
        Returns:
            AccidentData ou None se não houver dados
        """
        # Buscar no cache primeiro
        if location in self._accident_cache:
            return self._accident_cache[location]
        
        # Buscar próximo (dentro do raio)
        from hospital_routes.utils.distance import calculate_distance
        
        for cached_loc, data in self._accident_cache.items():
            distance = calculate_distance(location, cached_loc)
            if distance <= radius_km:
                return data
        
        # Se não encontrou, retornar None (sem dados)
        return None
    
    def get_route_risk(
        self, route_coordinates: List[Tuple[float, float]]
    ) -> Dict[str, any]:
        """
        Calcula risco total de uma rota baseado em acidentes.
        
        Args:
            route_coordinates: Lista de coordenadas da rota
        
        Returns:
            dict com estatísticas de risco
        """
        total_accidents = 0
        total_severity = 0.0
        high_risk_segments = 0
        risk_segments = []
        
        for i in range(len(route_coordinates) - 1):
            start = route_coordinates[i]
            end = route_coordinates[i + 1]
            
            # Verificar ambos os pontos
            for point in [start, end]:
                accident_data = self.get_accident_data(point)
                if accident_data:
                    total_accidents += accident_data.accidents_count
                    total_severity += accident_data.severity
                    
                    if accident_data.risk_level in ["high", "critical"]:
                        high_risk_segments += 1
                    
                    risk_segments.append({
                        "location": point,
                        "accidents": accident_data.accidents_count,
                        "severity": accident_data.severity,
                        "risk_level": accident_data.risk_level,
                        "road_name": accident_data.road_name,
                    })
        
        # Calcular risco médio
        avg_severity = total_severity / len(risk_segments) if risk_segments else 0.0
        
        # Determinar nível de risco geral
        if total_accidents == 0:
            overall_risk = "low"
        elif total_accidents < 5 and avg_severity < 2.0:
            overall_risk = "low"
        elif total_accidents < 10 and avg_severity < 3.0:
            overall_risk = "medium"
        elif total_accidents < 20 or avg_severity >= 3.5:
            overall_risk = "high"
        else:
            overall_risk = "critical"
        
        return {
            "total_accidents": total_accidents,
            "avg_severity": avg_severity,
            "high_risk_segments": high_risk_segments,
            "overall_risk": overall_risk,
            "risk_segments": risk_segments,
        }
    
    def add_accident_data(self, location: Tuple[float, float], data: AccidentData) -> None:
        """Adiciona dados de acidentes ao cache."""
        self._accident_cache[location] = data


def create_sample_accident_data() -> AccidentDataProvider:
    """
    Cria provedor com dados de exemplo de acidentes em São Paulo.
    
    Retorna dados simulados baseados em áreas conhecidas de alto risco.
    """
    provider = AccidentDataProvider()
    
    # Áreas de alto risco conhecidas em SP (dados simulados baseados em padrões reais)
    high_risk_areas = [
        # Marginal Tietê - área conhecida por acidentes
        ((-23.5200, -46.6200), 25, 4.2, "high", "Marginal Tietê"),
        ((-23.5250, -46.6250), 18, 3.8, "high", "Marginal Tietê"),
        
        # Av. Paulista - tráfego intenso
        ((-23.5550, -46.6600), 15, 3.5, "medium", "Av. Paulista"),
        ((-23.5500, -46.6550), 12, 3.2, "medium", "Av. Paulista"),
        
        # Av. Rebouças - cruzamentos perigosos
        ((-23.5600, -46.6700), 20, 4.0, "high", "Av. Rebouças"),
        
        # Rua Augusta - área central
        ((-23.5450, -46.6400), 10, 2.8, "medium", "Rua Augusta"),
        
        # Zona Leste - algumas áreas
        ((-23.5400, -46.6100), 8, 2.5, "low", "Av. Celso Garcia"),
        ((-23.5350, -46.6050), 6, 2.2, "low", "Rua Tatuapé"),
        
        # Zona Sul - algumas áreas
        ((-23.5900, -46.6900), 14, 3.3, "medium", "Av. Morumbi"),
        ((-23.5850, -46.6850), 11, 3.0, "medium", "Av. Morumbi"),
    ]
    
    for location, accidents, severity, risk_level, road_name in high_risk_areas:
        provider.add_accident_data(
            location,
            AccidentData(
                location=location,
                accidents_count=accidents,
                severity=severity,
                risk_level=risk_level,
                road_name=road_name,
            ),
        )
    
    return provider


def get_risk_color(risk_level: str) -> str:
    """
    Retorna cor correspondente ao nível de risco.
    
    Args:
        risk_level: Nível de risco (low, medium, high, critical)
    
    Returns:
        str: Cor em formato hex ou nome
    """
    colors = {
        "low": "#28a745",      # Verde
        "medium": "#ffc107",    # Amarelo
        "high": "#fd7e14",      # Laranja
        "critical": "#dc3545",  # Vermelho
    }
    return colors.get(risk_level, "#6c757d")  # Cinza padrão


def get_risk_icon(risk_level: str) -> str:
    """
    Retorna ícone correspondente ao nível de risco.
    
    Args:
        risk_level: Nível de risco
    
    Returns:
        str: Nome do ícone Font Awesome
    """
    icons = {
        "low": "check-circle",
        "medium": "exclamation-triangle",
        "high": "exclamation-circle",
        "critical": "times-circle",
    }
    return icons.get(risk_level, "info-circle")
