# 🎬 Guia Rápido - Gravação do Vídeo

## ⏱️ TIMING RÁPIDO

| Min | Seção | O Que Mostrar |
|-----|-------|--------------|
| 0-2 | Intro + Arquitetura | Problema, stack, estrutura |
| 2-6 | Algoritmo Genético | Representação, fitness, operadores |
| 6-9 | LLM | Chatbot, relatórios, prompts |
| 9-13 | DEMO | Dashboard + Chatbot + Rastreamento |
| 13-15 | Diferenciais + Conclusão | O que foi além + resultados |

---

## 🚀 COMANDOS PARA DEMONSTRAÇÃO

### Antes de Gravar
```bash
# 1. Verificar Ollama
ollama list

# 2. Verificar porta livre
lsof -i :5000  # deve estar vazia

# 3. Ativar ambiente (se necessário)
source bin/activate  # Linux/Mac
.\Scripts\activate   # Windows
```

### Durante o Vídeo
```bash
# Terminal 1: Iniciar Dashboard
python app_scripts/run_chatbot_interface.py

# Aguardar mensagem: "Running on http://127.0.0.1:5000"

# Navegador: http://localhost:5000
```

---

## 💬 PERGUNTAS PARA CHATBOT (DEMO)

Cole essas perguntas no chatbot durante o vídeo:

1. **"Quantos veículos foram usados?"**
   - Mostra resposta com dados específicos

2. **"Há entregas críticas?"**
   - Lista hospitais com prioridade 1

3. **"Analise a eficiência das rotas"**
   - Análise detalhada de distribuição

4. **"Sugira melhorias"**
   - Sugestões específicas baseadas em dados

5. **"Compare os veículos"**
   - Comparação de carga e distância

---

## 🎯 DIFERENCIAIS (Enfatizar!)

### 1. Rastreamento Tempo Real ⭐⭐⭐
- MapBox GL JS 3.0
- 100ms updates (10 FPS)
- Popups dinâmicos
- Trails/rastros
- Controle velocidade

### 2. Balanceamento de Carga ⭐⭐
- 6º componente fitness
- Distribui equitativamente
- LoadBalancePenalty

### 3. Busca Local ⭐⭐
- 2-opt + inter-route swap
- Refina soluções GA

### 4. Interface Profissional ⭐⭐
- Design system completo
- Header KPIs
- Responsivo

### 5. Análise Inteligente ⭐⭐
- RouteAnalyzer
- Sugestões acionáveis

---

## 📊 NÚMEROS IMPORTANTES

### Métricas da Solução
- **234.5 km** - Distância total otimizada
- **R$ 586.25** - Custo estimado
- **3 veículos** - Número usado
- **20 entregas** - Total
- **8 críticas** - Prioridade 1

### Comparativo
| Algoritmo | Distância | Veículos | Diferença |
|-----------|-----------|----------|-----------|
| GA (meu) | 234.5 km | 3 | - |
| Greedy | 287.3 km | 4 | +22.5% |
| Random | 412.8 km | 5 | +76.0% |

### Performance
- **15.2s** - Tempo execução GA (100 gerações)
- **100ms** - Intervalo atualização rastreamento
- **50** - Gerações para early stopping

---

## 🧬 ALGORITMO GENÉTICO - PONTOS CHAVE

### Representação
```python
[["H001", "H003"], ["H002"], ["H004", "H005"]]
# Lista de listas = VRP (não apenas TSP)
```

### Fitness (6 componentes)
1. **Distância** (1.0) - base
2. **Capacidade** (1000) - penalidade alta
3. **Autonomia** (1000) - penalidade alta
4. **Prioridade** (500) - média
5. **Balanceamento** (50) - baixa
6. **Veículos** (100) - média

### Operadores
- **Seleção**: Tournament (3 indivíduos)
- **Crossover**: Order Crossover adaptado (70%)
- **Mutação**: 4 tipos (Swap, Insertion, Inter-route, Merge) (20%)

---

## 🤖 LLM - PONTOS CHAVE

### Por Que Ollama?
- ✅ Gratuito
- ✅ Local (privado)
- ✅ Sem internet
- ✅ Fácil instalação
- ✅ Performance adequada

### 3 Componentes
1. **RouteChatbot** - Análise conversacional
2. **OllamaReporter** - Relatórios automáticos
3. **RouteAnalyzer** - Análise inteligente

### 4 Relatórios
1. Instruções motoristas
2. Resumo diário
3. Análise semanal
4. Relatório gerencial

---

## 🎨 FLUXO DO DASHBOARD

1. **Abrir** `http://localhost:5000`
2. **Mostrar Header** - 5 KPIs
3. **Mostrar Mapa** - Rotas coloridas
4. **Chatbot** - 4-5 perguntas
5. **Rastrear** - Abrir rastreamento MapBox
6. **Velocidade** - Mudar para 5x
7. **Notificações** - Mostrar toast

---

## 📁 ARQUIVOS IMPORTANTES

### Para Mostrar no Vídeo
```
optimization/genetic_algorithm.py  # GA principal
optimization/fitness/composite_fitness.py  # Fitness 6 componentes
llm/chatbot.py  # Chatbot
llm/ollama_reporter.py  # Relatórios
interfaces/rastreamento_mapbox.html  # Rastreamento
docs/VERIFICACAO_REQUISITOS.md  # Conformidade
```

### Estrutura
```
hospital_routes/
├── core/           # Interfaces SOLID
├── optimization/   # GA + fitness
├── llm/           # Chatbot + relatórios
├── visualization/ # Mapas
└── interfaces/    # Web UI
```

---

## ✅ REQUISITOS (Checklist Mental)

### Algoritmo Genético
- [x] Resolve VRP (não apenas TSP)
- [x] Representação genética (List[List[str]])
- [x] 3 operadores (seleção, crossover, mutação)
- [x] Função fitness (6 componentes)
- [x] Restrições: capacidade, autonomia, prioridade, múltiplos veículos
- [x] Visualização em mapa

### LLM
- [x] Instruções para motoristas
- [x] Relatórios diários/semanais
- [x] Sugestões de melhorias
- [x] Prompts eficientes
- [x] Linguagem natural (chat)

---

## 🎤 FRASES-CHAVE

### Abertura
> "Vou apresentar meu Sistema de Otimização de Rotas Hospitalares que resolve o Vehicle Routing Problem usando Algoritmos Genéticos com integração de LLMs."

### Fitness
> "A função fitness tem 6 componentes modulares, cada um em seu arquivo separado seguindo Composite Pattern."

### LLM
> "O chatbot usa dados reais da otimização, não respostas genéricas - ele sabe exatamente quais são as entregas críticas."

### Rastreamento
> "Este rastreamento em tempo real foi além dos requisitos - atualiza a cada 100ms com movimento suave e popups dinâmicos."

### Comparativo
> "O Algoritmo Genético economiza 52km por dia comparado ao Greedy, o que representa cerca de R$130 de economia diária."

### Conclusão
> "Entreguei 100% dos requisitos obrigatórios e implementei 30% de funcionalidades extras, sempre seguindo princípios SOLID e design patterns."

---

## 🚨 PROBLEMAS COMUNS

### Ollama não está rodando
```bash
ollama serve
# Nova janela
ollama list
```

### Porta 5000 ocupada
```bash
# Mudar porta em run_chatbot_interface.py
# Ou matar processo:
kill -9 $(lsof -ti:5000)
```

### MapBox não carrega
- Verificar token em `interfaces/rastreamento_mapbox.html`
- Linha ~650: `mapboxgl.accessToken = "..."`

### Chatbot demora
- Normal, LLM processa ~5-10s
- Mostrar que está "pensando"

---

## 🎯 TIMING DETALHADO POR SEÇÃO

### Seção 1: Introdução (0:00 - 1:30)
- 0:00-0:30: Problema e contexto
- 0:30-1:00: Visão geral (slide)
- 1:00-1:30: Requisitos atendidos

### Seção 2: Arquitetura (1:30 - 3:00)
- 1:30-2:00: Estrutura de módulos
- 2:00-2:30: SOLID e patterns
- 2:30-3:00: Tecnologias

### Seção 3: GA (3:00 - 6:30)
- 3:00-3:45: Representação genética
- 3:45-4:45: Fitness (6 componentes)
- 4:45-5:45: Operadores genéticos
- 5:45-6:30: Melhorias (busca local, elitismo)

### Seção 4: LLM (6:30 - 9:30)
- 6:30-7:15: Arquitetura LLM
- 7:15-8:00: Chatbot
- 8:00-8:45: Relatórios
- 8:45-9:30: Prompts

### Seção 5: DEMO (9:30 - 13:00)
- 9:30-10:00: Iniciar sistema
- 10:00-10:45: Dashboard
- 10:45-11:30: Chatbot interativo
- 11:30-12:15: Rastreamento tempo real
- 12:15-13:00: Comparativo

### Seção 6: Diferenciais (13:00 - 14:30)
- 13:00-13:45: O que foi além
- 13:45-14:30: Qualidade código

### Seção 7: Conclusão (14:30 - 15:00)
- 14:30-14:50: Resultados
- 14:50-15:00: Próximos passos

---

## 💡 DICAS FINAIS

### Visual
- ✅ Fonte grande (18pt+ no código)
- ✅ Tema escuro (mais profissional)
- ✅ Cursor destacado
- ✅ Tela limpa (fechar abas extras)

### Verbal
- ✅ Falar devagar e claro
- ✅ Pausar entre seções
- ✅ Mostrar entusiasmo
- ✅ Ser específico (números!)

### Técnico
- ✅ Testar tudo antes
- ✅ Ter backup (screenshots)
- ✅ Timer visível
- ✅ Comandos prontos

### Conteúdo
- ✅ Código real > teoria
- ✅ Demo > slides
- ✅ Específico > genérico
- ✅ Números > adjetivos

---

## 🎬 ORDEM DE GRAVAÇÃO SUGERIDA

1. **Grave seções teóricas primeiro** (1-4)
   - Mais fácil de repetir se errar
   - Não depende de demo funcionando

2. **Grave demo separadamente** (5)
   - Pode dar erro, melhor isolado
   - Editar depois se necessário

3. **Grave diferenciais e conclusão** (6-7)
   - Já tem contexto das seções anteriores

4. **Edite e combine**
   - Cortar pausas longas
   - Adicionar transições
   - Verificar timing total

---

## ⏰ CONTROLE DE TEMPO

Use timer visível e checkpoint a cada 3 minutos:

- ✅ **3:00** - Acabei arquitetura? (deveria estar em GA)
- ✅ **6:00** - Acabei operadores GA? (deveria estar em LLM)
- ✅ **9:00** - Acabei prompts? (deveria iniciar demo)
- ✅ **12:00** - Acabei rastreamento? (deveria ir para diferenciais)
- ✅ **15:00** - Encerramento

Se estiver atrasado:
- Pule detalhes de código
- Vá direto para demo
- Reduza teoria, aumente prática

Se estiver adiantado:
- Detalhe mais os diferenciais
- Mostre mais código
- Responda perguntas antecipadas

---

## 📋 CHECKLIST FINAL

### Antes de Apertar REC
- [ ] Timer iniciado
- [ ] Tela limpa
- [ ] Ollama rodando
- [ ] Dashboard testado
- [ ] Chatbot funcionando
- [ ] Rastreamento carregando
- [ ] Áudio testado
- [ ] Enquadramento OK

### Durante Gravação
- [ ] Respirar fundo
- [ ] Falar devagar
- [ ] Mostrar confiança
- [ ] Usar números
- [ ] Destacar diferenciais

### Depois de Gravar
- [ ] Verificar áudio
- [ ] Verificar vídeo
- [ ] Conferir tempo (até 15min)
- [ ] Adicionar intro/outro (opcional)
- [ ] Upload YouTube/Vimeo

---

**🚀 Você consegue! Seu projeto está incrível!**
