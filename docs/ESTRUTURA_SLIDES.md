# 📊 Estrutura de Slides - Vídeo 15 Minutos

## 🎨 Guia para Criação de Slides de Apoio

Este documento fornece a estrutura de slides que você pode usar como suporte visual durante o vídeo.

**Nota**: Slides são opcionais. Demonstração ao vivo é mais importante!

---

## SLIDE 1: TÍTULO (0:00)

```
╔════════════════════════════════════════════════╗
║                                                ║
║   🏥 Sistema de Otimização de Rotas          ║
║        Hospitalares                           ║
║                                                ║
║   Vehicle Routing Problem                      ║
║   Algoritmos Genéticos + LLMs                  ║
║                                                ║
║   [Seu Nome]                                   ║
║   TC IADT - Fase 2 - Projeto 2                ║
║                                                ║
╚════════════════════════════════════════════════╝
```

---

## SLIDE 2: PROBLEMA (0:30)

```
🎯 O PROBLEMA

Cenário: Distribuição de Medicamentos em São Paulo

📦 20+ entregas para hospitais
🚗 3 veículos com restrições diferentes
⚡ 8 entregas CRÍTICAS (prioridade 1)

Restrições:
  ✓ Capacidade de carga limitada
  ✓ Autonomia limitada (km máximos)
  ✓ Múltiplos veículos simultâneos
  ✓ Priorização de entregas críticas

Objetivo: Minimizar distância respeitando TODAS as restrições
```

---

## SLIDE 3: SOLUÇÃO (1:00)

```
✨ SOLUÇÃO IMPLEMENTADA

🧬 Algoritmo Genético
   └─ Vehicle Routing Problem (VRP)
   └─ 6 componentes de fitness
   └─ Operadores customizados

🤖 Integração LLM (Ollama)
   └─ Chatbot analítico
   └─ Relatórios automáticos
   └─ Análise inteligente

📍 Visualização
   └─ Mapas interativos (Folium)
   └─ Rastreamento tempo real (MapBox)
   └─ Dashboard profissional
```

---

## SLIDE 4: ARQUITETURA (1:30)

```
🏗️ ARQUITETURA MODULAR (SOLID)

┌─────────────────────────────────────────┐
│  core/          (Interfaces base)       │
│  ├─ BaseOptimizer                       │
│  ├─ BaseReporter                        │
│  └─ Models (Delivery, Vehicle, etc)     │
├─────────────────────────────────────────┤
│  optimization/  (Motor genético)        │
│  ├─ GeneticAlgorithmOptimizer           │
│  ├─ Fitness (6 componentes)             │
│  └─ Strategies (3 inicializações)       │
├─────────────────────────────────────────┤
│  llm/          (Inteligência)           │
│  ├─ RouteChatbot                        │
│  ├─ OllamaReporter                      │
│  └─ RouteAnalyzer                       │
├─────────────────────────────────────────┤
│  visualization/ (Interfaces)            │
│  ├─ MapGenerator (Folium)               │
│  └─ Dashboard (Flask)                   │
└─────────────────────────────────────────┘

Design Patterns: Strategy, Composite, Factory
```

---

## SLIDE 5: TECNOLOGIAS (2:30)

```
🛠️ STACK TECNOLÓGICO

Backend:
  🐍 Python 3.10+
  🧬 DEAP (Algoritmos Evolutivos)
  🌐 Flask (API REST)
  🤖 Ollama (LLM local - Llama 3.2)

Frontend:
  🗺️ MapBox GL JS 3.0 (Rastreamento)
  🍃 Folium (Mapas estáticos)
  🎨 HTML5 + CSS3 + JavaScript ES6+
  📊 Inter Font (Google Fonts)

Análise:
  📏 Haversine (Distâncias geodésicas)
  📐 NumPy (Cálculos numéricos)
```

---

## SLIDE 6: REPRESENTAÇÃO GENÉTICA (3:15)

```
🧬 REPRESENTAÇÃO GENÉTICA

Individual = List[List[str]]
             └─ Lista de rotas
                └─ Cada rota = lista de IDs

Exemplo:
┌────────────────────────────────────────┐
│ individual = [                         │
│   ["H001", "H003", "H005"],  ← Veículo 1│
│   ["H002", "H004"],          ← Veículo 2│
│   ["H006", "H007", "H008"]   ← Veículo 3│
│ ]                                      │
└────────────────────────────────────────┘

✓ VRP completo (não apenas TSP)
✓ Múltiplos veículos simultâneos
✓ Flexível e extensível
```

---

## SLIDE 7: FUNÇÃO FITNESS (3:45)

```
⚖️ FUNÇÃO FITNESS - 6 COMPONENTES

fitness = α·distance + β·capacity + γ·autonomy
        + δ·priority + ζ·balance + ε·vehicles

┌──────────────┬───────┬──────────────────────┐
│ Componente   │ Peso  │ Objetivo             │
├──────────────┼───────┼──────────────────────┤
│ Distance     │  1.0  │ Minimizar distância  │
│ Capacity     │ 1000  │ Não sobrecarregar    │
│ Autonomy     │ 1000  │ Respeitar range      │
│ Priority     │  500  │ Priorizar críticos   │
│ Balance      │   50  │ Distribuir carga     │
│ Vehicles     │  100  │ Minimizar veículos   │
└──────────────┴───────┴──────────────────────┘

Cada componente: arquivo separado (Composite Pattern)
```

---

## SLIDE 8: OPERADORES GENÉTICOS (4:45)

```
🔧 OPERADORES GENÉTICOS

1️⃣ SELEÇÃO
   └─ Tournament Selection (3 indivíduos)
   └─ Pressão seletiva média

2️⃣ CROSSOVER (70%)
   └─ Order Crossover (OX) adaptado
   └─ Preserva ordem parcial
   └─ Respeita restrições

3️⃣ MUTAÇÃO (20%)
   ├─ Swap (troca dentro da rota)
   ├─ Insertion (move posição)
   ├─ Inter-route swap (entre rotas)
   └─ Route merge (combina rotas)

4️⃣ MELHORIAS
   ├─ Busca Local (2-opt)
   ├─ Elitismo (top 5)
   └─ Early Stopping (50 gerações)
```

---

## SLIDE 9: ARQUITETURA LLM (6:45)

```
🤖 ARQUITETURA LLM

         Ollama (Local - Llama 3.2)
                   │
        ┌──────────┼──────────┐
        │          │          │
   RouteChatbot  Reporter  Analyzer
        │          │          │
   Conversação  Relatórios  Análise
   
┌────────────────────────────────────────┐
│ RouteChatbot                           │
│  └─ Perguntas em linguagem natural    │
│  └─ Respostas contextuais             │
│  └─ Usa dados reais da otimização     │
├────────────────────────────────────────┤
│ OllamaReporter                         │
│  ├─ Instruções para motoristas        │
│  ├─ Relatório diário                  │
│  ├─ Análise semanal                   │
│  └─ Relatório gerencial               │
├────────────────────────────────────────┤
│ RouteAnalyzer                          │
│  └─ Análise profunda de rotas         │
│  └─ Sugestões acionáveis              │
└────────────────────────────────────────┘
```

---

## SLIDE 10: POR QUE OLLAMA? (7:00)

```
❓ POR QUE OLLAMA?

✅ VANTAGENS:
   💰 Gratuito (sem custos de API)
   🔒 Privado (dados ficam locais)
   🌐 Offline (não precisa internet)
   ⚡ Rápido (modelo local)
   📦 Fácil (ollama pull llama3.2)

❌ ALTERNATIVAS DESCARTADAS:
   OpenAI GPT-4
   └─ Caro ($0.03 por 1k tokens)
   └─ Requer internet
   └─ Dados enviados externamente

   Google Gemini
   └─ Limitações de quota
   └─ Latência de rede

Ollama + Llama 3.2 = Melhor custo-benefício
```

---

## SLIDE 11: PROMPTS EFICIENTES (8:45)

```
📝 PROMPTS ESTRUTURADOS

Anatomia de um prompt eficiente:

┌────────────────────────────────────────┐
│ 1. CONTEXTO                            │
│    "Você é um assistente de            │
│     logística hospitalar..."           │
├────────────────────────────────────────┤
│ 2. DADOS REAIS                         │
│    "MÉTRICAS DA OTIMIZAÇÃO:            │
│     - Distância: 234.5 km              │
│     - Veículos: 3                      │
│     - Entregas críticas: 8"            │
├────────────────────────────────────────┤
│ 3. INSTRUÇÃO ESPECÍFICA                │
│    "Analise a distribuição de carga    │
│     entre os veículos e identifique    │
│     desbalanceamentos..."              │
├────────────────────────────────────────┤
│ 4. FORMATO ESPERADO                    │
│    "Responda em tópicos:               │
│     1. Análise                         │
│     2. Problemas                       │
│     3. Sugestões"                      │
└────────────────────────────────────────┘

Resultado: Respostas específicas, não genéricas
```

---

## SLIDE 12: DEMO - DASHBOARD (10:15)

```
💻 DASHBOARD PRINCIPAL

┌────────────────────────────────────────┐
│ HEADER - 5 KPIs                        │
│  📏 234.5 km  💰 R$586  🚗 3 veículos │
│  📦 20 entregas  ⚡ 8 críticas         │
├────────────────────────────────────────┤
│ MAPA INTERATIVO                        │
│  🔵 Veículo 1 (azul)                   │
│  🔴 Veículo 2 (vermelho)               │
│  🟢 Veículo 3 (verde)                  │
│  🏥 Marcadores hospitais               │
├────────────────────────────────────────┤
│ CHATBOT INTEGRADO                      │
│  💬 Perguntas em linguagem natural    │
│  🤖 Respostas com dados reais         │
│  📊 Análise e sugestões               │
└────────────────────────────────────────┘

[AQUI: MOSTRAR DEMO AO VIVO]
```

---

## SLIDE 13: COMPARATIVO (12:30)

```
📊 COMPARATIVO DE DESEMPENHO

┌──────────────┬──────────┬──────────┬────────────┐
│ Algoritmo    │ Distância│ Veículos │ Diferença  │
├──────────────┼──────────┼──────────┼────────────┤
│ GA (MINHA)   │ 234.5 km │    3     │     -      │
│ Greedy       │ 287.3 km │    4     │  +22.5% ❌ │
│ Random       │ 412.8 km │    5     │  +76.0% ❌ │
└──────────────┴──────────┴──────────┴────────────┘

💰 ECONOMIA DIÁRIA:
   GA vs Greedy: 52.8 km economizados
   52.8 km × R$2.50/km = R$132.00/dia
   
   Por mês (22 dias úteis):
   R$132 × 22 = R$2.904,00/mês 💸

⏱️ TEMPO DE EXECUÇÃO:
   GA: 15.2s (aceitável para planejamento diário)
   Greedy: 0.8s (mais rápido, muito pior)
   
CONCLUSÃO: GA compensa o tempo extra com economia
```

---

## SLIDE 14: DIFERENCIAIS (13:15)

```
🌟 DIFERENCIAIS - ALÉM DOS REQUISITOS

✅ OBRIGATÓRIOS (100%)
   ✓ Algoritmo genético VRP
   ✓ 6 componentes fitness
   ✓ Operadores genéticos
   ✓ Restrições realistas
   ✓ Integração LLM completa
   ✓ Visualização em mapas

🚀 EXTRAS (+30%)

1. ⭐⭐⭐ RASTREAMENTO TEMPO REAL
   └─ MapBox GL JS 3.0
   └─ Atualização 100ms (10 FPS)
   └─ Popups dinâmicos
   └─ Trails/rastros
   └─ Controle velocidade

2. ⭐⭐ BALANCEAMENTO DE CARGA
   └─ 6º componente fitness
   └─ Distribui equitativamente

3. ⭐⭐ BUSCA LOCAL
   └─ 2-opt + inter-route swap
   └─ Refina soluções GA

4. ⭐⭐ INTERFACE PROFISSIONAL
   └─ Design system completo
   └─ Responsivo mobile-first

5. ⭐⭐ ANÁLISE INTELIGENTE
   └─ RouteAnalyzer
   └─ Sugestões acionáveis
```

---

## SLIDE 15: CÓDIGO LIMPO (13:50)

```
👨‍💻 QUALIDADE DE CÓDIGO

PRINCÍPIOS SOLID:
  ✓ Single Responsibility
  ✓ Open/Closed
  ✓ Liskov Substitution
  ✓ Interface Segregation
  ✓ Dependency Inversion

DESIGN PATTERNS:
  ✓ Strategy (algoritmos)
  ✓ Composite (fitness)
  ✓ Factory (otimizadores)
  ✓ Observer (rastreamento)

BOAS PRÁTICAS:
  ✓ Type hints em tudo
  ✓ Docstrings completas
  ✓ Tratamento de erros
  ✓ Validações de entrada
  ✓ Separação de concerns

DOCUMENTAÇÃO:
  ✓ 25+ documentos em /docs
  ✓ README completo
  ✓ Guias de instalação
  ✓ Troubleshooting
```

---

## SLIDE 16: RESULTADOS (14:30)

```
🎯 RESULTADOS ALCANÇADOS

QUANTITATIVOS:
  ✅ 234.5 km otimizados
  ✅ R$ 586.25 custo total
  ✅ 3 veículos utilizados
  ✅ 20 entregas atendidas
  ✅ 8 entregas críticas priorizadas
  ✅ 100% restrições satisfeitas
  ✅ 22.5% melhor que Greedy
  ✅ 76% melhor que Random

QUALITATIVOS:
  ✅ Sistema completo e funcional
  ✅ Interface profissional
  ✅ Código limpo e extensível
  ✅ Documentação completa
  ✅ Pronto para uso real

CONFORMIDADE:
  ✅ 100% requisitos obrigatórios
  ✅ +30% funcionalidades extras
  ✅ Best practices aplicadas
```

---

## SLIDE 17: PRÓXIMOS PASSOS (14:45)

```
🚀 POSSÍVEIS EVOLUÇÕES

OTIMIZAÇÕES:
  🔄 Paralelização do GA (DEAP suporta)
  💾 Cache de matriz de distâncias
  🎮 GPU para cálculo de fitness
  ⚡ Compilação com Cython

FUNCIONALIDADES:
  ⏰ Janelas de tempo (time windows)
  🏢 Múltiplos depósitos
  ⛽ Pontos de reabastecimento
  📱 App mobile para motoristas

INTEGRAÇÕES:
  🗺️ OSRM para rotas reais
  📡 GPS tracking em tempo real
  📊 Dashboard gerencial web
  🔔 Notificações em tempo real

IA:
  🎓 Fine-tuning LLM para domínio
  📈 Previsão de demanda
  🔄 Otimização contínua/online
  🤝 Multi-agent learning
```

---

## SLIDE 18: CONCLUSÃO (14:50)

```
✨ CONCLUSÃO

ENTREGUE:
  ✅ Sistema completo de otimização
  ✅ Algoritmo genético robusto
  ✅ Integração LLM funcional
  ✅ Interface profissional
  ✅ Código de qualidade
  ✅ Documentação completa

APRENDIZADO:
  📚 Algoritmos evolutivos
  🤖 Integração de LLMs
  🏗️ Arquitetura SOLID
  📊 Visualização de dados
  💻 Desenvolvimento full-stack

IMPACTO:
  💰 Economia de R$132/dia
  ⚡ 8 entregas críticas priorizadas
  🚗 Uso otimizado de frota
  📉 Redução de 22.5% em distância

─────────────────────────────────────

Código: github.com/[seu-usuario]/hospital-routes
Docs: /docs/

Obrigado! 🙏
Perguntas? 💬
```

---

## 🎨 DICAS DE DESIGN

### Cores Sugeridas
- **Fundo**: Escuro (#1e1e1e ou #2d2d2d)
- **Texto**: Branco (#ffffff)
- **Destaques**: Verde (#4ade80), Azul (#3b82f6)
- **Alertas**: Vermelho (#ef4444)
- **Info**: Amarelo (#fbbf24)

### Fontes
- **Títulos**: Inter Bold ou Montserrat Bold
- **Corpo**: Inter Regular ou Roboto
- **Código**: Fira Code ou JetBrains Mono

### Layout
- **Slide 16:9** (formato widescreen)
- **Margens**: 5% em todos os lados
- **Hierarquia**: Títulos 32pt, Subtítulos 24pt, Corpo 18pt
- **Espaçamento**: Generoso, não compactar

### Elementos Visuais
- ✅ Use emojis para destacar pontos
- ✅ Use ícones em vez de bullet points quando possível
- ✅ Use caixas/boxes para agrupar informações
- ✅ Use cores para categorizar (verde=sucesso, azul=info)
- ❌ Evite muito texto por slide
- ❌ Evite animações excessivas

---

## 📱 FERRAMENTAS RECOMENDADAS

### Para Criar Slides
1. **Google Slides** (Gratuito, colaborativo)
2. **PowerPoint** (Profissional)
3. **Canva** (Templates prontos)
4. **Keynote** (Mac, design elegante)

### Para Diagramas
1. **Excalidraw** (Desenhos à mão)
2. **draw.io** (Diagramas técnicos)
3. **Lucidchart** (Profissional)

### Para Screenshots
1. **Greenshot** (Windows)
2. **Flameshot** (Linux)
3. **Snagit** (Profissional)

---

## 💡 LEMBRE-SE

### Slides SÃO:
✅ Suporte visual
✅ Guia para você
✅ Reforço de pontos-chave
✅ Estrutura da apresentação

### Slides NÃO SÃO:
❌ Roteiro completo
❌ Documentação
❌ Substituição da demo
❌ O foco principal

**A demonstração ao vivo é mais importante que os slides!**

Use slides para:
- Introduzir seções
- Mostrar conceitos teóricos
- Comparar resultados
- Resumir aprendizados

Use demo ao vivo para:
- Mostrar sistema funcionando
- Interagir com chatbot
- Visualizar rotas
- Provar que funciona

---

## 🎬 BOA APRESENTAÇÃO!

**Slides de apoio + Demo ao vivo = Apresentação perfeita! 🚀**
