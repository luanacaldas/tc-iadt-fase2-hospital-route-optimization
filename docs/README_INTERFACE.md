# 🎨 Interface Completa do Chatbot - Guia Rápido

## 🚀 Como Usar (1 comando!)

```bash
python app_scripts/open_interface.py
```

**Pronto!** O dashboard abrirá automaticamente no seu navegador.

> **Nota:** O chatbot interativo não funcionará sem servidor backend. Use para visualizar mapa, KPIs e layout.

---

## ✨ O Que Você Vai Ver

### 🎯 Layout Completo

```
┌─────────────────────────────────────────────────────────┐
│  Header: Estatísticas Rápidas (Veículos, Entregas...)  │
├──────────────────────────────────────┬───────────────────┤
│                                      │                   │
│  SIDEBAR CHAT (ESQUERDA)            │                   │
│  - Botão flutuante inferior esq.    │   MAPA INTEGRADO  │
│  - Painel colapsável                │   (DIREITA)       │
│  - Área de mensagens                │                   │
│  - Input + Botões rápidos           │   Rotas otimizadas│
│                                      │   Marcadores      │
│                                      │   Interativo      │
│                                      │                   │
└──────────────────────────────────────┴───────────────────┘
```

### 📋 Funcionalidades

1. **💬 Chatbot Interativo**

   - Respostas inteligentes sobre rotas
   - Histórico de conversa
   - Animações suaves

2. **👥 Painel de Motoristas**

   - Lista todos os motoristas
   - Entregas por motorista
   - Distâncias e pesos

3. **🏥 Painel de Hospitais**

   - Todos os hospitais
   - Prioridades e localizações
   - Badges de crítico/normal

4. **💊 Painel de Medicamentos**

   - Medicamentos críticos (vermelho)
   - Insumos normais (azul)
   - Organização por prioridade

5. **📊 Estatísticas**

   - Distância total
   - Custo total
   - Tempo de execução
   - Fitness score

6. **🗺️ Mapa Integrado**
   - Visualização completa das rotas
   - Marcadores interativos
   - Dados de acidentes

---

## 💡 Exemplos de Perguntas

### Básicas

- "Quantos veículos foram usados?"
- "Qual a distância total?"
- "Há entregas críticas?"

### Análise

- "Analise a eficiência das rotas"
- "Há melhorias possíveis?"
- "Compare os veículos"

### Específicas

- "Qual veículo tem mais entregas?"
- "Quais hospitais serão visitados?"
- "Há violações de restrições?"

---

## 🔧 Configuração

### Modo de Visualização (Atual)

```bash
python app_scripts/open_interface.py
```

Abre os HTMLs diretamente no navegador:

- ✅ Mapa interativo funciona
- ✅ KPIs e estatísticas funcionam
- ✅ Layout e design funcionam
- ❌ Chatbot requer servidor backend (não disponível no modo arquivo)

### Com Chatbot Real (Requer Servidor Flask)

Para habilitar o chatbot interativo, seria necessário:

1. Configurar servidor Flask
2. Resolver problemas de roteamento
3. Conectar com Ollama

_Atualmente em desenvolvimento._

### Sem Flask (Standalone)

A interface funciona mesmo sem Flask, usando respostas simuladas baseadas em palavras-chave.

---

## 🎨 Design

- ✅ **Moderno**: Design limpo e profissional
- ✅ **Responsivo**: Funciona em diferentes tamanhos de tela
- ✅ **Fluido**: Animações suaves e transições
- ✅ **Interativo**: Cards com hover, scrollbars customizadas
- ✅ **Colorido**: Cores profissionais e badges informativos

---

## 📁 Arquivos

- `run_chatbot_interface.py` - Script principal
- `visualization/chatbot_interface.py` - Gerador de interface
- `server_chatbot.py` - Servidor backend (opcional)
- `chatbot_interface.html` - Interface gerada
- `route_map.html` - Mapa gerado

---

## 🐛 Troubleshooting

### Interface não abre

- Verifique se o navegador padrão está configurado
- Abra manualmente: `chatbot_interface.html`

### Chatbot não responde

- Verifique se Ollama está rodando: `ollama list`
- Instale Flask: `pip install flask flask-cors`
- Verifique o console do navegador (F12) para erros

### Mapa não aparece

- Verifique se `route_map.html` foi gerado
- Tente abrir o mapa separadamente

---

## 🚀 Próximos Passos

1. Execute: `python run_chatbot_interface.py`
2. Explore a interface
3. Faça perguntas no chatbot
4. Visualize os dados nos painéis
5. Interaja com o mapa

---

**Divirta-se! 🎉**
