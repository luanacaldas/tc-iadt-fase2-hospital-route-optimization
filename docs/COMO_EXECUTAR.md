# 🚀 Como Executar o Projeto

Este guia mostra como visualizar e executar o sistema de otimização de rotas hospitalares.

## 📋 Pré-requisitos

Certifique-se de ter instalado:

- Python 3.8+
- Dependências do projeto (instaladas automaticamente ou via `pip install -r requirements.txt`)

## 🎯 Formas de Executar

### 1. **Demonstração Completa (Recomendado)** 🎬

Execute o script completo que mostra tudo:

- Otimização de rotas
- Mapa interativo HTML
- Relatório (se Ollama estiver disponível)

```bash
python run_demo.py
```

**O que acontece:**

1. ✅ Carrega dados reais de 12 hospitais de São Paulo
2. ✅ Executa otimização genética
3. ✅ Gera mapa interativo HTML
4. ✅ Abre o mapa automaticamente no navegador
5. ✅ (Opcional) Gera relatório com Ollama

**Arquivos gerados:**

- `route_map.html` - Mapa interativo (abre automaticamente)
- `driver_instructions.txt` - Relatório (se Ollama estiver disponível)

---

### 2. **Teste Básico** 🧪

Teste rápido com dados simples:

```bash
python test_optimization.py
```

Mostra resultados no terminal apenas.

---

### 3. **Com Dados Reais de Hospitais** 🏥

Use os dados reais de hospitais de SP:

```bash
python seed_real_data.py
```

Mostra informações sobre os hospitais disponíveis.

---

## 🗺️ Visualizando o Mapa

Após executar `run_demo.py`, o mapa HTML será aberto automaticamente no seu navegador.

**Recursos do mapa:**

- 🗺️ **Zoom**: Use o mouse ou os controles
- 📍 **Marcadores**: Clique para ver informações
- 🚚 **Rotas**: Linhas coloridas mostram o caminho de cada veículo
- ⭐ **Depósito**: Estrela azul marca o ponto de partida
- 🔴 **Críticas**: Marcadores vermelhos = entregas críticas (medicamentos)
- 🔵 **Normais**: Marcadores azuis = entregas normais (insumos)

**Cores das rotas:**

- Cada veículo tem uma cor diferente
- A legenda mostra qual cor pertence a qual veículo

---

## 📊 Entendendo os Resultados

### No Terminal

Você verá:

- **Distância total**: Soma de todas as rotas em km
- **Custo total**: Custo estimado em R$
- **Tempo de execução**: Quanto tempo levou para otimizar
- **Gerações**: Quantas gerações o algoritmo genético executou
- **Fitness**: Quanto menor, melhor (medida de qualidade)
- **Veículos usados**: Quantos veículos foram necessários

### No Mapa

- **Linhas coloridas**: Rotas de cada veículo
- **Marcadores**: Pontos de entrega
- **Popups**: Clique nos marcadores para ver detalhes

---

## 🔧 Configurações

### Alterar Dados de Entrada

Edite `seed_real_data.py` para:

- Adicionar mais hospitais
- Modificar entregas
- Ajustar veículos

### Ajustar Algoritmo

No `run_demo.py`, você pode modificar:

```python
config = get_optimization_config()
# Ajuste aqui:
config.generations = 100  # Mais gerações = melhor resultado, mais lento
config.population_size = 50  # Mais indivíduos = melhor, mais lento
```

---

## 🐛 Solução de Problemas

### Erro: "Folium não encontrado"

```bash
pip install folium
```

### Erro: "Módulo não encontrado"

Certifique-se de estar na raiz do projeto:

```bash
cd E:\hospital_routes
python run_demo.py
```

### Mapa não abre automaticamente

Abra manualmente o arquivo `route_map.html` no navegador.

### Ollama não funciona

- Instale: `pip install ollama`
- Baixe um modelo: `ollama pull llama3.2`
- Certifique-se de que o Ollama está rodando

---

## 📁 Estrutura de Arquivos Gerados

```
hospital_routes/
├── route_map.html          # Mapa interativo (gerado)
├── driver_instructions.txt # Relatório (se Ollama disponível)
└── ...
```

---

## 💡 Dicas

1. **Primeira execução**: Use `run_demo.py` para ver tudo funcionando
2. **Testes rápidos**: Use `test_optimization.py` para testes simples
3. **Dados reais**: Use `seed_real_data.py` para ver os hospitais disponíveis
4. **Mapa interativo**: Explore o mapa HTML - é totalmente interativo!
5. **Relatórios**: Se tiver Ollama, os relatórios são gerados automaticamente

---

## 🎓 Próximos Passos

1. ✅ Execute `python run_demo.py` para ver tudo funcionando
2. 📊 Explore o mapa interativo
3. 🔧 Experimente modificar os dados em `seed_real_data.py`
4. 📝 (Opcional) Configure Ollama para gerar relatórios
5. 🚀 Integre com seu próprio sistema!

---

**Divirta-se explorando o sistema! 🎉**
