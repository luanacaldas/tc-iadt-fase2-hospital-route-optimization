# Configuração do Ollama para Geração de Relatórios

Este guia explica como configurar e usar o Ollama para gerar relatórios localmente, sem necessidade de API keys pagas.

## O que é Ollama?

Ollama é uma ferramenta que permite executar modelos de LLM (Large Language Models) localmente no seu computador. Isso significa que você pode gerar relatórios sem depender de serviços pagos como OpenAI.

## Instalação

### 1. Instalar o Ollama

**Windows:**
- Baixe o instalador em: https://ollama.ai/download
- Execute o instalador e siga as instruções

**Linux/Mac:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Baixar um Modelo

Após instalar o Ollama, você precisa baixar um modelo. Modelos recomendados:

```bash
# Modelo pequeno e rápido (recomendado para começar)
ollama pull llama3.2

# Modelo médio (melhor qualidade)
ollama pull llama3.1

# Modelo grande (melhor qualidade, mais lento)
ollama pull llama3

# Alternativas
ollama pull mistral
ollama pull phi3
```

### 3. Instalar Dependências Python

Você tem duas opções:

**Opção 1: Usar biblioteca direta do Ollama (recomendado)**
```bash
pip install ollama
```

**Opção 2: Usar LangChain (mais recursos, mas mais pesado)**
```bash
pip install langchain-ollama
```

## Uso Básico

### Exemplo 1: Uso Simples

```python
from hospital_routes.llm.ollama_reporter import OllamaReporter
from hospital_routes.core.interfaces import ReportRequest, ReportType

# Inicializar o reporter
reporter = OllamaReporter(
    model_name="llama3.2",  # Nome do modelo que você baixou
    temperature=0.7,
    num_predict=2000,
)

# Gerar relatório
request = ReportRequest(
    optimization_result=resultado_otimizacao,
    report_type=ReportType.DRIVER_INSTRUCTIONS,
    language="pt-BR",
)

report = reporter.generate_report(request)
print(report.content)
```

### Exemplo 2: Com Dados Reais

```python
from hospital_routes.llm.ollama_reporter import OllamaReporter
from hospital_routes.optimization.genetic_algorithm import GeneticAlgorithmOptimizer
from seed_real_data import (
    generate_deliveries,
    generate_vehicles,
    get_optimization_config,
    get_depot_location,
)
from hospital_routes.core.interfaces import ReportRequest, ReportType

# 1. Otimizar rotas
deliveries = generate_deliveries()
vehicles = generate_vehicles()
config = get_optimization_config()
depot = get_depot_location()

optimizer = GeneticAlgorithmOptimizer()
result = optimizer.optimize(
    deliveries=deliveries,
    vehicles=vehicles,
    config=config,
    depot_location=depot,
)

# 2. Adicionar entregas aos metadados (para o relatório)
result.solution.metadata["deliveries"] = deliveries

# 3. Gerar relatório com Ollama
reporter = OllamaReporter(model_name="llama3.2")
request = ReportRequest(
    optimization_result=result,
    report_type=ReportType.DRIVER_INSTRUCTIONS,
    language="pt-BR",
)

report = reporter.generate_report(request)
print(report.content)
```

## Configuração Avançada

### Parâmetros do OllamaReporter

```python
reporter = OllamaReporter(
    model_name="llama3.2",        # Nome do modelo
    base_url="http://localhost:11434",  # URL do Ollama (padrão)
    temperature=0.7,               # Criatividade (0.0-2.0)
    num_predict=2000,               # Máximo de tokens a gerar
)
```

### Verificar Modelos Disponíveis

```python
import ollama

models = ollama.list()
for model in models['models']:
    print(f"- {model['name']}")
```

## Solução de Problemas

### Erro: "Ollama não está disponível"

**Solução:** Instale uma das dependências:
```bash
pip install ollama
# OU
pip install langchain-ollama
```

### Erro: "Modelo não encontrado"

**Solução:** Baixe o modelo primeiro:
```bash
ollama pull llama3.2
```

### Erro: "Erro ao conectar com Ollama"

**Solução:** Certifique-se de que o Ollama está rodando:
- Windows: Verifique se o serviço está ativo
- Linux/Mac: Execute `ollama serve` em um terminal

### Modelo muito lento

**Soluções:**
1. Use um modelo menor (ex: `llama3.2` ao invés de `llama3`)
2. Reduza `num_predict` para gerar menos texto
3. Use uma GPU se disponível (Ollama detecta automaticamente)

## Comparação: OpenAI vs Ollama

| Característica | OpenAI | Ollama |
|---------------|--------|--------|
| Custo | Pago (por token) | Gratuito |
| Requer Internet | Sim | Não |
| Privacidade | Dados enviados para servidor | 100% local |
| Velocidade | Rápida | Depende do hardware |
| Qualidade | Excelente | Boa (depende do modelo) |
| Requer API Key | Sim | Não |

## Modelos Recomendados

- **llama3.2** (2B parâmetros): Rápido, bom para testes
- **llama3.1** (8B parâmetros): Equilíbrio entre velocidade e qualidade
- **llama3** (70B parâmetros): Melhor qualidade, requer mais RAM/GPU
- **mistral**: Alternativa leve e eficiente
- **phi3**: Modelo pequeno mas eficiente

## Próximos Passos

1. Teste o exemplo: `python examples/test_ollama_reporter.py`
2. Experimente diferentes modelos
3. Ajuste os parâmetros `temperature` e `num_predict` conforme necessário
4. Integre com seu fluxo de trabalho

## Recursos Adicionais

- Documentação do Ollama: https://ollama.ai/docs
- Lista de modelos: https://ollama.ai/library
- GitHub: https://github.com/ollama/ollama

