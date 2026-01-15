# 🎨 Guia: Interface Completa do Chatbot

## 🚀 Como Usar

### Forma Mais Simples

Execute o script principal:

```bash
python app_scripts/open_interface.py
```

> **Atenção:** Abre HTMLs localmente. Chatbot não funciona sem servidor backend.

**O que acontece:**

1. ✅ Carrega dados de hospitais
2. ✅ Executa otimização
3. ✅ Gera mapa interativo
4. ✅ Cria interface web completa
5. ✅ Abre automaticamente no navegador
6. ✅ Inicia servidor backend (se Flask instalado)

---

## 🎯 Funcionalidades da Interface

### 1. **Chatbot Interativo** (Centro)

- 💬 Chat em tempo real
- 🤖 Respostas inteligentes sobre rotas
- ⚡ Perguntas rápidas com botões
- 📜 Histórico de conversa

### 2. **Painel Esquerdo: Motoristas e Hospitais**

- 👥 **Motoristas**: Lista de todos os motoristas com:

  - Número de entregas
  - Entregas críticas
  - Peso total
  - Distância percorrida

- 🏥 **Hospitais**: Lista de todos os hospitais com:
  - ID do hospital
  - Prioridade
  - Peso da entrega
  - Localização
  - Badge de crítica/normal

### 3. **Painel Direito: Estatísticas e Medicamentos**

- 📊 **Estatísticas**:

  - Distância total
  - Custo total
  - Tempo de execução
  - Fitness score

- 💊 **Medicamentos**:
  - Medicamentos críticos (vermelho)
  - Insumos normais (azul)
  - Peso de cada item

### 4. **Mapa Integrado** (Opcional)

- 🗺️ Mapa interativo com rotas
- 🚗 Visualização de veículos
- 📍 Marcadores de hospitais
- ⚠️ Dados de acidentes

### 5. **Header com Estatísticas Rápidas**

- 🚛 Número de veículos
- 📦 Número de entregas
- ⚠️ Entregas críticas
- 📏 Distância total
- 💰 Custo total

---

## 💡 Exemplos de Perguntas

### Sobre Rotas

- "Quantos veículos foram usados?"
- "Qual a distância total?"
- "Descreva as rotas otimizadas"

### Sobre Entregas

- "Há entregas críticas?"
- "Quais hospitais serão visitados?"
- "Qual veículo tem mais entregas?"

### Análise

- "Analise a eficiência das rotas"
- "Há melhorias possíveis?"
- "Compare os veículos"

---

## 🎨 Design

A interface foi criada com:

- ✅ Design moderno e fluido
- ✅ Responsivo (funciona em diferentes tamanhos de tela)
- ✅ Animações suaves
- ✅ Cores profissionais
- ✅ Ícones Font Awesome
- ✅ Scrollbars customizadas
- ✅ Cards interativos com hover

---

## 🔧 Configuração

### Com Servidor Backend (Recomendado)

Para usar o chatbot real com Ollama:

```bash
pip install flask flask-cors
python run_chatbot_interface.py
```

O servidor Flask será iniciado automaticamente em `http://127.0.0.1:5000`.

### Sem Servidor (Standalone)

Se Flask não estiver instalado, a interface funciona com respostas simuladas baseadas em palavras-chave.

---

## 📁 Arquivos Gerados

- `chatbot_interface.html` - Interface principal
- `route_map.html` - Mapa das rotas
- Servidor Flask (se disponível) - API backend

---

## 🎯 Integração com Mapa

A interface pode incluir o mapa de duas formas:

1. **Integrado na Interface** (padrão)

   - Mapa aparece como painel na interface
   - Visualização completa das rotas
   - Interativo e responsivo

2. **Separado**
   - Mapa em arquivo separado
   - Pode ser aberto independentemente
   - Útil para impressão ou compartilhamento

---

## 🚀 Melhorias Futuras

- [ ] Gráficos de performance
- [ ] Exportação de relatórios
- [ ] Filtros e buscas
- [ ] Modo escuro
- [ ] Notificações em tempo real
- [ ] Integração com banco de dados

---

## 📚 Documentação Técnica

- **Código**: `visualization/chatbot_interface.py`
- **Servidor**: `server_chatbot.py`
- **Script Principal**: `run_chatbot_interface.py`

---

**Divirta-se usando a interface! 🎨✨**
