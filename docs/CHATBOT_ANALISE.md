# 🤖 Chatbot e Análise Inteligente de Rotas

Este documento explica como usar o chatbot para operadores e a análise inteligente de rotas.

## 📋 Visão Geral

O sistema oferece duas funcionalidades principais:

1. **Chatbot para Operadores**: Interface conversacional para fazer perguntas sobre rotas
2. **Análise Inteligente**: Análise profunda e automática das rotas otimizadas

## 🚀 Configuração do Ollama

### 1. Instalar Ollama

Baixe e instale o Ollama: https://ollama.ai/

### 2. Baixar um Modelo

```bash
# Modelo recomendado (pequeno e rápido)
ollama pull llama3.2

# Ou modelos alternativos
ollama pull llama3.1
ollama pull mistral
ollama pull phi3
```

### 3. Verificar Modelos Disponíveis

```python
from hospital_routes.llm.ollama_helper import list_available_models

models = list_available_models()
print(f"Modelos disponíveis: {models}")
```

## 💬 Chatbot para Operadores

### Uso Básico

```python
from hospital_routes.llm.chatbot import RouteChatbot
from hospital_routes.optimization.genetic_algorithm import GeneticAlgorithmOptimizer

# 1. Otimizar rotas
optimizer = GeneticAlgorithmOptimizer()
result = optimizer.optimize(...)

# 2. Inicializar chatbot
chatbot = RouteChatbot()  # Auto-detecta modelo
chatbot.set_optimization_context(result)

# 3. Fazer perguntas
resposta = chatbot.chat("Quantos veículos foram usados?")
print(resposta)
```

### Exemplo Interativo

Execute o exemplo interativo:

```bash
python examples/chatbot_interactive.py
```

### Perguntas que Você Pode Fazer

- **Sobre Rotas:**
  - "Quantos veículos foram usados?"
  - "Qual a distância total percorrida?"
  - "Quais são as rotas otimizadas?"
  
- **Sobre Entregas:**
  - "Há entregas críticas nas rotas?"
  - "Quantas entregas críticas temos?"
  - "Qual veículo leva mais entregas?"
  
- **Sobre Performance:**
  - "A solução é eficiente?"
  - "Há violações de restrições?"
  - "Qual o custo total?"
  
- **Análise:**
  - "Analise a eficiência das rotas"
  - "Há alguma melhoria possível?"
  - "Compare as rotas dos veículos"

### Comandos Especiais

- `/help` - Mostrar ajuda
- `/clear` - Limpar histórico
- `/history` - Ver histórico de conversa
- `/quit` ou `/exit` - Sair

## 📊 Análise Inteligente de Rotas

### Uso Básico

```python
from hospital_routes.llm.chatbot import RouteAnalyzer

# Inicializar analisador
analyzer = RouteAnalyzer()  # Auto-detecta modelo

# Analisar rotas
analysis = analyzer.analyze_route(
    optimization_result=result,
    deliveries=deliveries,
    accident_provider=accident_provider,  # Opcional
)

# Acessar resultados
print(analysis["summary"])  # Análise textual
print(analysis["recommendations"])  # Lista de recomendações
```

### O que a Análise Inclui

1. **Avaliação Geral**: Visão geral da solução
2. **Pontos Fortes**: O que está funcionando bem
3. **Pontos de Atenção**: Áreas que precisam de atenção
4. **Eficiência**: Uso de veículos e recursos
5. **Distribuição**: Como entregas críticas estão distribuídas
6. **Segurança**: Análise de segurança das rotas (se dados de acidentes disponíveis)
7. **Recomendações**: Sugestões práticas e acionáveis

### Exemplo Completo

```python
from hospital_routes.llm.chatbot import RouteAnalyzer
from hospital_routes.utils.accident_data import create_sample_accident_data

# Carregar dados de acidentes
accident_provider = create_sample_accident_data()

# Analisar
analyzer = RouteAnalyzer()
analysis = analyzer.analyze_route(
    result,
    deliveries,
    accident_provider=accident_provider,
)

# Exibir resultados
print("=" * 70)
print("ANÁLISE INTELIGENTE")
print("=" * 70)
print(analysis["summary"])
print()
print("RECOMENDAÇÕES:")
for i, rec in enumerate(analysis["recommendations"], 1):
    print(f"{i}. {rec}")
```

## 🔧 Auto-Detecção de Modelos

O sistema agora detecta automaticamente modelos disponíveis:

```python
from hospital_routes.llm.ollama_helper import get_best_available_model

# Retorna o melhor modelo disponível
model = get_best_available_model()
print(f"Usando modelo: {model}")
```

### Ordem de Prioridade

1. `llama3.2` (recomendado)
2. `llama3.1`
3. `llama3`
4. `mistral`
5. `phi3`
6. `gemma2`
7. Qualquer outro modelo disponível

## 🎯 Casos de Uso

### 1. Operador Fazendo Perguntas

```python
chatbot = RouteChatbot()
chatbot.set_optimization_context(result)

# Pergunta do operador
resposta = chatbot.chat("O veículo 1 está sobrecarregado?")
print(resposta)
```

### 2. Análise Automática Após Otimização

```python
# Após otimizar
analyzer = RouteAnalyzer()
analysis = analyzer.analyze_route(result, deliveries)

# Salvar análise
with open("analise.txt", "w") as f:
    f.write(analysis["summary"])
```

### 3. Dashboard Interativo

```python
# Criar interface que permite:
# - Ver rotas
# - Fazer perguntas ao chatbot
# - Ver análise inteligente
# - Obter recomendações
```

## 💡 Dicas

1. **Modelo Recomendado**: Use `llama3.2` para melhor balanceamento de velocidade/qualidade
2. **Contexto**: Sempre defina o contexto antes de usar o chatbot
3. **Histórico**: O chatbot mantém histórico para contexto conversacional
4. **Análise**: Execute análise após cada otimização importante

## 🐛 Troubleshooting

### "Nenhum modelo disponível"

```bash
# Instalar modelo
ollama pull llama3.2
```

### "Ollama não está rodando"

Certifique-se de que o Ollama está instalado e rodando:
- Windows: Verifique se o serviço está ativo
- Linux/Mac: Execute `ollama serve` em um terminal

### Respostas lentas

- Use modelos menores (llama3.2 ao invés de llama3)
- Reduza `num_predict` para respostas mais curtas
- Use GPU se disponível (Ollama detecta automaticamente)

## 📝 Exemplos de Respostas

### Pergunta: "Quantos veículos foram usados?"

**Resposta:**
```
Foram utilizados 3 veículos na otimização. Cada veículo foi responsável por 
distribuir as entregas de forma eficiente, respeitando as restrições de 
capacidade e autonomia.
```

### Pergunta: "Há entregas críticas?"

**Resposta:**
```
Sim, há 5 entregas críticas (medicamentos) distribuídas entre os veículos:
- Veículo 1: 2 entregas críticas
- Veículo 2: 2 entregas críticas  
- Veículo 3: 1 entrega crítica

Todas as entregas críticas foram priorizadas e estão nas rotas otimizadas.
```

---

**Desenvolvido para tornar o sistema mais inteligente e acessível! 🚀🤖**
