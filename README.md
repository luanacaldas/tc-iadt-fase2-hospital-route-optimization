# Hospital Route Optimization System

Intelligent medication delivery routing for hospitals, combining Genetic Algorithms, local LLM reporting, and real-time route tracking.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Mapbox](https://img.shields.io/badge/Mapbox-GL%20JS%203.0-000000)
![Ollama](https://img.shields.io/badge/Ollama-Llama%203.2-green)
![License](https://img.shields.io/badge/License-TBD-lightgrey)

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Interactive Demo](#interactive-demo)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Genetic Algorithm](#genetic-algorithm)
- [LLM Integration](#llm-integration)
- [Real-Time Tracking](#real-time-tracking)
- [Requirements Compliance](#requirements-compliance)
- [Documentation](#documentation)
- [Technology Stack](#technology-stack)
- [Usage Examples](#usage-examples)
- [Contributing](#contributing)
- [License](#license)

## Overview

This project is a complete route optimization system for hospital medication delivery in Sao Paulo, Brazil. It solves a realistic Vehicle Routing Problem (VRP) with multiple constraints, generates operational reports with a local LLM, and provides a real-time tracking interface for simulated delivery vehicles.

### Problem Solved

- **Problem type:** Vehicle Routing Problem (VRP) with multiple vehicles
- **Scenario:** Medication delivery to hospitals in Sao Paulo
- **Constraints:** Vehicle capacity, vehicle range, critical delivery priority, and multi-vehicle allocation
- **Optimization method:** Genetic Algorithm with a six-component fitness function
- **AI layer:** Operational reports, driver instructions, route analysis, and analytical chatbot powered by Ollama

## Key Features

### Advanced Optimization

- Specialized Genetic Algorithm for VRP
- Six fitness components: distance, capacity, range, priority, load balancing, and vehicle usage
- Custom genetic operators: Order Crossover and multiple mutation strategies
- Realistic operational constraints: load capacity, vehicle autonomy, and critical deliveries
- Local search refinement with 2-opt and inter-route swap
- Elitism and early stopping for faster convergence

### Artificial Intelligence

- Analytical chatbot powered by Ollama and Llama 3.2
- Automatic daily, weekly, and management reports
- LLM-generated driver instructions
- Data-driven route improvement suggestions
- Natural-language route analysis and contextual Q&A

### Real-Time Tracking

- Mapbox GL JS 3.0 visualization with complete route rendering
- Smooth vehicle movement with 100 ms updates, equivalent to 10 FPS
- Interactive hospital and vehicle markers
- Dynamic popups with live status, speed, destination, and ETA
- Vehicle trails showing the path already traveled
- Toast notifications when vehicles arrive at hospitals
- Simulation speed controls from 0.5x to 10x
- Responsive mobile-first interface

### Professional Interface

- Clean design system using the Inter font and semantic colors
- Slim dashboard header with real-time KPI metrics
- Full route dashboard covering distance, cost, vehicles, deliveries, and critical stops
- Interactive Folium map with optimized route visualization
- Integrated chatbot for conversational route analysis

## Differentiators

This project goes beyond the base requirements with several production-oriented improvements:

| Area | Enhancement |
| --- | --- |
| Real-time tracking | Mapbox GL JS 3.0, 100 ms updates, dynamic popups, vehicle trails, and speed control |
| Load balancing | Additional fitness component to distribute workload more evenly across vehicles |
| Local search | 2-opt and inter-route swap refinements after Genetic Algorithm evolution |
| Interface quality | Professional responsive dashboard with mobile-first behavior |
| Intelligent analysis | RouteAnalyzer module with actionable route improvement recommendations |

## Interactive Demo

### 1. Main Dashboard

```bash
python app_scripts/run_chatbot_interface.py
```

Open:

```text
http://localhost:5000
```

The dashboard includes:

- Five KPI cards: distance, cost, vehicles, deliveries, and critical deliveries
- A **Track** button that opens the live tracking view
- An interactive chatbot for route analysis
- A map with optimized delivery routes

### 2. Live Tracking with Mapbox

Open the tracking page from the dashboard, or open it directly:

```text
interfaces/rastreamento_mapbox.html
```

The tracking interface includes:

- Complete route lines drawn on the map
- Hospital markers with informational popups
- Three simulated vehicles with distinct colors
- Smooth 100 ms vehicle position updates
- Live vehicle popups with status, destination, speed, and ETA
- Vehicle trails showing completed path segments
- Arrival notifications for hospital stops
- Speed control at 0.5x, 1x, 2x, 5x, and 10x
- Responsive layout for mobile devices

### 3. Analytical Chatbot

The chatbot is integrated into the main dashboard. Example questions:

```text
Analyze route efficiency.
Are there any critical deliveries?
What is the total distance?
Suggest route improvements.
Compare the vehicles.
```

## Architecture

The codebase is organized around modular, SOLID-oriented components.

```text
hospital_routes/
|-- core/                         # Base interfaces and shared models
|   |-- interfaces.py             # BaseOptimizer, BaseReporter
|   |-- models.py                 # OptimizationResult, RouteInfo
|   `-- exceptions.py             # Custom exceptions
|
|-- optimization/                 # Optimization engine
|   |-- genetic_algorithm.py      # Genetic Algorithm for VRP
|   |-- local_search.py           # 2-opt and inter-route swap
|   |-- fitness/                  # Fitness components
|   |   |-- composite_fitness.py
|   |   |-- distance_fitness.py
|   |   |-- capacity_penalty.py
|   |   |-- autonomy_penalty.py
|   |   |-- priority_penalty.py
|   |   `-- load_balance_penalty.py
|   `-- strategies/               # Initialization strategies
|
|-- llm/                          # Artificial intelligence layer
|   |-- chatbot.py                # Analytical chatbot using Ollama
|   |-- ollama_reporter.py        # Report generator
|   |-- prompts.py                # Prompt templates
|   `-- route_analyzer.py         # Intelligent route analysis
|
|-- visualization/                # Visualization layer
|   |-- map_generator.py          # Folium maps
|   `-- chatbot_interface_v2.py   # Flask dashboard
|
|-- domain/                       # Domain entities
|   |-- hospital.py
|   |-- vehicle.py
|   |-- delivery.py
|   `-- route.py
|
|-- utils/                        # Utilities
|   |-- distance_calculator.py    # Haversine and OSRM distance calculations
|   `-- data_loader.py            # Data loading helpers
|
|-- interfaces/                   # HTML interfaces
|   |-- chatbot_interface_v2.html # Main dashboard
|   |-- chatbot_interface.html    # Legacy dashboard
|   `-- rastreamento_mapbox.html  # Real-time tracking interface
|
|-- app_scripts/                  # Executable scripts
|   |-- run_chatbot_interface.py  # Flask server
|   |-- seed_real_data.py         # Realistic Sao Paulo data
|   |-- server_chatbot.py         # Chatbot API
|   |-- setup_ollama.py           # Ollama setup helper
|   |-- run_demo.py               # Full demo
|   `-- test_optimization.py      # Optimization tests
|
|-- docs/                         # Project documentation
|-- output/                       # Generated files, usually gitignored
|-- examples/                     # Usage examples
|-- cli.py                        # Command-line interface
|-- requirements.txt              # Python dependencies
`-- README.md
```

### Design Principles

- **SOLID:** Abstract interfaces and dependency injection
- **Strategy Pattern:** Interchangeable optimization strategies
- **Composite Pattern:** Modular fitness function composition
- **Factory Pattern:** Optimizer creation
- **Observer Pattern:** Real-time tracking updates

## Installation

### Prerequisites

- Python 3.10 or higher
- Ollama, required for local LLM features
- A free Mapbox account and access token

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/hospital_routes.git
cd hospital_routes
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux or macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Install Ollama

Download Ollama from:

```text
https://ollama.com/download
```

Then install the Llama 3.2 model:

```bash
ollama pull llama3.2
```

### 4. Configure Mapbox

1. Create a free account at `https://account.mapbox.com/`.
2. Copy your access token.
3. Update the token in `interfaces/rastreamento_mapbox.html`:

```javascript
mapboxgl.accessToken = "YOUR_MAPBOX_TOKEN";
```

## Quick Start

### Option 1: Full Web Interface

```bash
python app_scripts/run_chatbot_interface.py
```

Then open:

```text
http://localhost:5000
```

From the dashboard, you can view optimized routes, open the live tracking simulation, and use the chatbot for route analysis.

### Option 2: Command-Line Interface

```bash
python app_scripts/seed_real_data.py
python cli.py
```

Then open the generated map:

```text
output/route_map.html
```

### Option 3: Programmatic API

```python
from optimization.genetic_algorithm import GeneticAlgorithmOptimizer
from core.interfaces import VehicleConstraints, Delivery
from utils.distance_calculator import HaversineDistanceCalculator

vehicles = [
    VehicleConstraints(id="V1", max_capacity=150, max_range=100, cost_per_km=2.5),
    VehicleConstraints(id="V2", max_capacity=200, max_range=120, cost_per_km=3.0),
]

deliveries = [
    Delivery(
        id="H001",
        hospital_name="Hospital das Clinicas",
        latitude=-23.5646,
        longitude=-46.6708,
        urgency_level=1,
        required_capacity=50,
    ),
]

optimizer = GeneticAlgorithmOptimizer()
result = optimizer.optimize(
    deliveries=deliveries,
    vehicles=vehicles,
    depot_location=(-23.5505, -46.6333),
    distance_calculator=HaversineDistanceCalculator(),
)

print(f"Total distance: {result.total_distance:.2f} km")
print(f"Total cost: R$ {result.total_cost:.2f}")
print(f"Vehicles used: {len(result.routes)}")
```

## Genetic Algorithm

### Genetic Representation

Each individual is represented as a list of vehicle routes:

```python
individual = [
    ["H001", "H003", "H005"],  # Vehicle 1
    ["H002", "H004"],          # Vehicle 2
    ["H006", "H007", "H008"],  # Vehicle 3
]
```

### Fitness Function

The fitness function combines six optimization objectives:

```text
fitness = alpha * distance
        + beta  * capacity_penalty
        + gamma * autonomy_penalty
        + delta * priority_penalty
        + zeta  * load_balance_penalty
        + eps   * vehicle_penalty
```

Default weights:

| Component | Weight | Purpose |
| --- | ---: | --- |
| Distance | 1.0 | Minimize total distance |
| Capacity penalty | 1000.0 | Strongly penalize load capacity violations |
| Autonomy penalty | 1000.0 | Strongly penalize vehicle range violations |
| Priority penalty | 500.0 | Penalize delayed critical deliveries |
| Load balance penalty | 50.0 | Encourage balanced vehicle workload |
| Vehicle penalty | 100.0 | Reduce unnecessary vehicle usage |

### Genetic Operators

| Stage | Method |
| --- | --- |
| Selection | Tournament selection with three individuals |
| Crossover | Order Crossover adapted for VRP |
| Mutation | Swap, insertion, inter-route swap, and route merge |
| Local search | 2-opt and inter-route swap applied to the best individual |

Example configuration:

```python
config = OptimizationConfig(
    population_size=100,
    num_generations=200,
    crossover_rate=0.7,
    mutation_rate=0.2,
    elite_size=5,
    tournament_size=3,
    max_iterations_without_improvement=50,
)
```

## LLM Integration

### Local Chatbot with Ollama

```python
from llm.chatbot import RouteChatbot

chatbot = RouteChatbot(model="llama3.2")
chatbot.set_optimization_context(result, deliveries)

response = chatbot.chat("Are there possible improvements in these routes?")
print(response)
```

### Automatic Reports

```python
from llm.ollama_reporter import OllamaReporter

reporter = OllamaReporter()

instructions = reporter.generate_driver_instructions(result, deliveries, vehicles)
daily = reporter.generate_daily_summary(result, deliveries)
weekly = reporter.generate_weekly_analysis(result, deliveries)
managerial = reporter.generate_managerial_report(result, deliveries, vehicles)
```

### Intelligent Route Analysis

```python
from llm.route_analyzer import RouteAnalyzer

analyzer = RouteAnalyzer()
analysis = analyzer.analyze_route(result, deliveries, vehicles)

print(f"Load distribution: {analysis['load_distribution']}")
print(f"Recommendations: {analysis['recommendations']}")
```

## Real-Time Tracking

The Mapbox tracking interface includes eight professional capabilities:

| Feature | Description |
| --- | --- |
| Route rendering | Planned routes are drawn as LineString layers |
| Hospital markers | Hospital destinations include informative popups |
| Smooth movement | Vehicle positions update every 100 ms |
| Header controls | Simulation speed can be changed from the interface |
| Vehicle popups | Live status, destination, speed, and ETA |
| Vehicle trails | Completed path segments are rendered per vehicle |
| Toast notifications | Arrival alerts are shown with short animations |
| Mobile responsiveness | Layout adapts to smaller screens |

Customization examples:

```javascript
const vehicles = [
  { id: 1, baseSpeed: 45 },
  { id: 2, baseSpeed: 35 },
];

setInterval(updatePositions, 100);
```

## Requirements Compliance

### Requirement 1: Route Optimization with Genetic Algorithms

| Item | Status | Evidence |
| --- | --- | --- |
| TSP/VRP optimization system | Implemented | `optimization/genetic_algorithm.py` |
| Genetic representation | Implemented | DEAP individual as `List[List[str]]` |
| Genetic operators | Implemented | Tournament selection, OX crossover, and four mutations |
| Fitness function | Implemented | Six modular fitness components |
| Priority handling | Implemented | `PriorityPenalty` and critical deliveries |
| Capacity constraints | Implemented | `CapacityPenalty` and `max_capacity` |
| Vehicle autonomy constraints | Implemented | `AutonomyPenalty` and `max_range` |
| Multiple vehicles | Implemented | Complete VRP representation |
| Additional constraints | Implemented | Load balancing and local search |
| Map visualization | Implemented | Folium and Mapbox GL JS |

### Requirement 3: LLM Integration

| Item | Status | Evidence |
| --- | --- | --- |
| Driver instructions | Implemented | `OllamaReporter.generate_driver_instructions()` |
| Daily and weekly reports | Implemented | `generate_daily_summary()` and `generate_weekly_analysis()` |
| Improvement suggestions | Implemented | `RouteChatbot.chat()` and `RouteAnalyzer` |
| Effective prompts | Implemented | `llm/prompts.py` and structured system prompts |
| Natural language interface | Implemented | Web interface, REST API, and Ollama integration |

All mandatory requirements are implemented and functional.

## Documentation

### Main Guides

- `docs/VERIFICACAO_REQUISITOS.md` - Detailed requirements compliance
- `docs/ARCHITECTURE.md` - Full architecture description
- `docs/PROJECT_STRUCTURE.md` - Folder structure
- `docs/UX_HEADER_REDESIGN.md` - Design system and header redesign

### Quick Guides

- `docs/GUIA_RAPIDO_CHATBOT.md` - Chatbot quick start
- `docs/COMO_USAR_CHATBOT.md` - Complete chatbot tutorial
- `docs/COMO_RESOLVER_OLLAMA.md` - Ollama troubleshooting
- `docs/INSTALACAO_FLASK.md` - Flask setup

### Implemented Improvements

- `docs/MELHORIAS_ALGORITMO.md` - Genetic Algorithm improvements
- `docs/MELHORIAS_CHATBOT.md` - LLM analysis improvements
- `docs/MELHORIAS_SENIOR.md` - Senior engineering practices
- `docs/UX_HEADER_REDESIGN.md` - Professional UI improvements

## Technology Stack

### Backend

- Python 3.10+
- DEAP for evolutionary algorithms
- Flask for the REST API and web server
- Ollama with Llama 3.2 for local LLM features

### Frontend

- HTML5, CSS3, and modern JavaScript
- Mapbox GL JS 3.0 for interactive maps
- Folium for static route maps
- Inter font for interface typography

### Python Libraries

- `deap` for evolutionary algorithms
- `folium` for Leaflet-based maps
- `requests` for HTTP calls
- `flask` and `flask-cors` for the API
- `python-dotenv` for configuration

## Usage Examples

### Basic Optimization

```bash
python cli.py
```

### Full Dashboard

```bash
python app_scripts/run_chatbot_interface.py
```

Open:

```text
http://localhost:5000
```

### Direct Tracking View

Open the following file in a browser:

```text
interfaces/rastreamento_mapbox.html
```

You can also open it by clicking **Track** in the dashboard.

### Chatbot API

```python
import requests

response = requests.post(
    "http://localhost:5000/api/chat",
    json={"message": "Analyze route efficiency"},
)

print(response.json()["response"])
```

## Contributing

Contributions are welcome.

1. Fork the project.
2. Create a feature branch:

   ```bash
   git checkout -b feature/amazing-feature
   ```

3. Commit your changes:

   ```bash
   git commit -m "Add amazing feature"
   ```

4. Push to your branch:

   ```bash
   git push origin feature/amazing-feature
   ```

5. Open a Pull Request.
