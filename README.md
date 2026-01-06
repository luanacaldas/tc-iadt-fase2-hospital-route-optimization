# 🏥 Hospital Route Optimization System

Sistema de otimização de rotas hospitalares usando Algoritmos Genéticos e LLMs para geração de relatórios operacionais.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Poetry](https://img.shields.io/badge/Poetry-Latest-cyan.svg)](https://python-poetry.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 Objetivo

Resolver o problema de distribuição de medicamentos (Vehicle Routing Problem - VRP) usando múltiplas abordagens de otimização (Genetic Algorithm, Greedy, Simulated Annealing) com comparativo de desempenho, e usar LLMs para gerar relatórios operacionais.

## 🏗️ Arquitetura

O projeto segue princípios SOLID e é organizado em módulos desacoplados:

- **Core**: Interfaces abstratas e modelos de dados
- **Optimization**: Motor de otimização com algoritmos genéticos
- **LLM**: Geradores de relatórios baseados em LLM
- **Domain**: Entidades de domínio (Veículo, Entrega, Rota)
- **Visualization**: Visualização de rotas em mapas interativos

## 📋 Requisitos

- Python 3.10+
- Poetry (gerenciador de pacotes)

## 🚀 Instalação

```bash
# Instalar Poetry (se ainda não tiver)
curl -sSL https://install.python-poetry.org | python3 -

# Instalar dependências
poetry install

# Ativar ambiente virtual
poetry shell
```

## 📦 Estrutura do Projeto

Ver `PROJECT_STRUCTURE.md` para detalhes completos da estrutura de pastas.

## 🔧 Configuração

1. Copie `.env.example` para `.env`
2. Configure suas chaves de API (OpenAI, etc.)

```bash
cp .env.example .env
```

## 📚 Documentação

- **Arquitetura**: Ver `ARCHITECTURE.md`
- **Estrutura**: Ver `PROJECT_STRUCTURE.md`

## 🧪 Testes

```bash
poetry run pytest
```

## 🚀 Início Rápido

```bash
# 1. Instalar dependências
poetry install
poetry shell

# 2. Gerar dados de teste
python seed_data.py

# 3. Executar exemplo completo
python examples/test_with_seed_data.py

# 4. Comparar algoritmos (NOVO!)
python examples/benchmark_comparison.py

# 5. Abrir mapa gerado no navegador
# route_map_seed_data.html
```

## 🔬 Comparativo de Algoritmos

O projeto implementa **3 algoritmos de otimização** com módulo de benchmark:

- **Genetic Algorithm**: Meta-heurística evolutiva (melhor qualidade)
- **Greedy (Nearest Neighbor)**: Heurística gulosa (mais rápido)
- **Simulated Annealing**: Meta-heurística baseada em física (balance)

Ver `BENCHMARK_COMPARISON.md` para detalhes completos.
