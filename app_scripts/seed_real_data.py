"""
Dados reais de hospitais de São Paulo para testes de otimização de rotas.

Este arquivo contém informações de hospitais reais de São Paulo,
incluindo localizações (latitude/longitude) e dados para simulação
de entregas de medicamentos e insumos hospitalares.
"""

from typing import List, Tuple
from hospital_routes.core.interfaces import (
    Delivery,
    VehicleConstraints,
    OptimizationConfig,
)


# Localização do depósito central (exemplo: Centro de Distribuição em São Paulo)
DEPOT_LOCATION: Tuple[float, float] = (-23.5505, -46.6333)  # Centro de SP


# Dados de hospitais reais de São Paulo
# Formato: (nome, latitude, longitude, endereço)
HOSPITALS_DATA = [
    # Zona Sul
    ("Hospital Albert Einstein", -23.5928, -46.6889, "Av. Albert Einstein, 627 - Morumbi"),
    ("Hospital Sírio-Libanês", -23.5560, -46.6566, "Rua Dona Adma Jafet, 91 - Bela Vista"),
    ("Hospital 9 de Julho", -23.5560, -46.6566, "Rua Peixoto Gomide, 625 - Bela Vista"),
    ("Hospital Santa Catarina", -23.5431, -46.6367, "Av. Paulista, 200 - Bela Vista"),
    
    # Zona Norte
    ("Hospital do Mandaqui", -23.4859, -46.6333, "Rua Voluntários da Pátria, 4301 - Santana"),
    ("Hospital São Paulo (UNIFESP)", -23.6028, -46.6703, "Rua Botucatu, 740 - Vila Clementino"),
    ("Hospital Santa Marcelina", -23.5631, -46.4642, "Rua Santa Marcelina, 177 - Parque do Carmo"),
    
    # Zona Leste
    ("Hospital Municipal Dr. Moysés Deutsch", -23.5431, -46.6125, "Av. Celso Garcia, 4815 - Tatuapé"),
    ("Hospital Municipal Vila Nova Cachoeirinha", -23.4859, -46.6703, "Rua Dr. Antônio Bento, 575 - Vila Nova Cachoeirinha"),
    
    # Zona Oeste
    ("Instituto do Câncer de São Paulo", -23.5558, -46.6732, "Av. Dr. Arnaldo, 251 - Cerqueira César"),
    ("Hospital das Clínicas FMUSP", -23.5558, -46.6732, "Av. Dr. Enéas de Carvalho Aguiar, 255 - Cerqueira César"),
    
    # Centro
    ("Hospital Beneficência Portuguesa", -23.5489, -46.6388, "Rua Maestro Cardim, 769 - Bela Vista"),
    ("Hospital Samaritano", -23.5431, -46.6367, "Rua Conselheiro Brotero, 1486 - Higienópolis"),
]


def generate_deliveries() -> List[Delivery]:
    """
    Gera lista de entregas baseadas em hospitais reais de São Paulo.
    
    Returns:
        List[Delivery]: Lista de entregas para hospitais
    """
    deliveries = []
    
    # Entregas críticas (medicamentos - priority=1)
    critical_deliveries = [
        # Hospital Albert Einstein - Medicamentos urgentes
        Delivery(
            id="HOSP_001",
            location=(-23.5928, -46.6889),
            weight=15.0,
            priority=1,
        ),
        # Hospital Sírio-Libanês - Medicamentos de emergência
        Delivery(
            id="HOSP_002",
            location=(-23.5560, -46.6566),
            weight=12.0,
            priority=1,
        ),
        # Hospital das Clínicas - Medicamentos críticos
        Delivery(
            id="HOSP_003",
            location=(-23.5558, -46.6732),
            weight=20.0,
            priority=1,
        ),
        # Instituto do Câncer - Quimioterápicos
        Delivery(
            id="HOSP_004",
            location=(-23.5558, -46.6732),
            weight=18.0,
            priority=1,
        ),
        # Hospital 9 de Julho - Medicamentos cardíacos
        Delivery(
            id="HOSP_005",
            location=(-23.5560, -46.6566),
            weight=10.0,
            priority=1,
        ),
    ]
    
    # Entregas normais (insumos - priority=2)
    normal_deliveries = [
        # Hospital do Mandaqui - Insumos gerais
        Delivery(
            id="HOSP_006",
            location=(-23.4859, -46.6333),
            weight=25.0,
            priority=2,
        ),
        # Hospital Santa Catarina - Material de limpeza
        Delivery(
            id="HOSP_007",
            location=(-23.5431, -46.6367),
            weight=30.0,
            priority=2,
        ),
        # Hospital São Paulo UNIFESP - Equipamentos
        Delivery(
            id="HOSP_008",
            location=(-23.6028, -46.6703),
            weight=22.0,
            priority=2,
        ),
        # Hospital Santa Marcelina - Insumos
        Delivery(
            id="HOSP_009",
            location=(-23.5631, -46.4642),
            weight=28.0,
            priority=2,
        ),
        # Hospital Beneficência Portuguesa - Material cirúrgico
        Delivery(
            id="HOSP_010",
            location=(-23.5489, -46.6388),
            weight=15.0,
            priority=2,
        ),
        # Hospital Samaritano - Insumos
        Delivery(
            id="HOSP_011",
            location=(-23.5431, -46.6367),
            weight=20.0,
            priority=2,
        ),
        # Hospital Municipal Dr. Moysés Deutsch - Material geral
        Delivery(
            id="HOSP_012",
            location=(-23.5431, -46.6125),
            weight=18.0,
            priority=2,
        ),
    ]
    
    deliveries = critical_deliveries + normal_deliveries
    return deliveries


def generate_vehicles() -> List[VehicleConstraints]:
    """
    Gera lista de veículos para as entregas.
    
    Returns:
        List[VehicleConstraints]: Lista de veículos disponíveis
    """
    vehicles = [
        # Veículo 1: Van média (para entregas críticas)
        VehicleConstraints(
            max_capacity=50.0,  # 50 kg
            max_range=150.0,  # 150 km
            fuel_cost_per_km=2.5,
            driver_cost_per_hour=25.0,
        ),
        # Veículo 2: Van média
        VehicleConstraints(
            max_capacity=50.0,
            max_range=150.0,
            fuel_cost_per_km=2.5,
            driver_cost_per_hour=25.0,
        ),
        # Veículo 3: Caminhão pequeno (para insumos)
        VehicleConstraints(
            max_capacity=100.0,  # 100 kg
            max_range=200.0,  # 200 km
            fuel_cost_per_km=3.5,
            driver_cost_per_hour=30.0,
        ),
    ]
    return vehicles


def get_optimization_config() -> OptimizationConfig:
    """
    Retorna configuração padrão para otimização.
    
    Returns:
        OptimizationConfig: Configuração do algoritmo genético
    """
    return OptimizationConfig(
        population_size=50,
        generations=100,
        crossover_rate=0.8,
        mutation_rate=0.2,
        max_iterations_without_improvement=20,
    )


def get_depot_location() -> Tuple[float, float]:
    """
    Retorna localização do depósito central.
    
    Returns:
        Tuple[float, float]: (latitude, longitude) do depósito
    """
    return DEPOT_LOCATION


# Função auxiliar para obter informações de um hospital
def get_hospital_info(hospital_id: str) -> dict:
    """
    Retorna informações de um hospital pelo ID.
    
    Args:
        hospital_id: ID da entrega (ex: "HOSP_001")
    
    Returns:
        dict: Informações do hospital ou None se não encontrado
    """
    # Mapeamento de IDs para índices nos dados
    hospital_map = {
        "HOSP_001": 0,  # Hospital Albert Einstein
        "HOSP_002": 1,  # Hospital Sírio-Libanês
        "HOSP_003": 10,  # Hospital das Clínicas
        "HOSP_004": 9,  # Instituto do Câncer
        "HOSP_005": 2,  # Hospital 9 de Julho
        "HOSP_006": 4,  # Hospital do Mandaqui
        "HOSP_007": 3,  # Hospital Santa Catarina
        "HOSP_008": 5,  # Hospital São Paulo UNIFESP
        "HOSP_009": 6,  # Hospital Santa Marcelina
        "HOSP_010": 11,  # Beneficência Portuguesa
        "HOSP_011": 12,  # Hospital Samaritano
        "HOSP_012": 7,  # Hospital Municipal Tatuapé
    }
    
    idx = hospital_map.get(hospital_id)
    if idx is None or idx >= len(HOSPITALS_DATA):
        return None
    
    nome, lat, lon, endereco = HOSPITALS_DATA[idx]
    return {
        "nome": nome,
        "endereco": endereco,
        "latitude": lat,
        "longitude": lon,
    }


if __name__ == "__main__":
    """
    Exemplo de uso dos dados.
    """
    print("🏥 Dados de Hospitais de São Paulo")
    print("=" * 60)
    print()
    
    # Gerar entregas
    deliveries = generate_deliveries()
    print(f"📦 Total de entregas: {len(deliveries)}")
    print(f"   ⚠️  Críticas (medicamentos): {sum(1 for d in deliveries if d.priority == 1)}")
    print(f"   📋 Normais (insumos): {sum(1 for d in deliveries if d.priority == 2)}")
    print()
    
    # Mostrar entregas críticas
    print("🚨 Entregas Críticas:")
    for delivery in deliveries:
        if delivery.priority == 1:
            info = get_hospital_info(delivery.id)
            if info:
                print(f"   • {delivery.id}: {info['nome']}")
                print(f"     Peso: {delivery.weight} kg | {info['endereco']}")
    print()
    
    # Mostrar entregas normais
    print("📋 Entregas Normais:")
    for delivery in deliveries:
        if delivery.priority == 2:
            info = get_hospital_info(delivery.id)
            if info:
                print(f"   • {delivery.id}: {info['nome']}")
                print(f"     Peso: {delivery.weight} kg | {info['endereco']}")
    print()
    
    # Informações do depósito
    depot = get_depot_location()
    print(f"📍 Depósito Central: ({depot[0]}, {depot[1]})")
    print("   Localização: Centro de São Paulo")
    print()
    
    # Informações dos veículos
    vehicles = generate_vehicles()
    print(f"🚚 Veículos disponíveis: {len(vehicles)}")
    for i, vehicle in enumerate(vehicles, 1):
        print(f"   Veículo {i}: Capacidade {vehicle.max_capacity} kg | Alcance {vehicle.max_range} km")

