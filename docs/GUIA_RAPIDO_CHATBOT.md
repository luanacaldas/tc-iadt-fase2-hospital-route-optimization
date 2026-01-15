# 💬 Guia Rápido: Como Usar o Chatbot

## 🚀 Forma Mais Simples (Recomendada)

Execute o chatbot interativo:

```bash
python examples/chatbot_interactive.py
```

**O que acontece:**
1. ✅ Carrega dados automaticamente
2. ✅ Otimiza rotas
3. ✅ Abre chat interativo
4. ✅ Você faz perguntas e recebe respostas!

---

## 💡 Exemplos de Perguntas

### Perguntas Básicas
```
Você: Quantos veículos foram usados?
Você: Qual a distância total?
Você: Há entregas críticas?
```

### Perguntas de Análise
```
Você: Analise a eficiência das rotas
Você: Há melhorias possíveis?
Você: Compare os veículos
```

### Perguntas Específicas
```
Você: Qual veículo tem mais entregas?
Você: Quais hospitais serão visitados?
Você: Há violações de restrições?
```

---

## 🎮 Comandos Especiais

No chatbot interativo, você pode usar:

- `/help` - Ver exemplos de perguntas
- `/clear` - Limpar histórico
- `/history` - Ver últimas mensagens
- `/quit` - Sair

---

## 📝 Uso no Seu Código

```python
from hospital_routes.llm.chatbot import RouteChatbot

# 1. Criar chatbot
chatbot = RouteChatbot()

# 2. Definir contexto (resultado da otimização)
chatbot.set_optimization_context(resultado_otimizacao)

# 3. Fazer perguntas
resposta = chatbot.chat("Sua pergunta aqui")
print(resposta)
```

---

## 🎯 Exemplo Completo

```python
from hospital_routes.llm.chatbot import RouteChatbot
from hospital_routes.optimization.genetic_algorithm import GeneticAlgorithmOptimizer
from seed_real_data import *

# Otimizar
deliveries = generate_deliveries()
vehicles = generate_vehicles()
config = get_optimization_config()
depot = get_depot_location()

optimizer = GeneticAlgorithmOptimizer()
result = optimizer.optimize(deliveries, vehicles, config, depot)

# Usar chatbot
chatbot = RouteChatbot()
chatbot.set_optimization_context(result)

# Perguntar
print(chatbot.chat("Quantos veículos foram usados?"))
print(chatbot.chat("Há entregas críticas?"))
print(chatbot.chat("Analise a eficiência"))
```

---

## ✅ Pronto para Usar!

Execute agora:
```bash
python examples/chatbot_interactive.py
```

E comece a fazer perguntas! 🤖
