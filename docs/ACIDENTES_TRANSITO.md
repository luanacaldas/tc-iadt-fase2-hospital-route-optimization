# ⚠️ Sistema de Dados de Acidentes de Trânsito

Este documento explica como usar o sistema de integração de dados de acidentes de trânsito no mapa de rotas.

## 📋 Visão Geral

O sistema permite:

- ✅ Visualizar pontos de acidentes no mapa
- ✅ Analisar risco de segurança das rotas
- ✅ Colorir rotas baseado no nível de risco
- ✅ Mostrar estatísticas de acidentes por rota
- ✅ Integrar dados reais ou simulados

## 🚀 Uso Básico

### 1. Usar Dados Simulados (Padrão)

```python
from hospital_routes.utils.accident_data import create_sample_accident_data
from hospital_routes.visualization.map_generator import MapGenerator

# Criar provedor com dados de exemplo
accident_provider = create_sample_accident_data()

# Gerar mapa com dados de acidentes
map_obj = MapGenerator.generate_route_map(
    result,
    deliveries,
    depot_location,
    "mapa.html",
    accident_provider=accident_provider,
    show_accidents=True,
)
```

### 2. Usar Dados Reais (JSON)

```python
from hospital_routes.utils.accident_data import AccidentDataProvider

# Carregar dados de arquivo JSON
accident_provider = AccidentDataProvider(data_file="accidents_data.json")

# Usar no mapa
map_obj = MapGenerator.generate_route_map(
    result,
    deliveries,
    depot_location,
    "mapa.html",
    accident_provider=accident_provider,
)
```

## 📊 Formato de Dados JSON

Crie um arquivo `accidents_data.json`:

```json
{
  "accidents": [
    {
      "location": [-23.52, -46.62],
      "accidents_count": 25,
      "severity": 4.2,
      "risk_level": "high",
      "road_name": "Marginal Tietê"
    },
    {
      "location": [-23.555, -46.66],
      "accidents_count": 15,
      "severity": 3.5,
      "risk_level": "medium",
      "road_name": "Av. Paulista"
    }
  ]
}
```

### Campos Obrigatórios

- `location`: `[latitude, longitude]` - Coordenadas do ponto
- `accidents_count`: `int` - Número de acidentes no último ano
- `severity`: `float` - Severidade média (1.0 a 5.0)
- `risk_level`: `string` - Nível de risco: `"low"`, `"medium"`, `"high"`, `"critical"`

### Campos Opcionais

- `road_name`: `string` - Nome da via

## 🎨 Visualização no Mapa

### Cores de Risco

- 🟢 **Verde** (`low`) - Baixo risco
- 🟡 **Amarelo** (`medium`) - Risco médio
- 🟠 **Laranja** (`high`) - Alto risco
- 🔴 **Vermelho** (`critical`) - Risco crítico

### Elementos Visuais

1. **Marcadores de Acidentes**: Círculos coloridos nos pontos de acidente
2. **Rotas Coloridas**: Rotas com alto risco ficam mais escuras/vermelhas
3. **Popups Informativos**: Clique nos marcadores para ver detalhes
4. **Camada de Acidentes**: Ative/desative no controle de camadas do mapa

## 📈 Análise de Rotas

O sistema calcula automaticamente:

```python
route_risk = accident_provider.get_route_risk(route_coordinates)

# Retorna:
{
    "total_accidents": 45,           # Total de acidentes no trajeto
    "avg_severity": 3.2,             # Severidade média
    "high_risk_segments": 3,         # Segmentos de alto risco
    "overall_risk": "high",          # Risco geral da rota
    "risk_segments": [...]           # Detalhes de cada segmento
}
```

## 🔗 Integração com APIs Reais

### Exemplo: Integração com API de Trânsito

```python
import requests
from hospital_routes.utils.accident_data import AccidentDataProvider, AccidentData

class APITrafficAccidentProvider(AccidentDataProvider):
    """Provedor que busca dados de API real."""

    def __init__(self, api_url: str, api_key: str):
        super().__init__()
        self.api_url = api_url
        self.api_key = api_key
        self._fetch_data()

    def _fetch_data(self):
        """Busca dados da API."""
        response = requests.get(
            self.api_url,
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        data = response.json()

        for item in data:
            self.add_accident_data(
                (item["lat"], item["lon"]),
                AccidentData(
                    location=(item["lat"], item["lon"]),
                    accidents_count=item["count"],
                    severity=item["severity"],
                    risk_level=self._calculate_risk(item["count"], item["severity"]),
                    road_name=item.get("road"),
                )
            )

    def _calculate_risk(self, count: int, severity: float) -> str:
        """Calcula nível de risco."""
        if count < 5 and severity < 2.0:
            return "low"
        elif count < 10 and severity < 3.0:
            return "medium"
        elif count < 20 or severity >= 3.5:
            return "high"
        return "critical"
```

## 🎯 Casos de Uso

### 1. Otimização Considerando Segurança

```python
# Calcular risco de cada rota
for route in routes:
    risk = accident_provider.get_route_risk(route.coordinates)
    # Penalizar rotas de alto risco no fitness
    if risk["overall_risk"] in ["high", "critical"]:
        fitness_penalty += 1000
```

### 2. Alertas para Motoristas

```python
route_risk = accident_provider.get_route_risk(route_coordinates)

if route_risk["overall_risk"] == "critical":
    print("🚨 ALERTA: Rota com risco crítico de acidentes!")
    print(f"   {route_risk['total_accidents']} acidentes no último ano")
```

### 3. Relatórios de Segurança

```python
# Gerar relatório de segurança
for vehicle_id, route in enumerate(routes):
    risk = accident_provider.get_route_risk(route)
    print(f"Veículo {vehicle_id + 1}:")
    print(f"  Risco: {risk['overall_risk']}")
    print(f"  Acidentes: {risk['total_accidents']}")
    print(f"  Segmentos perigosos: {risk['high_risk_segments']}")
```

## 📝 Fontes de Dados Reais

### São Paulo

- **CET (Companhia de Engenharia de Tráfego)**: Dados oficiais de acidentes
- **Infosiga SP**: Sistema de informações de acidentes
- **OpenStreetMap**: Dados de vias e tráfego

### APIs Públicas

- **Google Maps Roads API**: Informações de vias
- **Waze API**: Dados de tráfego em tempo real
- **OpenRouteService**: Dados de rotas e vias

## 🔧 Configuração Avançada

### Ajustar Sensibilidade

```python
# Buscar acidentes em raio maior
accident_data = provider.get_accident_data(
    location,
    radius_km=0.5  # 500 metros
)
```

### Cache de Dados

```python
# Salvar cache de acidentes
provider = AccidentDataProvider(data_file="accidents_cache.json")
# Dados são automaticamente salvos e carregados
```

## 💡 Dicas

1. **Dados Simulados**: Use `create_sample_accident_data()` para testes
2. **Dados Reais**: Integre com APIs oficiais para produção
3. **Performance**: Cache dados de acidentes para melhor performance
4. **Atualização**: Atualize dados periodicamente (mensal/trimestral)

## 🐛 Troubleshooting

### Acidentes não aparecem no mapa

- Verifique se `show_accidents=True`
- Confirme que `accident_provider` não é `None`
- Ative a camada "Pontos de Acidentes" no controle de camadas

### Dados não carregam

- Verifique formato do JSON
- Confirme coordenadas válidas
- Veja logs para erros de parsing

---

**Desenvolvido para tornar as rotas hospitalares mais seguras! 🏥🚗**
