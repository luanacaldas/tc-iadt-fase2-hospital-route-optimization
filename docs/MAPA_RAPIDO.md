# 🗺️ Mapa Rápido do Projeto

> Encontre rapidamente o que você precisa!

## 🎯 Quer Executar?

| O que você quer fazer? | Comando                                |
| ---------------------- | -------------------------------------- |
| 🎨 **Abrir Dashboard** | `python app_scripts/open_interface.py` |
| 🖥️ **CLI Simples**     | `python cli.py`                        |
| 🌱 **Gerar Dados**     | `python app_scripts/seed_real_data.py` |
| 📍 **Rastreamento**    | Clicar em "Rastrear" no dashboard      |
| 🤖 **API Chatbot**     | `python app_scripts/server_chatbot.py` |

---

## 📚 Precisa de Ajuda?

| Dúvida                | Documento                                                   |
| --------------------- | ----------------------------------------------------------- |
| Como executar?        | [docs/COMO_EXECUTAR.md](COMO_EXECUTAR.md)                   |
| Chatbot não funciona? | [docs/COMO_RESOLVER_OLLAMA.md](COMO_RESOLVER_OLLAMA.md)     |
| Como usar chatbot?    | [docs/COMO_USAR_CHATBOT.md](COMO_USAR_CHATBOT.md)           |
| Guia rápido?          | [docs/GUIA_RAPIDO_CHATBOT.md](GUIA_RAPIDO_CHATBOT.md)       |
| Design system?        | [docs/UX_HEADER_REDESIGN.md](UX_HEADER_REDESIGN.md)         |
| Requisitos atendidos? | [docs/VERIFICACAO_REQUISITOS.md](VERIFICACAO_REQUISITOS.md) |

---

## 🔧 Onde Está o Código?

| Módulo                  | Localização                            | O que faz                       |
| ----------------------- | -------------------------------------- | ------------------------------- |
| **Algoritmo Genético**  | `optimization/genetic_algorithm.py`    | VRP com 6 componentes fitness   |
| **Chatbot**             | `llm/chatbot.py`                       | Análise conversacional (Ollama) |
| **Relatórios LLM**      | `llm/ollama_reporter.py`               | Instruções, relatórios          |
| **Mapa Folium**         | `visualization/map_generator.py`       | Gera route_map.html             |
| **Interface Dashboard** | `interfaces/chatbot_interface_v2.html` | Dashboard principal             |
| **Rastreamento**        | `interfaces/rastreamento_mapbox.html`  | MapBox tempo real               |

---

## 📁 Estrutura Visual

```
📦 hospital_routes
│
├── 🎯 ESSENCIAIS (raiz)
│   ├── cli.py              → Interface linha de comando
│   ├── README.md           → Documentação principal
│   └── requirements.txt    → Dependências
│
├── 💻 CÓDIGO FONTE
│   ├── core/               → Interfaces abstratas
│   ├── optimization/       → Algoritmo genético VRP
│   ├── llm/                → Chatbot + LLMs
│   ├── visualization/      → Geradores de mapa
│   ├── domain/             → Entidades (Hospital, Vehicle)
│   └── utils/              → Utilitários
│
├── 🎨 INTERFACES WEB
│   ├── interfaces/         → HTMLs organizados
│   │   ├── chatbot_interface_v2.html  ⭐
│   │   └── rastreamento_mapbox.html   🗺️
│   └── README.md
│
├── 🚀 EXECUTÁVEIS
│   ├── app_scripts/        → Scripts Python
│   │   ├── run_chatbot_interface.py  ⭐
│   │   ├── seed_real_data.py
│   │   └── server_chatbot.py
│   └── README.md
│
├── 📚 DOCUMENTAÇÃO
│   ├── docs/               → Guias e tutoriais
│   │   ├── COMO_EXECUTAR.md
│   │   ├── GUIA_RAPIDO_CHATBOT.md
│   │   └── VERIFICACAO_REQUISITOS.md
│   └── 13 arquivos .md
│
└── 📤 OUTPUTS GERADOS
    └── output/             → Mapas, relatórios (gitignored)
        ├── route_map.html
        └── driver_instructions.txt
```

---

## 🏃 Fluxo de Trabalho Típico

### 1️⃣ Primeira Execução

```bash
# 1. Gerar dados realistas
python app_scripts/seed_real_data.py

# 2. Abrir dashboard
python app_scripts/run_chatbot_interface.py

# 3. Navegar para http://localhost:5000
```

### 2️⃣ Uso Diário

```bash
# Abrir interface
python app_scripts/run_chatbot_interface.py

# No navegador:
# - Ver rotas otimizadas no mapa
# - Conversar com chatbot
# - Clicar em "Rastrear" → rastreamento ao vivo
```

### 3️⃣ Desenvolvimento

```bash
# CLI para testes rápidos
python cli.py

# Verificar outputs gerados
ls output/
```

---

## 🎨 Interfaces Disponíveis

### Dashboard Principal ⭐

**Arquivo:** `interfaces/chatbot_interface_v2.html`  
**Como abrir:** `python app_scripts/run_chatbot_interface.py`  
**Funcionalidades:**

- ✅ Header com 5 KPIs
- ✅ Chatbot integrado
- ✅ Mapa Folium
- ✅ Botão "Rastrear"

### Rastreamento ao Vivo 🗺️

**Arquivo:** `interfaces/rastreamento_mapbox.html`  
**Como abrir:** Clicar em "Rastrear" no dashboard  
**Funcionalidades:**

- ✅ MapBox GL JS 3.0
- ✅ 3 veículos simulados
- ✅ Movimento suave 100ms
- ✅ Popups tempo real
- ✅ Notificações chegada
- ✅ Controle velocidade

---

## 🤖 LLM/Chatbot

### Ollama (Local)

```bash
# Verificar se está rodando
ollama list

# Iniciar (se necessário)
ollama serve

# Usar modelo
ollama run llama3.2
```

### Chatbot no Dashboard

1. Abrir dashboard
2. Perguntar: "Analise a eficiência"
3. Obter respostas baseadas em dados reais

---

## ⚙️ Configurações

### MapBox Token

**Arquivo:** `interfaces/rastreamento_mapbox.html` (linha ~650)

```javascript
mapboxgl.accessToken = "pk.eyJ1...";
```

### Ollama Model

**Arquivo:** `llm/chatbot.py`

```python
model = "llama3.2"  # ou outro modelo
```

---

## 📊 Métricas Rápidas

| Métrica             | Valor        |
| ------------------- | ------------ |
| Módulos Python      | 7 principais |
| Interfaces HTML     | 3            |
| Scripts Executáveis | 7            |
| Arquivos Docs       | 13+          |
| Linhas de Código    | ~5000+       |
| Componentes Fitness | 6            |

---

## 🆘 Resolução Rápida

| Problema            | Solução                                                 |
| ------------------- | ------------------------------------------------------- |
| Ollama não funciona | [docs/COMO_RESOLVER_OLLAMA.md](COMO_RESOLVER_OLLAMA.md) |
| Flask erro          | [docs/SOLUCAO_FLASK.md](SOLUCAO_FLASK.md)               |
| Imports quebrados   | Rodar de dentro da pasta raiz                           |
| MapBox não aparece  | Verificar token (linha 650)                             |

---

## 🎉 Atalhos Úteis

```bash
# Estrutura resumida
tree /F /A

# Rodar interface
python app_scripts/run_chatbot_interface.py

# Ver outputs gerados
dir output

# Ler docs principais
code docs/COMO_EXECUTAR.md

# Ver código principal
code optimization/genetic_algorithm.py
```

---

<div align="center">

**[⬆ README Principal](../README.md)** | **[📚 Todas as Docs](./)**

Navegação rápida para iniciar!

</div>
