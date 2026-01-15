# 💬 Como Usar o Chatbot para Operadores

Guia prático para usar o chatbot do sistema de otimização de rotas.

## 🚀 Formas de Usar

### 1. **Chatbot Interativo** (Recomendado para começar)

Execute o script interativo:

```bash
python examples/chatbot_interactive.py
```

**O que acontece:**
1. ✅ Carrega dados de hospitais
2. ✅ Executa otimização automaticamente
3. ✅ Inicializa o chatbot
4. ✅ Abre interface interativa para você fazer perguntas

**Exemplo de uso:**
```
Você: Quantos veículos foram usados?
🤖 Assistente: Foram utilizados 3 veículos na otimização...

Você: Há entregas críticas?
🤖 Assistente: Sim, há 5 entregas críticas distribuídas...
```

---

### 2. **No Script run_demo.py** (Automático)

O `run_demo.py` já inclui um exemplo do chatbot:

```bash
python run_demo.py
```

No final, você verá:
- ✅ Exemplo de análise inteligente
- ✅ Teste do chatbot com uma pergunta de exemplo

---

### 3. **Uso Programático** (No seu código)

```python
from hospital_routes.llm.chatbot import RouteChatbot
from hospital_routes.optimization.genetic_algorithm import GeneticAlgorithmOptimizer
from seed_real_data import (
    generate_deliveries,
    generate_vehicles,
    get_optimization_config,
    get_depot_location,
)

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

# 2. Inicializar chatbot
chatbot = RouteChatbot()  # Auto-detecta modelo
chatbot.set_optimization_context(result)

# 3. Fazer perguntas
resposta = chatbot.chat("Quantos veículos foram usados?")
print(resposta)
```

---

## 💡 Perguntas que Você Pode Fazer

### Sobre Rotas
- "Quantos veículos foram usados?"
- "Qual a distância total percorrida?"
- "Descreva as rotas otimizadas"
- "Quais são as rotas de cada veículo?"

### Sobre Entregas
- "Há entregas críticas nas rotas?"
- "Quantas entregas críticas temos?"
- "Qual veículo tem mais entregas?"
- "Quais hospitais serão visitados?"

### Sobre Performance
- "A solução é eficiente?"
- "Há violações de restrições?"
- "Qual o custo total?"
- "Quanto tempo levou para otimizar?"

### Análise e Sugestões
- "Analise a eficiência das rotas"
- "Há alguma melhoria possível?"
- "Compare os veículos"
- "Quais são os pontos fortes da solução?"

---

## 🎮 Comandos Especiais (Chatbot Interativo)

Quando usar o chatbot interativo, você tem comandos especiais:

- `/help` - Mostra ajuda e exemplos
- `/clear` - Limpa o histórico de conversa
- `/history` - Mostra últimas mensagens
- `/quit` ou `/exit` - Sair do chatbot

---

## 📝 Exemplos Práticos

### Exemplo 1: Verificar Rotas

```python
chatbot = RouteChatbot()
chatbot.set_optimization_context(result)

pergunta = "Quantos veículos foram usados e qual a distância total?"
resposta = chatbot.chat(pergunta)
print(resposta)
```

**Resposta esperada:**
```
Foram utilizados 3 veículos na otimização. A distância total percorrida 
é de aproximadamente 85.15 km, distribuída entre os veículos de forma 
eficiente para minimizar custos e tempo de entrega.
```

### Exemplo 2: Verificar Entregas Críticas

```python
resposta = chatbot.chat("Há entregas críticas? Quais são?")
print(resposta)
```

### Exemplo 3: Análise Completa

```python
resposta = chatbot.chat("Analise a eficiência das rotas e sugira melhorias")
print(resposta)
```

---

## 🔧 Configuração Avançada

### Usar Modelo Específico

```python
# Especificar modelo manualmente
chatbot = RouteChatbot(model_name="llama3.1")
```

### Ajustar Temperatura (Criatividade)

```python
# Mais criativo (0.9) ou mais conservador (0.3)
chatbot = RouteChatbot(temperature=0.7)
```

### Limpar Histórico

```python
chatbot.clear_history()  # Limpa conversa anterior
```

---

## 🎯 Casos de Uso Reais

### 1. Operador Verificando Rotas do Dia

```python
chatbot.chat("Resuma as rotas de hoje")
chatbot.chat("Há alguma entrega crítica que precisa de atenção?")
chatbot.chat("Qual veículo tem a rota mais longa?")
```

### 2. Supervisor Analisando Performance

```python
chatbot.chat("A solução está eficiente?")
chatbot.chat("Compare a eficiência dos veículos")
chatbot.chat("Há melhorias possíveis?")
```

### 3. Planejamento

```python
chatbot.chat("Quantas entregas cada veículo fará?")
chatbot.chat("Qual o tempo estimado total?")
chatbot.chat("Há restrições violadas?")
```

---

## 🐛 Troubleshooting

### Erro: "Nenhum modelo disponível"

**Solução:**
```bash
ollama pull llama3.2
```

### Erro: "Ollama não está rodando"

**Solução:**
- Verifique se o Ollama está instalado
- Inicie o Ollama (geralmente inicia automaticamente)

### Respostas lentas

**Solução:**
- Use modelo menor: `llama3.2` ao invés de `llama3`
- Reduza `num_predict` no construtor

---

## 📚 Mais Informações

- Documentação completa: `docs/CHATBOT_ANALISE.md`
- Exemplo interativo: `examples/chatbot_interactive.py`
- Código fonte: `llm/chatbot.py`

---

**Divirta-se usando o chatbot! 🤖💬**
