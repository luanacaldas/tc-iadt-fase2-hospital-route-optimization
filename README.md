# 🏥 Sistema de Otimização de Rotas Hospitalares

> Sistema inteligente de distribuição de medicamentos com Algoritmos Genéticos, LLMs e visualização em tempo real

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![MapBox](https://img.shields.io/badge/MapBox-GL_JS_3.0-green.svg)](https://www.mapbox.com/)
[![Ollama](https://img.shields.io/badge/LLM-Ollama-orange.svg)](https://ollama.ai/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📑 Índice

- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Demo Interativa](#-demo-interativa)
- [Arquitetura](#-arquitetura)
- [Instalação](#-instalação)
- [Início Rápido](#-início-rápido)
- [Algoritmo Genético](#-algoritmo-genético)
- [Integração LLM](#-integração-llm)
- [Rastreamento ao Vivo](#-rastreamento-ao-vivo)
- [Conformidade Requisitos](#-conformidade-requisitos)
- [Documentação](#-documentação)

---

## 🎯 Visão Geral

Sistema completo para otimizar distribuição de medicamentos hospitalares que resolve o **Vehicle Routing Problem (VRP)** com múltiplas restrições realistas, gera relatórios inteligentes usando LLMs e oferece rastreamento em tempo real.

### 🎪 Problema Resolvido

- **Tipo**: Vehicle Routing Problem (VRP) com múltiplos veículos
- **Cenário**: Distribuição de medicamentos para hospitais de São Paulo
- **Restrições**: Capacidade, autonomia, prioridades críticas, múltiplos veículos
- **Método**: Algoritmo Genético com 6 componentes de fitness
- **LLM**: Relatórios operacionais, instruções para motoristas, chatbot analítico

---

## ✨ Funcionalidades

### 🧬 Otimização Avançada

- ✅ **Algoritmo Genético** especializado para VRP
- ✅ **6 componentes de fitness**: distância, capacidade, autonomia, prioridade, balanceamento, veículos
- ✅ **Operadores genéticos customizados**: Order Crossover, múltiplas mutações
- ✅ **Restrições realistas**: capacidade de carga, autonomia, entregas críticas
- ✅ **Busca local**: 2-opt e inter-route swap para refinamento
- ✅ **Elitismo e early stopping**: convergência otimizada

### 🤖 Inteligência Artificial

- ✅ **Chatbot analítico** com Ollama (Llama 3.2)
- ✅ **Relatórios automáticos**: diário, semanal, gerencial
- ✅ **Instruções para motoristas**: geradas por LLM
- ✅ **Análise inteligente**: sugestões de melhorias baseadas em dados reais
- ✅ **Linguagem natural**: perguntas e respostas contextuais

### 📍 Rastreamento em Tempo Real

- ✅ **Visualização MapBox GL JS 3.0** com rotas completas
- ✅ **Movimento suave**: atualização a cada 100ms (10 FPS)
- ✅ **Marcadores interativos**: hospitais 🏥 e veículos 🚗
- ✅ **Popups dinâmicos**: info em tempo real (status, velocidade, ETA)
- ✅ **Trails/rastros**: caminho percorrido por cada veículo
- ✅ **Notificações toast**: alertas de chegada em hospitais
- ✅ **Controle de velocidade**: 0.5x até 10x para simulação
- ✅ **Responsivo**: mobile-first design

### 📊 Interface Profissional

- ✅ **Design system** com Inter font e paleta semântica
- ✅ **Header slim** com métricas KPI em tempo real
- ✅ **Dashboard completo**: distância, custo, veículos, entregas, críticas
- ✅ **Mapa interativo Folium**: rotas otimizadas coloridas
- ✅ **Chatbot integrado**: análise conversacional das rotas

---

## 🎬 Demo Interativa

### 1️⃣ Interface Principal (Dashboard)

```bash
python app_scripts/open_interface.py
```

Abra: `http://localhost:5000`

**Funcionalidades**:

- Header profissional com 5 KPIs (distância, custo, veículos, entregas, críticas)
- Botão "Rastrear" → abre rastreamento ao vivo em nova aba
- Chatbot interativo para análise de rotas
- Mapa com rotas otimizadas

### 2️⃣ Rastreamento ao Vivo (MapBox)

```bash
# Clique no botão "Rastrear" no dashboard
# OU abra diretamente:
# interfaces/rastreamento_mapbox.html
```

**Funcionalidades**:

- 🗺️ **Rotas completas** desenhadas no mapa (LineString)
- 🏥 **Marcadores hospitais** com popups informativos
- 🚗 **3 veículos** simulados (azul, vermelho, verde)
- ⚡ **Movimento suave** 100ms (vs 3000ms anterior)
- 📊 **Popups veículos** com status, destino, velocidade, ETA
- 🛤️ **Trails/rastros** mostrando caminho percorrido
- 🔔 **Notificações** quando veículo chega em hospital
- 🎛️ **Controle velocidade** (0.5x, 1x, 2x, 5x, 10x)
- 📱 **Responsivo** para mobile

### 3️⃣ Chatbot Analítico

```bash
# Integrado no dashboard principal
# Perguntas exemplo:
- "Analise a eficiência das rotas"
- "Há entregas críticas?"
- "Qual a distância total?"
- "Sugira melhorias"
- "Compare os veículos"
```

---

## 🏗️ Arquitetura

### Estrutura de Módulos (SOLID)

```
hospital_routes/
├── 📁 core/                    # 🎯 Interfaces e modelos base
│   ├── interfaces.py           # BaseOptimizer, BaseReporter
│   ├── models.py               # OptimizationResult, RouteInfo
│   └── exceptions.py           # Exceções customizadas
│
├── 📁 optimization/            # 🧬 Motor de otimização
│   ├── genetic_algorithm.py    # Algoritmo Genético VRP
│   ├── local_search.py         # 2-opt, inter-route swap
│   ├── fitness/                # Componentes de fitness
│   │   ├── composite_fitness.py
│   │   ├── distance_fitness.py
│   │   ├── capacity_penalty.py
│   │   ├── autonomy_penalty.py
│   │   ├── priority_penalty.py
│   │   └── load_balance_penalty.py
│   └── strategies/             # Estratégias de inicialização
│
├── 📁 llm/                     # 🤖 Inteligência Artificial
│   ├── chatbot.py              # Chatbot analítico (Ollama)
│   ├── ollama_reporter.py      # Gerador de relatórios
│   ├── prompts.py              # Templates de prompts
│   └── route_analyzer.py       # Análise inteligente de rotas
│
├── 📁 visualization/           # 📊 Visualização
│   ├── map_generator.py        # Mapas Folium
│   └── chatbot_interface_v2.py # Dashboard Flask
│
├── 📁 domain/                  # 🏥 Entidades de domínio
│   ├── hospital.py
│   ├── vehicle.py
│   ├── delivery.py
│   └── route.py
│
├── 📁 utils/                   # 🛠️ Utilitários
│   ├── distance_calculator.py  # Haversine, OSRM
│   └── data_loader.py          # Carregamento de dados
│
├── 📁 interfaces/              # 🎨 Interfaces HTML (NOVO!)
│   ├── chatbot_interface_v2.html   # Dashboard principal
│   ├── chatbot_interface.html      # Dashboard v1 (legado)
│   └── rastreamento_mapbox.html    # Rastreamento tempo real
│
├── 📁 app_scripts/             # 🚀 Scripts executáveis (NOVO!)
│   ├── run_chatbot_interface.py    # Servidor Flask
│   ├── seed_real_data.py           # Dados realistas SP
│   ├── server_chatbot.py           # API chatbot
│   ├── setup_ollama.py             # Configurar Ollama
│   ├── run_demo.py                 # Demo completo
│   └── test_optimization.py        # Testes otimização
│
├── 📁 docs/                    # 📚 Documentação (NOVO!)
│   ├── VERIFICACAO_REQUISITOS.md   # Conformidade detalhada
│   ├── COMO_EXECUTAR.md            # Guia execução
│   ├── COMO_USAR_CHATBOT.md        # Tutorial chatbot
│   ├── COMO_RESOLVER_OLLAMA.md     # Troubleshooting Ollama
│   ├── GUIA_RAPIDO_CHATBOT.md      # Quick start
│   ├── INSTALACAO_FLASK.md         # Setup Flask
│   ├── SOLUCAO_FLASK.md            # Resolução problemas
│   ├── MELHORIAS_ALGORITMO.md      # Otimizações genético
│   ├── MELHORIAS_CHATBOT.md        # Análises LLM
│   ├── MELHORIAS_SENIOR.md         # Best practices
│   ├── UX_HEADER_REDESIGN.md       # Design system
│   └── ORGANIZACAO_PROJETO.md      # Este documento de organização
│
├── 📁 output/                  # 📤 Arquivos gerados (NOVO!)
│   ├── route_map.html          # Mapa gerado (gitignored)
│   ├── driver_instructions.txt # Instruções geradas
│   └── route_analysis.txt      # Análises geradas
│
├── 📁 examples/                # 💡 Exemplos de uso
│
├── cli.py                      # 🖥️ Interface linha de comando
├── requirements.txt            # 📦 Dependências Python
└── README.md                   # 📖 Este arquivo
```

### Princípios de Design

- **SOLID**: Interfaces abstratas, injeção de dependência
- **Strategy Pattern**: Algoritmos intercambiáveis
- **Composite Pattern**: Função fitness modular
- **Factory Pattern**: Criação de otimizadores
- **Observer Pattern**: Rastreamento em tempo real

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.10+
- Ollama (para LLM)
- Conta MapBox (token gratuito)

### Passo 1: Clonar Repositório

```bash
git clone https://github.com/seu-usuario/hospital_routes.git
cd hospital_routes
```

### Passo 2: Instalar Dependências

```bash
# Criar ambiente virtual
python -m venv .

# Ativar (Windows)
.\Scripts\activate

# Ativar (Linux/Mac)
source bin/activate

# Instalar pacotes
pip install -r requirements.txt
```

### Passo 3: Instalar Ollama

```bash
# Windows/Mac/Linux
# Baixar de: https://ollama.ai/download

# Instalar modelo Llama 3.2
ollama pull llama3.2
```

### Passo 4: Configurar MapBox

1. Criar conta gratuita: https://account.mapbox.com/
2. Copiar Access Token
3. Atualizar `interfaces/rastreamento_mapbox.html` linha ~650:

```javascript
mapboxgl.accessToken = "SEU_TOKEN_AQUI";
```

---

## 🎯 Início Rápido

### Opção 1: Interface Completa (Recomendado)

```bash
# 1. Iniciar servidor Flask
python app_scripts/scripts/run_chatbot_interface.py

# 2. Abrir navegador
# http://localhost:5000

# 3. Explorar funcionalidades:
#    - Ver mapa com rotas otimizadas
#    - Clicar em "Rastrear" → rastreamento ao vivo
#    - Usar chatbot para análise
```

### Opção 2: CLI (Terminal)

```bash
# 1. Gerar dados realistas
python app_scripts/seed_real_data.py

# 2. Executar otimização
python cli.py

# 3. Abrir mapa gerado
# output/route_map.html
```

### Opção 3: API Programática

```python
from optimization.genetic_algorithm import GeneticAlgorithmOptimizer
from core.interfaces import VehicleConstraints, Delivery
from utils.distance_calculator import HaversineDistanceCalculator

# Configurar veículos
vehicles = [
    VehicleConstraints(id="V1", max_capacity=150, max_range=100, cost_per_km=2.5),
    VehicleConstraints(id="V2", max_capacity=200, max_range=120, cost_per_km=3.0)
]

# Configurar entregas
deliveries = [
    Delivery(
        id="H001", hospital_name="Hospital das Clínicas",
        latitude=-23.5646, longitude=-46.6708,
        urgency_level=1,  # Crítico
        required_capacity=50
    ),
    # ... mais entregas
]

# Otimizar
optimizer = GeneticAlgorithmOptimizer()
result = optimizer.optimize(
    deliveries=deliveries,
    vehicles=vehicles,
    depot_location=(-23.5505, -46.6333),  # São Paulo
    distance_calculator=HaversineDistanceCalculator()
)

print(f"Distância total: {result.total_distance:.2f} km")
print(f"Custo total: R$ {result.total_cost:.2f}")
print(f"Veículos usados: {len(result.routes)}")
```

---

## 🧬 Algoritmo Genético

### Representação Genética

```python
# Individual = List[List[str]]
# Cada lista interna = rota de um veículo

individual = [
    ["H001", "H003", "H005"],  # Veículo 1
    ["H002", "H004"],          # Veículo 2
    ["H006", "H007", "H008"]   # Veículo 3
]
```

### Função Fitness (6 Componentes)

```
fitness = α * distance                  # Minimizar distância total
       + β * capacity_penalty          # Penalizar violação capacidade
       + γ * autonomy_penalty          # Penalizar violação autonomia
       + δ * priority_penalty          # Penalizar atraso críticos
       + ζ * load_balance_penalty      # Balancear carga entre veículos
       + ε * vehicle_penalty           # Minimizar número veículos
```

**Pesos Padrão**:

- `α = 1.0` (distância base)
- `β = 1000.0` (capacidade - alta penalidade)
- `γ = 1000.0` (autonomia - alta penalidade)
- `δ = 500.0` (prioridade - média penalidade)
- `ζ = 50.0` (balanceamento - baixa penalidade)
- `ε = 100.0` (veículos - média penalidade)

### Operadores Genéticos

#### 1. Seleção

- **Método**: Tournament Selection (torneio com 3 indivíduos)
- **Pressão seletiva**: Média

#### 2. Crossover

- **Método**: Order Crossover (OX) adaptado para VRP
- **Taxa**: 70%
- **Características**: Preserva ordem parcial, respeita capacidade

#### 3. Mutação

- **Operadores**:
  - Swap (troca dentro da rota)
  - Insertion (move para outra posição)
  - Inter-route swap (move entre rotas)
  - Route merge (combina rotas)
- **Taxa**: 20%

#### 4. Busca Local

- **2-opt**: Otimiza rotas individuais
- **Inter-route swap**: Balanceia carga
- **Aplicação**: Após cada geração no melhor indivíduo

### Configuração

```python
config = OptimizationConfig(
    population_size=100,
    num_generations=200,
    crossover_rate=0.7,
    mutation_rate=0.2,
    elite_size=5,
    tournament_size=3,
    max_iterations_without_improvement=50
)
```

---

## 🤖 Integração LLM

### Ollama (Local, Gratuito)

```python
from llm.chatbot import RouteChatbot

chatbot = RouteChatbot(model="llama3.2")
chatbot.set_optimization_context(result, deliveries)

# Análise conversacional
response = chatbot.chat("Há melhorias possíveis nas rotas?")
print(response)
```

### Relatórios Automáticos

```python
from llm.ollama_reporter import OllamaReporter

reporter = OllamaReporter()

# 1. Instruções para motoristas
instructions = reporter.generate_driver_instructions(result, deliveries, vehicles)

# 2. Relatório diário
daily = reporter.generate_daily_summary(result, deliveries)

# 3. Análise semanal
weekly = reporter.generate_weekly_analysis(result, deliveries)

# 4. Relatório gerencial
managerial = reporter.generate_managerial_report(result, deliveries, vehicles)
```

### Análise Inteligente

```python
from llm.route_analyzer import RouteAnalyzer

analyzer = RouteAnalyzer()
analysis = analyzer.analyze_route(result, deliveries, vehicles)

print(f"Distribuição de carga: {analysis['load_distribution']}")
print(f"Sugestões: {analysis['recommendations']}")
```

---

## 📍 Rastreamento ao Vivo

### 8 Funcionalidades Profissionais

#### 1. 🗺️ Rotas no Mapa

```javascript
// LineString para cada veículo com cores distintas
drawRoutes() → Visualiza rotas planejadas
```

#### 2. 🏥 Marcadores Hospitais

```javascript
// Ícone 🏥 com popups informativos
addHospitalMarkers() → Destinos com hover effects
```

#### 3. ⚡ Movimento Suave

```javascript
// 100ms updates (vs 3000ms anterior)
updatePositions() → 10 FPS, UI render 1Hz
```

#### 4. 🎛️ Header Controles

```html
<!-- Dropdown velocidade: 0.5x, 1x, 2x, 5x, 10x -->
<select id="speedControl" onchange="changeSimulationSpeed()"></select>
```

#### 5. 💬 Popups Veículos

```javascript
// Info tempo real: Status, Destino, Velocidade, ETA
getVehiclePopupHTML(vehicle) → Atualização automática
```

#### 6. 🛤️ Trails/Rastros

```javascript
// LineString mostrando caminho percorrido
initializeTrails() + updateTrail() → Cores por veículo
```

#### 7. 🔔 Notificações Toast

```javascript
// Alertas de chegada com animações
showNotification(message, type) → Auto-remove 3s
```

#### 8. 📱 Responsividade Mobile

```css
/* Grid 1 coluna, header stack, botões apenas ícones */
@media (max-width: 768px) {
  ...;
}
```

### Personalização

```javascript
// Ajustar velocidade base dos veículos
vehicles: [
    { id: 1, baseSpeed: 45, ... },
    { id: 2, baseSpeed: 35, ... }
]

// Ajustar intervalo de atualização
setInterval(updatePositions, 100); // 100ms = 10 FPS
```

---

## ✅ Conformidade Requisitos

### Requisito 1: Sistema Otimização (Algoritmos Genéticos)

| Item                       | Status | Evidência                            |
| -------------------------- | ------ | ------------------------------------ |
| 1.1 Sistema TSP/VRP        | ✅     | `optimization/genetic_algorithm.py`  |
| 1.2 Representação Genética | ✅     | DEAP Individual (List[List[str]])    |
| 1.3 Operadores Genéticos   | ✅     | Tournament, OX Crossover, 4 mutações |
| 1.4 Função Fitness         | ✅     | 6 componentes modulares              |
| 1.5.1 Prioridades          | ✅     | `PriorityPenalty` + críticos         |
| 1.5.2 Capacidade           | ✅     | `CapacityPenalty` + max_capacity     |
| 1.5.3 Autonomia            | ✅     | `AutonomyPenalty` + max_range        |
| 1.5.4 Múltiplos Veículos   | ✅     | VRP completo                         |
| 1.5.5 Outras Restrições    | ✅     | Balanceamento + busca local          |
| 1.6 Visualização Mapa      | ✅     | Folium + MapBox GL JS                |

### Requisito 3: Integração LLMs

| Item                            | Status | Evidência                                                |
| ------------------------------- | ------ | -------------------------------------------------------- |
| 3.1 Instruções Motoristas       | ✅     | `OllamaReporter.generate_driver_instructions()`          |
| 3.2 Relatórios Diários/Semanais | ✅     | `generate_daily_summary()`, `generate_weekly_analysis()` |
| 3.3 Sugestões Melhorias         | ✅     | `RouteChatbot.chat()`, `RouteAnalyzer`                   |
| 3.4 Prompts Eficientes          | ✅     | `llm/prompts.py`, system prompts estruturados            |
| 3.5 Linguagem Natural           | ✅     | Interface web + API REST + Ollama                        |

**✅ TODOS OS REQUISITOS OBRIGATÓRIOS IMPLEMENTADOS E FUNCIONAIS!**

---

## 📚 Documentação

### Guias Principais

- 📖 **[VERIFICACAO_REQUISITOS.md](docs/VERIFICACAO_REQUISITOS.md)** - Conformidade detalhada
- 🏗️ **[ARCHITECTURE.md](ARCHITECTURE.md)** - Arquitetura completa
- 📦 **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Estrutura de pastas
- 🎨 **[UX_HEADER_REDESIGN.md](docs/UX_HEADER_REDESIGN.md)** - Design system

### Guias Rápidos

- 🚀 **[GUIA_RAPIDO_CHATBOT.md](GUIA_RAPIDO_CHATBOT.md)** - Usar chatbot
- 💬 **[COMO_USAR_CHATBOT.md](COMO_USAR_CHATBOT.md)** - Tutorial completo
- 🔧 **[COMO_RESOLVER_OLLAMA.md](COMO_RESOLVER_OLLAMA.md)** - Troubleshooting
- ⚙️ **[INSTALACAO_FLASK.md](INSTALACAO_FLASK.md)** - Setup servidor

### Melhorias Implementadas

- 📊 **[MELHORIAS_ALGORITMO.md](docs/MELHORIAS_ALGORITMO.md)** - Otimizações genético
- 🤖 **[MELHORIAS_CHATBOT.md](docs/MELHORIAS_CHATBOT.md)** - Análises LLM
- 👨‍💼 **[MELHORIAS_SENIOR.md](docs/MELHORIAS_SENIOR.md)** - Best practices
- 🎨 **[UX_HEADER_REDESIGN.md](docs/UX_HEADER_REDESIGN.md)** - UI profissional

---

## 🛠️ Tecnologias

### Backend

- **Python 3.10+**: Linguagem principal
- **DEAP**: Framework algoritmos genéticos
- **Flask**: Servidor web API REST
- **Ollama**: LLM local (Llama 3.2)

### Frontend

- **HTML5/CSS3/JavaScript ES6+**: Interface web
- **MapBox GL JS 3.0**: Mapas interativos
- **Folium**: Visualização estática rotas
- **Inter Font (Google Fonts)**: Tipografia profissional

### Libs Python

- `deap`: Algoritmos evolutivos
- `folium`: Mapas Leaflet
- `requests`: Cliente HTTP
- `flask`, `flask-cors`: API REST
- `python-dotenv`: Configuração

---

## 🎓 Exemplos de Uso

### Exemplo 1: Otimização Básica

```bash
python cli.py
```

### Exemplo 2: Dashboard Completo

```bash
python app_scripts/run_chatbot_interface.py
# http://localhost:5000
```

### Exemplo 3: Rastreamento Direto

```bash
# Abrir interfaces/rastreamento_mapbox.html no navegador
# OU clicar em "Rastrear" no dashboard
```

### Exemplo 4: Chatbot API

```python
import requests

response = requests.post('http://localhost:5000/api/chat', json={
    "message": "Analise a eficiência das rotas"
})
print(response.json()['response'])
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

<div align="center">

**[⬆ Voltar ao topo](#-sistema-de-otimização-de-rotas-hospitalares)**

Feito com ❤️ e ☕

</div>
