# ✅ Mapeamento Requisitos Obrigatórios → Roteiro do Vídeo

## 📋 CHECKLIST: Cada Requisito e Onde Aparece no Vídeo

---

## 🧬 REQUISITO 1: ALGORITMO GENÉTICO PARA OTIMIZAÇÃO DE ROTAS

### ✅ 1.1 Sistema que resolve TSP/VRP

**Requisito:**
> "Desenvolver um sistema que resolva o problema do caixeiro viajante (TSP) para otimizar rotas de entrega de medicamentos"

**Onde mostrar no vídeo:**

- **[3:00-3:45]** Seção 3 - Representação Genética
  ```
  FALAR: "Resolvi o Vehicle Routing Problem, que é uma extensão 
  do TSP para múltiplos veículos. A representação genética é 
  uma lista de listas, onde cada lista é a rota de um veículo."
  
  MOSTRAR: Código em optimization/genetic_algorithm.py
  ```

- **[10:00-10:45]** Demo - Dashboard
  ```
  MOSTRAR: Mapa com 3 rotas otimizadas
  FALAR: "Aqui estão as rotas otimizadas para 20 hospitais 
  usando 3 veículos. O algoritmo genético encontrou esta 
  solução em 15 segundos."
  ```

**Evidência no código:**
- `optimization/genetic_algorithm.py` - Classe `GeneticAlgorithmOptimizer`
- Linha ~95-100

---

### ✅ 1.2 Representação genética adequada

**Requisito:**
> "Implementar a representação genética adequada para rotas"

**Onde mostrar no vídeo:**

- **[3:00-3:45]** Seção 3 - Representação
  ```
  FALAR: "A representação genética é List[List[str]], onde 
  cada indivíduo representa um conjunto completo de rotas 
  para todos os veículos."
  
  MOSTRAR SLIDE:
  individual = [
      ["HOSP_001", "HOSP_003", "HOSP_005"],  # Veículo 1
      ["HOSP_002", "HOSP_004"],              # Veículo 2
      ["HOSP_006", "HOSP_007", "HOSP_008"]   # Veículo 3
  ]
  
  FALAR: "Isso permite otimizar múltiplos veículos 
  simultaneamente, não apenas um único veículo."
  ```

**Evidência no código:**
- `optimization/genetic_algorithm.py` - Linha ~300-350
- Função `_setup_deap()`

---

### ✅ 1.3 Operadores genéticos especializados

**Requisito:**
> "Desenvolver operadores genéticos especializados (seleção, crossover, mutação) para o problema de roteamento"

**Onde mostrar no vídeo:**

- **[4:45-5:45]** Seção 3 - Operadores Genéticos

#### SELEÇÃO
```
FALAR: "Para seleção, implementei Tournament Selection 
com 3 indivíduos por torneio, que mantém boa pressão 
seletiva sem convergir muito rápido."

MOSTRAR CÓDIGO:
def _select(self, population, config):
    return tools.selTournament(population, len(population), tournsize=3)
```

#### CROSSOVER
```
FALAR: "O crossover é Order Crossover adaptado para VRP. 
Ele preserva a ordem parcial das entregas e redistribui 
respeitando as restrições de capacidade."

MOSTRAR CÓDIGO:
def _route_crossover(self, ind1, ind2):
    """Order Crossover (OX) adaptado para VRP"""
    # 1. Flatten rotas
    # 2. Aplica OX preservando ordem
    # 3. Redistribui respeitando capacidade
```

#### MUTAÇÃO
```
FALAR: "Implementei 4 operadores de mutação diferentes 
para aumentar a diversidade genética:
1. Swap - troca dentro da rota
2. Insertion - move para outra posição
3. Inter-route swap - move entre rotas
4. Route merge - combina rotas se possível"

MOSTRAR CÓDIGO:
def _mutate(self, offspring, config):
    # Aplica um dos 4 operadores aleatoriamente
```

**Evidência no código:**
- Seleção: Linha ~550-558
- Crossover: Linha ~560-626
- Mutação: Linha ~680-750

---

### ✅ 1.4 Função fitness com distância, prioridade e restrições

**Requisito:**
> "Criar uma função fitness que considere distância, prioridade de entregas e outras restrições relevantes"

**Onde mostrar no vídeo:**

- **[3:45-4:45]** Seção 3 - Função Fitness

```
FALAR: "A função fitness tem 6 componentes. Vou explicar cada um:

FITNESS = α·distance + β·capacity + γ·autonomy + δ·priority + ζ·balance + ε·vehicles

1. DISTÂNCIA (peso 1.0): Minimiza quilômetros totais
   → Atende requisito obrigatório

2. CAPACIDADE (peso 1000): Penaliza sobrecarga
   → Alta penalidade para garantir respeito à restrição

3. AUTONOMIA (peso 1000): Penaliza rotas muito longas
   → Alta penalidade para garantir veículos não ficam sem combustível

4. PRIORIDADE (peso 500): Penaliza atraso em entregas críticas
   → Atende requisito obrigatório de priorização

5. BALANCEAMENTO (peso 50): Distribui carga entre veículos
   → Melhoria adicional para eficiência

6. VEÍCULOS (peso 100): Minimiza número de veículos
   → Otimização de recursos

MOSTRAR SLIDE com pesos e objetivos

FALAR: "Cada componente está em um arquivo separado, 
seguindo Composite Pattern para facilitar manutenção."
```

**Evidência no código:**
- `optimization/fitness/composite_fitness.py`
- `optimization/fitness/distance_fitness.py` (distância)
- `optimization/fitness/priority_penalty.py` (prioridade)
- Outros componentes em `optimization/fitness/`

---

## 🚗 REQUISITO 2: RESTRIÇÕES REALISTAS

### ✅ 2.1 Prioridades diferentes

**Requisito:**
> "Prioridades diferentes para entregas (medicamentos críticos vs. insumos regulares)"

**Onde mostrar no vídeo:**

- **[4:00-4:15]** Seção 3 - Componente Priority Penalty
  ```
  FALAR: "Entregas têm prioridade 1 (críticas) ou 2+ (regulares).
  O componente PriorityPenalty penaliza atraso em entregas críticas 
  com peso 500, garantindo que medicamentos urgentes sejam 
  entregues primeiro."
  ```

- **[10:45-11:00]** Demo - Chatbot
  ```
  PERGUNTAR NO CHATBOT: "Há entregas críticas?"
  
  CHATBOT RESPONDE: "Sim, há 8 entregas críticas (prioridade 1):
  - Hospital das Clínicas (Veículo 1)
  - Hospital Santa Casa (Veículo 1)
  - ..."
  
  FALAR: "O sistema identifica e prioriza automaticamente 
  as entregas críticas."
  ```

**Evidência no código:**
- `core/interfaces.py` - Campo `Delivery.priority`
- `optimization/fitness/priority_penalty.py`
- `optimization/initialization_strategy.py` - `PriorityFirstInitializationStrategy`

---

### ✅ 2.2 Capacidade limitada de carga

**Requisito:**
> "Capacidade limitada de carga dos veículos"

**Onde mostrar no vídeo:**

- **[4:15-4:30]** Seção 3 - Componente Capacity Penalty
  ```
  FALAR: "Cada veículo tem capacidade máxima em kg. 
  O componente CapacityPenalty tem peso 1000 (muito alto) 
  para garantir que NUNCA sobrecarregamos um veículo."
  
  MOSTRAR DADOS:
  Veículo 1: max 150kg
  Veículo 2: max 200kg
  Veículo 3: max 180kg
  ```

- **[11:00-11:15]** Demo - Chatbot
  ```
  PERGUNTAR: "Analise a distribuição de carga"
  
  CHATBOT RESPONDE: "Veículo 1: 142kg/150kg (94.7%)
                     Veículo 2: 185kg/200kg (92.5%)
                     Veículo 3: 165kg/180kg (91.7%)
                     
  Todos dentro da capacidade, bem balanceados."
  
  FALAR: "Nenhum veículo está sobrecarregado, a restrição 
  é respeitada."
  ```

**Evidência no código:**
- `core/interfaces.py` - Campo `VehicleConstraints.max_capacity`
- `optimization/fitness/capacity_penalty.py`

---

### ✅ 2.3 Autonomia limitada

**Requisito:**
> "Autonomia limitada dos veículos (distância máxima que pode ser percorrida)"

**Onde mostrar no vídeo:**

- **[4:30-4:45]** Seção 3 - Componente Autonomy Penalty
  ```
  FALAR: "Veículos têm autonomia máxima (range) em km. 
  Se uma rota exceder essa autonomia, há penalidade de 1000. 
  Isso garante que veículos não ficam sem combustível."
  
  MOSTRAR DADOS:
  Veículo 1: max 100km
  Veículo 2: max 120km
  Veículo 3: max 110km
  ```

- **[12:30-12:45]** Demo - Comparativo
  ```
  MOSTRAR SLIDE:
  Veículo 1: 87.3km/100km ✅
  Veículo 2: 115.8km/120km ✅
  Veículo 3: 98.2km/110km ✅
  
  FALAR: "Todas as rotas respeitam a autonomia máxima."
  ```

**Evidência no código:**
- `core/interfaces.py` - Campo `VehicleConstraints.max_range`
- `optimization/fitness/autonomy_penalty.py`

---

### ✅ 2.4 Múltiplos veículos (VRP)

**Requisito:**
> "Múltiplos veículos disponíveis (ampliando para o problema de roteamento de veículos - VRP)"

**Onde mostrar no vídeo:**

- **[3:15-3:30]** Seção 3 - Representação
  ```
  FALAR: "A representação suporta múltiplos veículos 
  simultaneamente. Isso torna o problema VRP (Vehicle 
  Routing Problem), que é mais complexo que TSP.
  
  Cada lista interna representa a rota de um veículo 
  diferente, permitindo otimizar todos os veículos ao 
  mesmo tempo."
  ```

- **[10:15-10:30]** Demo - Dashboard
  ```
  MOSTRAR MAPA com 3 rotas coloridas:
  🔵 Azul = Veículo 1
  🔴 Vermelho = Veículo 2
  🟢 Verde = Veículo 3
  
  FALAR: "O algoritmo otimizou 3 veículos simultaneamente, 
  distribuindo as 20 entregas entre eles de forma eficiente."
  ```

**Evidência no código:**
- Estrutura: `List[List[str]]` em `genetic_algorithm.py`
- Linha ~300-400

---

### ✅ 2.5 Outras restrições interessantes

**Requisito:**
> "Outras restrições que achar interessante"

**Onde mostrar no vídeo:**

- **[5:45-6:30]** Seção 3 - Melhorias Adicionais
  ```
  FALAR: "Implementei 3 restrições adicionais que vão 
  além do obrigatório:
  
  1. BALANCEAMENTO DE CARGA: Evita que um veículo fique 
     sobrecarregado enquanto outros ficam ociosos
  
  2. MINIMIZAÇÃO DE VEÍCULOS: Tenta usar menos veículos 
     quando possível, economizando custos
  
  3. BUSCA LOCAL: 2-opt e inter-route swap refinam as 
     soluções após o algoritmo genético
  
  Essas melhorias aumentam a eficiência do sistema."
  ```

**Evidência no código:**
- `optimization/fitness/load_balance_penalty.py`
- `optimization/local_search.py`
- Peso de veículos em `composite_fitness.py`

---

### ✅ 2.6 Visualização em mapa

**Requisito:**
> "Visualizar as rotas otimizadas em um mapa para fácil interpretação"

**Onde mostrar no vídeo:**

- **[10:00-10:45]** Demo - Dashboard Mapa
  ```
  MOSTRAR: route_map.html com Folium
  
  FALAR: "As rotas otimizadas são visualizadas em um mapa 
  interativo usando Folium. Cada veículo tem uma cor diferente:
  - Azul para Veículo 1
  - Vermelho para Veículo 2
  - Verde para Veículo 3
  
  Os hospitais têm marcadores com informações da entrega."
  ```

- **[11:30-12:15]** Demo - Rastreamento Tempo Real
  ```
  MOSTRAR: rastreamento_mapbox.html
  
  FALAR: "Além do mapa estático, implementei rastreamento 
  em tempo real com MapBox GL JS. Aqui você vê os veículos 
  se movendo, popups com informações dinâmicas, e rastros 
  mostrando o caminho percorrido.
  
  Este é um diferencial que vai além dos requisitos."
  ```

**Evidência no código:**
- `visualization/map_generator.py` (Folium)
- `interfaces/rastreamento_mapbox.html` (MapBox - diferencial)

---

## 🤖 REQUISITO 3: INTEGRAÇÃO COM LLMs

### ✅ 3.1 Instruções para motoristas

**Requisito:**
> "Gerar instruções detalhadas para motoristas e equipes de entrega com base nas rotas otimizadas"

**Onde mostrar no vídeo:**

- **[8:00-8:30]** Seção 4 - Relatórios Automáticos
  ```
  FALAR: "Implementei geração automática de instruções 
  para motoristas usando Ollama (LLM local). O sistema 
  gera instruções detalhadas incluindo:
  - Ordem de entregas
  - Endereços completos
  - Distâncias entre paradas
  - Destaque para entregas críticas
  - Tempo estimado total"
  
  MOSTRAR CÓDIGO:
  def generate_driver_instructions(self, result, deliveries, vehicles):
      # Gera instruções usando LLM
  ```

- **[11:05-11:20]** Demo - (Opcional: mostrar arquivo gerado)
  ```
  Se tiver tempo, mostrar arquivo:
  output/driver_instructions.txt
  
  FALAR: "Aqui está um exemplo de instruções geradas 
  automaticamente para o motorista do Veículo 1."
  ```

**Evidência no código:**
- `llm/ollama_reporter.py` - Método `generate_driver_instructions()`
- `llm/prompts.py` - Template `DRIVER_INSTRUCTIONS_PROMPT`

---

### ✅ 3.2 Relatórios diários/semanais

**Requisito:**
> "Criar relatórios diários/semanais sobre eficiência de rotas, economia de tempo e recursos"

**Onde mostrar no vídeo:**

- **[8:30-8:45]** Seção 4 - Relatórios
  ```
  FALAR: "O sistema gera 4 tipos de relatórios automáticos:
  
  1. INSTRUÇÕES PARA MOTORISTAS (já mostrei)
  2. RELATÓRIO DIÁRIO: Eficiência do dia, economia de recursos
  3. ANÁLISE SEMANAL: Padrões, tendências, comparações
  4. RELATÓRIO GERENCIAL: KPIs, decisões estratégicas
  
  Todos gerados automaticamente pelo LLM Ollama."
  
  MOSTRAR CÓDIGO:
  def generate_daily_summary(...)
  def generate_weekly_analysis(...)
  def generate_managerial_report(...)
  ```

**Evidência no código:**
- `llm/ollama_reporter.py`:
  - `generate_daily_summary()`
  - `generate_weekly_analysis()`
  - `generate_managerial_report()`

---

### ✅ 3.3 Sugestões de melhorias

**Requisito:**
> "Sugerir melhorias no processo com base nos padrões identificados"

**Onde mostrar no vídeo:**

- **[7:15-8:00]** Seção 4 - Chatbot Analítico
  ```
  FALAR: "O chatbot não apenas responde perguntas, mas 
  também analisa os dados e sugere melhorias específicas."
  ```

- **[11:15-11:30]** Demo - Chatbot Sugestões
  ```
  PERGUNTAR NO CHATBOT: "Sugira melhorias"
  
  CHATBOT RESPONDE: "Analisando as rotas otimizadas:
  
  SUGESTÕES:
  1. Veículo 2 está com 92.5% da capacidade. Considere 
     realocar 1 entrega para Veículo 1 (94.7%) para 
     melhor balanceamento.
  
  2. Rota do Veículo 3 tem 3 entregas próximas ao final. 
     Considere reordenar para reduzir 2-3km.
  
  3. Todas as entregas críticas estão nos primeiros 50% 
     das rotas ✅ Excelente priorização!
  
  IMPACTO ESTIMADO: Economia de 5-7km (~R$15/dia)"
  
  FALAR: "O chatbot usa o RouteAnalyzer para dar sugestões 
  específicas e acionáveis, baseadas nos dados reais da 
  otimização, não respostas genéricas."
  ```

**Evidência no código:**
- `llm/chatbot.py` - Classe `RouteChatbot`
- `llm/route_analyzer.py` - Classe `RouteAnalyzer`
- Método `analyze_route()` com recomendações

---

### ✅ 3.4 Prompts eficientes

**Requisito:**
> "Implementar prompts eficientes para extrair informações úteis da LLM"

**Onde mostrar no vídeo:**

- **[8:45-9:30]** Seção 4 - Prompts Estruturados
  ```
  FALAR: "Os prompts são estruturados com:
  
  1. CONTEXTO: Quem é o assistente (logística hospitalar)
  2. DADOS REAIS: Métricas da otimização (234km, 3 veículos, etc)
  3. INSTRUÇÃO ESPECÍFICA: O que queremos (análise, sugestão)
  4. FORMATO ESPERADO: Como responder (tópicos, lista)
  
  Isso evita respostas genéricas e força o LLM a usar 
  os dados reais fornecidos."
  
  MOSTRAR CÓDIGO em llm/prompts.py:
  DRIVER_INSTRUCTIONS_PROMPT = """
  Você é um assistente de logística hospitalar.
  
  DADOS DA OTIMIZAÇÃO:
  {context}
  
  Gere instruções DETALHADAS para motorista...
  FORMATO: Claro, objetivo, acionável.
  """
  ```

**Evidência no código:**
- `llm/prompts.py` - Templates estruturados
- `llm/chatbot.py` - System prompts detalhados

---

### ✅ 3.5 Respostas em linguagem natural

**Requisito:**
> "Permitir que o sistema responda as perguntas em linguagem natural sobre as rotas e entregas"

**Onde mostrar no vídeo:**

- **[10:45-11:30]** Demo - Chatbot Interativo (PRINCIPAL!)
  ```
  FALAR: "Agora vou demonstrar o chatbot respondendo 
  perguntas em linguagem natural."
  
  PERGUNTAS NO CHATBOT:
  
  1. "Quantos veículos foram usados?"
     → Resposta com dados específicos
  
  2. "Há entregas críticas?"
     → Lista hospitais com prioridade 1
  
  3. "Qual a distância total?"
     → Distância, custo, economia
  
  4. "Analise a eficiência das rotas"
     → Análise detalhada da distribuição
  
  5. "Sugira melhorias"
     → Sugestões específicas baseadas em dados
  
  FALAR: "O chatbot entende linguagem natural e responde 
  com dados reais da otimização. Ele tem contexto completo 
  das rotas, entregas, veículos e restrições."
  ```

**Evidência no código:**
- `llm/chatbot.py` - Método `chat(user_message)`
- `visualization/chatbot_interface_v2.py` - Interface web
- `app_scripts/server_chatbot.py` - API REST

---

## 📊 RESUMO: TIMING DE CADA REQUISITO NO VÍDEO

### Algoritmo Genético (3:00 - 6:30)
- ✅ TSP/VRP: 3:00-3:45
- ✅ Representação: 3:00-3:45
- ✅ Operadores: 4:45-5:45
- ✅ Fitness: 3:45-4:45

### Restrições (3:45 - 6:30)
- ✅ Prioridades: 4:00-4:15 + 10:45-11:00 (demo)
- ✅ Capacidade: 4:15-4:30 + 11:00-11:15 (demo)
- ✅ Autonomia: 4:30-4:45 + 12:30-12:45 (demo)
- ✅ Múltiplos veículos: 3:15-3:30 + 10:15-10:30 (demo)
- ✅ Outras: 5:45-6:30
- ✅ Visualização: 10:00-10:45 + 11:30-12:15 (demo)

### LLM (6:30 - 9:30 + 10:45 - 11:30)
- ✅ Instruções motoristas: 8:00-8:30
- ✅ Relatórios: 8:30-8:45
- ✅ Sugestões: 7:15-8:00 + 11:15-11:30 (demo)
- ✅ Prompts: 8:45-9:30
- ✅ Linguagem natural: 10:45-11:30 (demo) ← MAIS IMPORTANTE

---

## ✅ CHECKLIST FINAL DURANTE GRAVAÇÃO

Durante o vídeo, mencione EXPLICITAMENTE:

### Algoritmo Genético
- [ ] "Resolvi o TSP ampliado para VRP com múltiplos veículos"
- [ ] "Representação genética: List[List[str]]"
- [ ] "3 operadores: Tournament Selection, Order Crossover, 4 mutações"
- [ ] "Fitness com 6 componentes incluindo distância e prioridade"

### Restrições
- [ ] "Prioridades: críticas (1) vs regulares (2+)"
- [ ] "Capacidade limitada: peso 1000 na penalidade"
- [ ] "Autonomia limitada: distância máxima respeitada"
- [ ] "Múltiplos veículos: VRP completo, não apenas TSP"
- [ ] "Balanceamento de carga e busca local como extras"
- [ ] "Visualização em mapa Folium + MapBox"

### LLM
- [ ] "Instruções automáticas para motoristas"
- [ ] "4 tipos de relatórios: diário, semanal, gerencial"
- [ ] "Sugestões específicas baseadas em análise"
- [ ] "Prompts estruturados com contexto + dados + formato"
- [ ] "Chatbot responde linguagem natural com dados reais"

---

## 🎯 FRASES MÁGICAS (Use no vídeo!)

### Para GA
> "Implementei o Algoritmo Genético ampliando do TSP para VRP com múltiplos veículos, usando representação List[List[str]] e função fitness com 6 componentes incluindo distância e prioridade."

### Para Restrições
> "O sistema respeita TODAS as restrições: prioridades diferentes com penalidade 500, capacidade limitada com penalidade 1000, autonomia limitada, e múltiplos veículos simultaneamente."

### Para LLM
> "Integrei Ollama (LLM local) para gerar instruções automáticas para motoristas, relatórios diários e semanais, e um chatbot que responde em linguagem natural com sugestões específicas baseadas nos dados reais da otimização."

---

## 💡 DICA FINAL

Se o professor perguntar "Você atendeu todos os requisitos?", responda:

> "Sim! Atendi 100% dos requisitos obrigatórios:
> 
> ALGORITMO GENÉTICO ✅
> - TSP ampliado para VRP
> - Representação genética adequada
> - 3 operadores especializados
> - Fitness com distância + prioridade + restrições
> 
> RESTRIÇÕES ✅
> - Prioridades diferentes (críticas vs regulares)
> - Capacidade limitada
> - Autonomia limitada
> - Múltiplos veículos (VRP)
> - Extras: balanceamento + busca local
> - Visualização em mapa
> 
> LLM ✅
> - Instruções para motoristas
> - Relatórios diários/semanais
> - Sugestões de melhorias
> - Prompts eficientes
> - Linguagem natural (chatbot)
> 
> E ainda implementei 30% de funcionalidades extras como rastreamento tempo real!"

---

**🎬 COM ESTE MAPEAMENTO, VOCÊ NÃO VAI ESQUECER NENHUM REQUISITO! 🚀**
