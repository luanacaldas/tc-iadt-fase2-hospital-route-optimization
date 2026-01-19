# 🎬 Roteiro de Vídeo - Sistema de Otimização de Rotas Hospitalares
## Duração: 15 minutos | Projeto 2 - Algoritmos Genéticos + LLMs

---

## 📊 Estrutura do Vídeo (Timing)

| Seção | Tempo | Conteúdo |
|-------|-------|----------|
| **1. Introdução** | 0:00 - 1:30 | Problema, contexto e visão geral |
| **2. Arquitetura** | 1:30 - 3:00 | Estrutura do projeto e padrões SOLID |
| **3. Algoritmo Genético** | 3:00 - 6:30 | Implementação detalhada do GA |
| **4. Integração LLM** | 6:30 - 9:30 | Chatbot, relatórios e análises |
| **5. Demonstração Ao Vivo** | 9:30 - 13:00 | Sistema em execução |
| **6. Diferenciais** | 13:00 - 14:30 | O que foi além dos requisitos |
| **7. Conclusão** | 14:30 - 15:00 | Resultados e próximos passos |

---

## 🎯 SEÇÃO 1: INTRODUÇÃO (0:00 - 1:30)

### **Talking Points:**

**[0:00 - 0:30] Abertura e Problema**

```
"Olá! Vou apresentar meu Sistema de Otimização de Rotas Hospitalares 
que resolve o Vehicle Routing Problem usando Algoritmos Genéticos 
com integração de Large Language Models.

O problema: distribuir medicamentos para hospitais de São Paulo 
com múltiplos veículos, respeitando capacidade de carga, autonomia, 
e priorizando entregas críticas."
```

**[0:30 - 1:00] Slide: Visão Geral**

Mostrar:
- 🏥 **Cenário**: 20+ hospitais em São Paulo
- 🚗 **Frota**: 3 veículos com restrições diferentes
- 📦 **Entregas**: Críticas (prioridade 1) e regulares (prioridade 2+)
- 🧬 **Solução**: Algoritmo Genético com 6 componentes de fitness
- 🤖 **IA**: Chatbot analítico e relatórios automáticos

**[1:00 - 1:30] Requisitos Atendidos**

```
"Este projeto atende TODOS os requisitos obrigatórios:
✅ Algoritmo Genético para VRP
✅ Múltiplas restrições realistas
✅ Integração completa com LLMs
✅ Visualização interativa em mapas
E vai além com funcionalidades extras que vou mostrar."
```

---

## 🏗️ SEÇÃO 2: ARQUITETURA (1:30 - 3:00)

### **Talking Points:**

**[1:30 - 2:00] Slide: Estrutura de Módulos**

Mostrar a estrutura:
```
hospital_routes/
├── 📁 core/           # Interfaces base (SOLID)
├── 📁 optimization/   # Motor genético + fitness
├── 📁 llm/           # Chatbot + relatórios
├── 📁 visualization/ # Mapas + dashboards
└── 📁 interfaces/    # Web UI
```

```
"A arquitetura segue princípios SOLID e Design Patterns:
- Strategy Pattern para algoritmos de inicialização
- Composite Pattern para função fitness modular
- Factory Pattern para criação de otimizadores
- Interface BaseOptimizer permite trocar algoritmos facilmente"
```

**[2:00 - 2:30] Slide: Padrões Implementados**

Destacar:
- ✅ **Separation of Concerns**: Cada módulo tem responsabilidade única
- ✅ **Dependency Injection**: Componentes desacoplados
- ✅ **Interface Segregation**: Interfaces focadas
- ✅ **Open/Closed**: Extensível sem modificar código existente

**[2:30 - 3:00] Tecnologias**

```
"Tecnologias principais:
- Python 3.10+ com DEAP para algoritmos evolutivos
- Ollama (Llama 3.2) para LLM local e gratuito
- Flask para API REST
- MapBox GL JS para visualização em tempo real
- Folium para mapas estáticos
```

---

## 🧬 SEÇÃO 3: ALGORITMO GENÉTICO (3:00 - 6:30)

### **Talking Points:**

**[3:00 - 3:45] Representação Genética**

Mostrar código em `optimization/genetic_algorithm.py`:

```python
# Individual = List[List[str]]
# Cada lista interna = rota de um veículo

individual = [
    ["HOSP_001", "HOSP_003", "HOSP_005"],  # Veículo 1
    ["HOSP_002", "HOSP_004"],              # Veículo 2
    ["HOSP_006", "HOSP_007", "HOSP_008"]   # Veículo 3
]
```

```
"A representação genética é uma lista de listas, onde cada lista
interna representa a rota de um veículo. Isso permite otimizar
múltiplos veículos simultaneamente (VRP, não apenas TSP)."
```

**[3:45 - 4:45] Função Fitness (6 Componentes)**

Mostrar slide com a fórmula:

```python
fitness = α * distance                # Minimizar distância
       + β * capacity_penalty        # Penalizar sobrecarga
       + γ * autonomy_penalty        # Penalizar excesso autonomia
       + δ * priority_penalty        # Penalizar atraso críticos
       + ζ * load_balance_penalty    # Balancear carga
       + ε * vehicle_penalty         # Minimizar veículos
```

```
"A função fitness tem 6 componentes modulares:

1. DISTÂNCIA (peso 1.0): Minimiza km total
2. CAPACIDADE (peso 1000): Alta penalidade para sobrecarga
3. AUTONOMIA (peso 1000): Alta penalidade para rotas longas
4. PRIORIDADE (peso 500): Penaliza atraso em entregas críticas
5. BALANCEAMENTO (peso 50): Distribui carga equitativamente
6. VEÍCULOS (peso 100): Minimiza número de veículos usados

Cada componente está em um arquivo separado (Composite Pattern)."
```

**[4:45 - 5:45] Operadores Genéticos**

Mostrar código e explicar:

**Seleção:**
```python
def _select(self, population, config):
    return tools.selTournament(population, len(population), tournsize=3)
```
"Tournament Selection com 3 indivíduos por torneio"

**Crossover:**
```python
def _route_crossover(self, ind1, ind2):
    """Order Crossover (OX) adaptado para VRP"""
    # 1. Flatten rotas
    # 2. Aplica OX preservando ordem
    # 3. Redistribui respeitando capacidade
```
"Order Crossover adaptado que preserva ordem parcial e respeita restrições"

**Mutação (4 operadores):**
```python
# 1. SWAP: Troca dentro da rota
# 2. INSERTION: Move para outra posição
# 3. INTER-ROUTE SWAP: Move entre rotas
# 4. ROUTE MERGE: Combina rotas
```
"Múltiplos operadores aumentam diversidade genética"

**[5:45 - 6:30] Estratégias Adicionais**

```
"Implementei 3 melhorias além dos requisitos:

1. BUSCA LOCAL (2-opt + inter-route swap):
   - Refinamento após cada geração
   - Otimiza rotas individuais

2. ELITISMO:
   - Mantém top 5 soluções entre gerações
   - Garante não perder boas soluções

3. EARLY STOPPING:
   - Para se não houver melhoria por 50 gerações
   - Economiza tempo computacional
```

---

## 🤖 SEÇÃO 4: INTEGRAÇÃO LLM (6:30 - 9:30)

### **Talking Points:**

**[6:30 - 7:15] Arquitetura LLM**

Mostrar diagrama:
```
Ollama (Local) → llm/chatbot.py → RouteChatbot
                → llm/ollama_reporter.py → Relatórios
                → llm/route_analyzer.py → Análise
```

```
"Uso Ollama com Llama 3.2 rodando localmente:
- Gratuito e privado (dados não saem da máquina)
- Performance adequada para análise de rotas
- Sem dependência de APIs pagas

Três componentes principais:
1. RouteChatbot: Análise conversacional
2. OllamaReporter: Relatórios automáticos
3. RouteAnalyzer: Análise inteligente
```

**[7:15 - 8:00] Chatbot Analítico**

Mostrar código em `llm/chatbot.py`:

```python
class RouteChatbot:
    """Chatbot especializado em otimização de rotas."""
    
    def chat(self, user_message: str) -> str:
        """Responde perguntas usando contexto de otimização."""
        # 1. Extrai métricas do resultado
        # 2. Formata contexto estruturado
        # 3. Envia para LLM com system prompt
        # 4. Retorna resposta natural
```

```
"O chatbot responde perguntas em linguagem natural sobre:
- Eficiência das rotas
- Entregas críticas
- Comparação entre veículos
- Sugestões de melhorias
- Análise de distribuição de carga

DIFERENCIAL: Usa dados reais da otimização, não respostas genéricas."
```

**[8:00 - 8:45] Relatórios Automáticos**

Mostrar código em `llm/ollama_reporter.py`:

```python
class OllamaReporter(BaseReporter):
    def generate_driver_instructions(self, result, deliveries, vehicles):
        """Instruções detalhadas para motoristas"""
    
    def generate_daily_summary(self, result, deliveries):
        """Relatório diário de eficiência"""
    
    def generate_weekly_analysis(self, result, deliveries):
        """Análise semanal de padrões"""
    
    def generate_managerial_report(self, result, deliveries, vehicles):
        """Relatório gerencial com métricas"""
```

```
"4 tipos de relatórios gerados automaticamente:
1. Instruções para motoristas (ordem, distâncias, críticos)
2. Relatório diário (eficiência, economia)
3. Análise semanal (padrões, tendências)
4. Relatório gerencial (KPIs, decisões)
```

**[8:45 - 9:30] Prompts Eficientes**

Mostrar exemplo de `llm/prompts.py`:

```python
DRIVER_INSTRUCTIONS_PROMPT = """
Você é um assistente de logística hospitalar.

DADOS DA OTIMIZAÇÃO:
{context}

Gere instruções DETALHADAS para o motorista do veículo {vehicle_id}:
1. Lista ordenada de entregas com endereços
2. Distâncias entre paradas
3. Destaque entregas CRÍTICAS (prioridade 1)
4. Tempo estimado total
5. Dicas de navegação

FORMATO: Claro, objetivo, acionável.
"""
```

```
"Prompts estruturados com:
- Contexto detalhado (métricas reais)
- Instruções específicas
- Formato esperado
- Exemplos quando necessário

IMPORTANTE: Evitam respostas genéricas, forçam uso de dados reais."
```

---

## 💻 SEÇÃO 5: DEMONSTRAÇÃO AO VIVO (9:30 - 13:00)

### **Instruções de Demonstração:**

**[9:30 - 10:00] Iniciar Sistema**

```bash
# Terminal 1: Verificar Ollama
ollama list

# Terminal 2: Iniciar Dashboard
python app_scripts/run_chatbot_interface.py

# Navegador: http://localhost:5000
```

```
"Vou iniciar o sistema. Primeiro verifico que o Ollama está rodando,
depois inicio o dashboard Flask. O sistema carrega automaticamente
dados realistas de São Paulo."
```

**[10:00 - 10:45] Dashboard Principal**

Mostrar na tela:
1. **Header com KPIs**:
   - Distância total: 234.5 km
   - Custo estimado: R$ 586.25
   - Veículos usados: 3
   - Entregas: 20 (8 críticas)

2. **Mapa interativo**:
   - Rotas coloridas por veículo
   - Marcadores de hospitais
   - Legenda

```
"O dashboard mostra 5 KPIs em tempo real no header:
- Distância otimizada
- Custo total
- Veículos necessários
- Total de entregas
- Entregas críticas prioritárias

O mapa mostra as rotas otimizadas com cores diferentes por veículo.
Cada hospital tem um marcador com informações da entrega."
```

**[10:45 - 11:30] Chatbot Interativo**

Fazer perguntas no chatbot:

1. **Pergunta 1**: "Quantos veículos foram usados?"
   - Mostrar resposta com dados específicos

2. **Pergunta 2**: "Há entregas críticas?"
   - Mostrar lista de críticas com hospitais

3. **Pergunta 3**: "Analise a eficiência das rotas"
   - Mostrar análise detalhada

4. **Pergunta 4**: "Sugira melhorias"
   - Mostrar sugestões baseadas em dados reais

```
"O chatbot usa o contexto da otimização para dar respostas específicas.
Ele não responde com genéricos como 'depende do caso', mas usa os
dados reais das rotas calculadas.

Por exemplo, quando pergunto sobre entregas críticas, ele lista
exatamente quais hospitais têm entregas de prioridade 1."
```

**[11:30 - 12:15] Rastreamento em Tempo Real**

Clicar no botão "Rastrear" para abrir rastreamento MapBox:

```
"Agora vou mostrar o rastreamento em tempo real. Este é um diferencial
que implementei além dos requisitos."
```

Mostrar:
1. **3 veículos simulados** movendo simultaneamente
2. **Rotas completas** desenhadas no mapa
3. **Popups dinâmicos** com:
   - Status (Em trânsito / Chegando)
   - Destino atual
   - Velocidade (km/h)
   - ETA (tempo estimado)
4. **Trails/rastros** mostrando caminho percorrido
5. **Notificações toast** quando veículo chega em hospital
6. **Controle de velocidade** (mudar para 5x)

```
"Funcionalidades do rastreamento:
- Atualização a cada 100ms (10 FPS) para movimento suave
- Popups com informações em tempo real
- Rastros coloridos mostrando caminho percorrido
- Notificações quando veículo chega em hospital
- Controle de velocidade (posso acelerar para 5x ou 10x)
- Totalmente responsivo para mobile
```

**[12:15 - 13:00] Comparativo com Outras Abordagens**

Mostrar slide ou terminal com benchmark:

```python
# Resultados de benchmark (optimization/benchmark.py)
Algoritmo Genético:  234.5 km (3 veículos)
Greedy (Guloso):     287.3 km (4 veículos) [+22.5%]
Random:              412.8 km (5 veículos) [+76.0%]

Tempo de execução:
GA: 15.2s (100 gerações)
Greedy: 0.8s
Random: 0.1s
```

```
"Implementei um módulo de benchmark que compara:

1. ALGORITMO GENÉTICO (minha implementação):
   - 234.5 km com 3 veículos
   - Melhor qualidade de solução

2. GREEDY (baseline):
   - 287.3 km com 4 veículos
   - 22.5% PIOR que GA
   - Mais rápido mas menos eficiente

3. RANDOM (controle):
   - 412.8 km com 5 veículos
   - 76% PIOR que GA
   - Mostra ganho real do GA

O GA demora mais (15s) mas economiza 52km = ~R$130 por dia."
```

---

## 🌟 SEÇÃO 6: DIFERENCIAIS (13:00 - 14:30)

### **Talking Points:**

**[13:00 - 13:45] O Que Foi Além dos Requisitos**

Mostrar slide:

```
✅ REQUISITOS OBRIGATÓRIOS (100%)
   ✓ Algoritmo genético VRP
   ✓ 6 componentes fitness
   ✓ Operadores genéticos
   ✓ Restrições realistas
   ✓ Integração LLM completa
   ✓ Visualização em mapas

🌟 DIFERENCIAIS IMPLEMENTADOS (+30%)

1. RASTREAMENTO EM TEMPO REAL
   - MapBox GL JS 3.0
   - Movimento suave (100ms updates)
   - Popups dinâmicos
   - Trails/rastros
   - Notificações toast
   - Controle velocidade

2. BALANCEAMENTO DE CARGA
   - Componente fitness adicional
   - Distribui carga equitativamente
   - Evita sobrecarga de um veículo

3. BUSCA LOCAL
   - 2-opt para rotas individuais
   - Inter-route swap
   - Refina soluções do GA

4. ANÁLISE INTELIGENTE
   - RouteAnalyzer com insights
   - Sugestões acionáveis
   - Comparação entre veículos

5. MÚLTIPLAS ESTRATÉGIAS
   - 3 estratégias de inicialização
   - Random, Nearest Neighbor, Priority First
   - Testadas e comparadas

6. INTERFACE PROFISSIONAL
   - Design system completo
   - Inter font (Google Fonts)
   - Responsivo mobile-first
   - Dashboard com KPIs

7. DOCUMENTAÇÃO COMPLETA
   - 25+ documentos em /docs
   - Guias de instalação
   - Tutoriais detalhados
   - Troubleshooting

8. DADOS REALISTAS
   - 20+ hospitais de São Paulo
   - Coordenadas reais
   - Hotspots de acidentes
```

```
"Esses diferenciais mostram que fui além do básico:
- Não apenas otimizei rotas, mas criei um sistema completo
- Não apenas integrei LLM, mas fiz análise inteligente
- Não apenas visualizei, mas adicionei rastreamento em tempo real
- Não apenas funcionou, mas está pronto para produção"
```

**[13:45 - 14:30] Arquitetura e Qualidade de Código**

Mostrar código:

```python
# Exemplo de SOLID: Open/Closed Principle
class BaseOptimizer(ABC):
    """Interface para otimizadores."""
    
    @abstractmethod
    def optimize(self, deliveries, vehicles, depot, distance_calc):
        """Otimiza rotas."""
        pass

# Posso adicionar novos otimizadores sem modificar código existente
class SimulatedAnnealingOptimizer(BaseOptimizer):
    """Implementação com Simulated Annealing."""
    pass
```

```
"Qualidade do código:

1. PRINCÍPIOS SOLID
   - Single Responsibility
   - Open/Closed
   - Liskov Substitution
   - Interface Segregation
   - Dependency Inversion

2. DESIGN PATTERNS
   - Strategy (algoritmos)
   - Composite (fitness)
   - Factory (otimizadores)
   - Observer (rastreamento)

3. TRATAMENTO DE ERROS
   - Exceções customizadas
   - Validações de entrada
   - Mensagens claras

4. TESTES
   - Validação de restrições
   - Benchmark comparativo
   - Exemplos funcionais

5. DOCUMENTAÇÃO
   - Docstrings em tudo
   - Type hints
   - README detalhado
   - 25+ guias
```

---

## 🎯 SEÇÃO 7: CONCLUSÃO (14:30 - 15:00)

### **Talking Points:**

**[14:30 - 14:50] Resultados Alcançados**

```
"Resumindo o que foi entregue:

RESULTADOS QUANTITATIVOS:
✅ 234.5 km de rotas otimizadas (vs 287 km do greedy)
✅ 3 veículos (vs 4 do greedy)
✅ 100% das restrições atendidas
✅ 8 entregas críticas priorizadas
✅ Economia de ~R$130 por dia

RESULTADOS QUALITATIVOS:
✅ Sistema completo e funcional
✅ Interface profissional
✅ Código limpo e extensível
✅ Documentação completa
✅ Pronto para uso real

CONFORMIDADE:
✅ 100% dos requisitos obrigatórios
✅ +30% de funcionalidades extras
✅ Código seguindo best practices
```

**[14:50 - 15:00] Próximos Passos e Encerramento**

```
"Possíveis evoluções futuras:

1. OTIMIZAÇÕES:
   - Paralelização do GA
   - Cache de distâncias
   - GPU para fitness

2. FUNCIONALIDADES:
   - Janelas de tempo
   - Múltiplos depósitos
   - Reabastecimento

3. INTEGRAÇÕES:
   - API de mapas para rotas reais
   - Sistema de tracking GPS
   - Dashboard gerencial web

4. IA:
   - Fine-tuning LLM para domínio
   - Previsão de demanda
   - Otimização contínua

Obrigado pela atenção! O código está disponível no GitHub
e toda a documentação em /docs. Estou à disposição para perguntas."
```

---

## 📝 CHECKLIST PRÉ-GRAVAÇÃO

### Ambiente
- [ ] Ollama rodando (`ollama list`)
- [ ] Modelo llama3.2 instalado
- [ ] Token MapBox configurado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Porta 5000 livre

### Arquivos
- [ ] Dashboard funcional (`python app_scripts/run_chatbot_interface.py`)
- [ ] Rastreamento MapBox funcionando
- [ ] Mapa route_map.html gerado
- [ ] Dados realistas carregados

### Gravação
- [ ] Tela limpa (fechar abas desnecessárias)
- [ ] Terminal preparado com comandos
- [ ] Slides preparados (se usar)
- [ ] Testar áudio e vídeo
- [ ] Timer visível (15 minutos)

### Demonstração
- [ ] Testar fluxo completo antes
- [ ] Preparar perguntas para chatbot
- [ ] Testar rastreamento MapBox
- [ ] Verificar métricas no dashboard
- [ ] Ter código pronto para mostrar

---

## 🎨 DICAS DE APRESENTAÇÃO

### Visual
1. **Tela Dividida**: Código (esquerda) + Dashboard (direita)
2. **Zoom**: Aumentar fonte do código e terminal
3. **Destaque**: Use mouse/cursor para destacar partes importantes
4. **Transições**: Mostre o fluxo completo (terminal → navegador → resultado)

### Verbal
1. **Confiança**: Fale com segurança, você domina o código
2. **Ritmo**: Não corra, 15 minutos é suficiente
3. **Entusiasmo**: Mostre empolgação com os diferenciais
4. **Clareza**: Explique COMO você implementou, não apenas O QUE fez

### Técnico
1. **Código Real**: Mostre implementações reais, não apenas slides
2. **Demonstração**: Sistema funcionando é mais importante que teoria
3. **Métricas**: Use números concretos (234km, R$586, 3 veículos)
4. **Comparativo**: Mostre que GA é melhor que alternativas

### Diferenciais
1. **Enfatize**: "Isso vai além dos requisitos..."
2. **Justifique**: "Implementei porque..."
3. **Mostre Valor**: "Isso economiza... / melhora..."
4. **Seja Específico**: Números, não adjetivos vagos

---

## 📋 PERGUNTAS COMUNS DO PROFESSOR

Esteja preparado para:

### 1. "Por que escolheu Algoritmo Genético?"
```
"Escolhi GA porque:
- Ideal para problemas combinatórios como VRP
- Naturalmente lida com múltiplas restrições
- Extensível (fácil adicionar novos objetivos)
- Não precisa de gradientes (fitness black-box)
- Exploração + exploração balanceadas"
```

### 2. "Como garantiu convergência?"
```
"Implementei 3 mecanismos:
1. Elitismo: mantém top 5 soluções
2. Early stopping: para sem melhoria por 50 gerações
3. Busca local: refina melhor solução

Testado com múltiplos datasets, sempre converge."
```

### 3. "Por que Ollama e não OpenAI?"
```
"Ollama porque:
- Gratuito (sem custos de API)
- Privado (dados ficam locais)
- Sem dependência de internet
- Performance adequada para o caso de uso
- Fácil de instalar (ollama pull llama3.2)"
```

### 4. "Como validou as restrições?"
```
"Validação em 3 níveis:
1. Na função fitness: penalidades altas
2. No crossover/mutação: reparo se necessário
3. No resultado final: verificação completa

Arquivo: utils/validators.py
Testes: examples/test_optimization.py"
```

### 5. "Qual a escalabilidade?"
```
"Testado com:
- 20 entregas: ~15s
- 50 entregas: ~45s (estimado)
- 100 entregas: ~120s (estimado)

Melhorias possíveis:
- Paralelização (DEAP suporta)
- Cache de distâncias
- GPU para fitness (se disponível)"
```

---

## 💡 EXEMPLO DE NARRAÇÃO COMPLETA (Seção 5)

```
[10:00] "Agora vou demonstrar o sistema completo funcionando.

[10:05] Aqui no dashboard principal, vocês podem ver o header com
5 KPIs em tempo real. A rota otimizada tem 234 quilômetros,
custa estimados 586 reais, usa 3 veículos, atende 20 entregas,
sendo 8 delas críticas que foram priorizadas.

[10:20] No mapa interativo aqui embaixo, cada cor representa um
veículo diferente. O azul é o veículo 1, vermelho é o 2, verde é o 3.
Vocês podem ver que as rotas estão balanceadas - nenhum veículo
está sobrecarregado enquanto outro fica ocioso.

[10:35] Agora vou usar o chatbot integrado. Vou perguntar:
'Quantos veículos foram usados?' E ele responde com dados
específicos da otimização, não uma resposta genérica.

[10:50] Outra pergunta: 'Há entregas críticas?' Ele lista
exatamente os 8 hospitais com prioridade 1, com nomes e veículos
responsáveis. Isso é importante porque o LLM está usando o
contexto real da otimização.

[11:05] Agora uma análise mais complexa: 'Analise a eficiência
das rotas'. Ele faz uma análise detalhada da distribuição de
carga, distâncias, e até sugere se há possibilidade de melhoria.

[11:20] E quando pergunto 'Sugira melhorias', ele analisa os
dados e dá sugestões específicas e acionáveis. Por exemplo,
ele identifica se algum veículo está muito carregado ou se
uma rota pode ser otimizada.

[11:35] Agora vou mostrar o diferencial do rastreamento em tempo
real. Clico aqui em 'Rastrear' e abre uma nova aba com o mapa
MapBox.

[11:45] Aqui vocês podem ver os 3 veículos se movendo
simultaneamente. O movimento é suave porque atualiza a cada
100 milissegundos. Quando clico em um veículo, o popup mostra
status, destino, velocidade e tempo estimado - tudo atualizado
em tempo real.

[12:00] Esses rastros coloridos mostram o caminho já percorrido
por cada veículo. E quando um veículo chega em um hospital,
aparece essa notificação toast aqui em cima.

[12:15] No header, posso controlar a velocidade da simulação.
Vou mudar para 5x para vocês verem os veículos se movendo
mais rápido. Útil para demonstrações ou análise rápida.

[12:30] Tudo isso é responsivo para mobile. Se eu diminuir a
tela... vocês podem ver que o layout se adapta automaticamente.
```

---

## 🎬 BOA SORTE NA GRAVAÇÃO!

**Lembre-se:**
- Você domina o projeto
- 15 minutos passa rápido
- Demonstração vale mais que teoria
- Mostre os diferenciais
- Seja específico com números
- Teste tudo antes de gravar

**Sucesso! 🚀**
