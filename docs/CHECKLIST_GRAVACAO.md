# 📋 Checklist de Gravação - Imprima Esta Página

## ⏰ TIMING (Cole ao lado da tela)

```
┌─────────────────────────────────────┐
│  0:00 ┃ INÍCIO                      │
│  1:30 ┃ ARQUITETURA                 │
│  3:00 ┃ ALGORITMO GENÉTICO          │
│  6:30 ┃ INTEGRAÇÃO LLM              │
│  9:30 ┃ DEMONSTRAÇÃO                │
│ 13:00 ┃ DIFERENCIAIS                │
│ 14:30 ┃ CONCLUSÃO                   │
│ 15:00 ┃ FIM                         │
└─────────────────────────────────────┘
```

---

## ✅ ANTES DE GRAVAR

### Ambiente Técnico
- [ ] Ollama rodando (`ollama list`)
- [ ] Modelo llama3.2 instalado
- [ ] Porta 5000 livre (`lsof -i :5000`)
- [ ] Token MapBox configurado
- [ ] Python venv ativado

### Sistema Testado
- [ ] Dashboard abre (`python app_scripts/run_chatbot_interface.py`)
- [ ] Chatbot responde
- [ ] Rastreamento MapBox carrega
- [ ] Mapa Folium aparece
- [ ] Sem erros no console

### Setup de Gravação
- [ ] Tela limpa (fechar abas extras)
- [ ] Tema escuro ativado
- [ ] Fonte código aumentada (18pt+)
- [ ] Áudio testado
- [ ] Vídeo testado
- [ ] Timer visível (15min)
- [ ] Água por perto 💧

---

## 💬 PERGUNTAS PARA CHATBOT (Copie/Cole)

```
1. Quantos veículos foram usados?

2. Há entregas críticas?

3. Analise a eficiência das rotas

4. Sugira melhorias

5. Compare os veículos
```

---

## 🎯 NÚMEROS IMPORTANTES (Memorize)

```
234.5 km    = Distância otimizada
R$ 586.25   = Custo total
3 veículos  = Quantidade usada
20 entregas = Total
8 críticas  = Prioridade 1

Comparativo:
GA: 234.5 km (melhor)
Greedy: 287.3 km (+22.5%)
Random: 412.8 km (+76.0%)
```

---

## 🌟 DIFERENCIAIS (Enfatize!)

```
⭐⭐⭐ Rastreamento Tempo Real (MapBox)
⭐⭐ Balanceamento de Carga
⭐⭐ Busca Local (2-opt)
⭐⭐ Interface Profissional
⭐⭐ Análise Inteligente
```

---

## 🧬 FITNESS = 6 COMPONENTES

```
1. Distância      (1.0)
2. Capacidade     (1000) ← alto
3. Autonomia      (1000) ← alto
4. Prioridade     (500)
5. Balanceamento  (50)
6. Veículos       (100)
```

---

## 🤖 LLM = 3 COMPONENTES

```
1. RouteChatbot    → Conversação
2. OllamaReporter  → Relatórios
3. RouteAnalyzer   → Análise
```

---

## 🚨 SE ALGO DER ERRADO

### Ollama não responde
```bash
ollama serve
# Nova janela:
ollama list
```

### Porta ocupada
```bash
kill -9 $(lsof -ti:5000)
```

### Chatbot lento
- Normal! LLM leva 5-10s
- Mencionar: "LLM está processando..."

### MapBox não carrega
- Verificar token
- Linha ~650 em rastreamento_mapbox.html

---

## 🎤 FRASES-CHAVE

### Abertura (0:00)
> "Sistema de Otimização de Rotas Hospitalares
> com Algoritmos Genéticos e LLMs"

### Fitness (3:45)
> "6 componentes modulares, cada um em
> arquivo separado (Composite Pattern)"

### Chatbot (7:15)
> "Usa dados reais, não respostas genéricas"

### Rastreamento (11:30)
> "Rastreamento tempo real - além dos requisitos
> - 100ms updates, movimento suave"

### Comparativo (12:30)
> "GA economiza 52km = R$132/dia vs Greedy"

### Conclusão (14:30)
> "100% requisitos + 30% extras
> Código SOLID, pronto para produção"

---

## ⏰ CHECKPOINTS

```
3:00  → Devo estar no GA
6:00  → Devo estar no LLM
9:00  → Devo iniciar DEMO
12:00 → Devo estar em Diferenciais
15:00 → ENCERRAR
```

### Se Estiver Atrasado
- Pule detalhes de código
- Vá direto para demo
- Menos teoria, mais prática

### Se Estiver Adiantado
- Detalhe diferenciais
- Mostre mais código
- Explique SOLID

---

## 📱 COMANDOS (Terminal)

```bash
# Iniciar Dashboard
python app_scripts/run_chatbot_interface.py

# Navegador
http://localhost:5000
```

---

## 🎬 DURANTE A GRAVAÇÃO

### Lembre-se
- [ ] Respirar fundo
- [ ] Falar devagar
- [ ] Pausar entre seções
- [ ] Usar números (234km, não "bastante")
- [ ] Mostrar entusiasmo
- [ ] Destacar diferenciais

### Evite
- [ ] Falar rápido demais
- [ ] Dizer "uhm", "tipo", "né"
- [ ] Palavras genéricas
- [ ] Desculpas por erros
- [ ] Criticar próprio código

---

## ✅ APÓS GRAVAR

- [ ] Assistir gravação completa
- [ ] Verificar áudio claro
- [ ] Verificar vídeo nítido
- [ ] Tempo até 15:00
- [ ] Sem erros técnicos graves
- [ ] Demonstração funcionou

### Se Precisar Regravar
- [ ] Normal! Profissionais fazem várias takes
- [ ] Gravar seções separadas OK
- [ ] Editar depois OK

---

## 🎯 ESTRUTURA RESUMIDA

```
1. INTRO (1:30)
   → Problema + Solução + Stack

2. ARQUITETURA (1:30)
   → Módulos + SOLID + Patterns

3. GA (3:30)
   → Representação + Fitness + Operadores

4. LLM (3:00)
   → Chatbot + Relatórios + Prompts

5. DEMO (3:30) ⭐ MAIS IMPORTANTE
   → Dashboard + Chatbot + Rastreamento

6. DIFERENCIAIS (1:30)
   → 8 funcionalidades extras

7. CONCLUSÃO (0:30)
   → Resultados + Próximos passos
```

---

## 💡 ÚLTIMO LEMBRETE

**DEMONSTRAÇÃO AO VIVO > TEORIA**

```
✅ Mostrar funcionando
✅ Interagir com chatbot
✅ Ver rotas no mapa
✅ Rastrear veículos

É mais convincente que slides!
```

---

## 🚀 VOCÊ CONSEGUE!

```
┌────────────────────────────────────┐
│                                    │
│  Seu projeto está INCRÍVEL!        │
│                                    │
│  Você domina o código.             │
│                                    │
│  Respire. Relaxe. Comece.          │
│                                    │
│  🎬 BOA GRAVAÇÃO! 🚀              │
│                                    │
└────────────────────────────────────┘
```

---

**IMPRIMA ESTA PÁGINA E COLE AO LADO DO MONITOR** 📋
