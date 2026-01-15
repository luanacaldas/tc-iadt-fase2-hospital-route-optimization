# 🎨 Interfaces HTML

Esta pasta contém as interfaces web do sistema.

## 📄 Arquivos

### 🎯 Interface Principal

**`chatbot_interface_v2.html`** _(Recomendado)_

- Dashboard completo com design profissional
- Header slim com 5 KPIs em tempo real
- Chatbot integrado para análise de rotas
- Mapa interativo Folium com rotas otimizadas
- Botão "Rastrear" → abre rastreamento ao vivo
- Design system com Inter font

**Como usar:**

```bash
# Iniciar servidor Flask
python scripts/run_chatbot_interface.py

# Acessar
http://localhost:5000
```

---

### 📍 Rastreamento em Tempo Real

**`rastreamento_mapbox.html`**

- Visualização MapBox GL JS 3.0
- 3 veículos simulados com movimento suave (100ms)
- Rotas completas desenhadas (LineString)
- Marcadores hospitais 🏥 interativos
- Popups dinâmicos com status, velocidade, ETA
- Trails/rastros de caminho percorrido
- Notificações toast de chegada
- Controle de velocidade (0.5x até 10x)
- Totalmente responsivo (mobile-first)

**Como abrir:**

1. Através do dashboard: Clicar no botão "Rastrear"
2. Diretamente no navegador: Abrir `interfaces/rastreamento_mapbox.html`

**Configuração MapBox:**

- Criar conta gratuita: https://account.mapbox.com/
- Copiar Access Token
- Editar linha ~650:
  ```javascript
  mapboxgl.accessToken = "SEU_TOKEN_AQUI";
  ```

---

### 📦 Interface Legado

**`chatbot_interface.html`** _(v1)_

- Versão anterior do dashboard
- Mantida para compatibilidade
- Recomendado usar `chatbot_interface_v2.html`

---

## 🎯 Funcionalidades por Interface

| Funcionalidade      | Dashboard v2 | Rastreamento | Dashboard v1 |
| ------------------- | :----------: | :----------: | :----------: |
| KPIs Header         |      ✅      |      ✅      |      ❌      |
| Chatbot Integrado   |      ✅      |      ❌      |      ✅      |
| Mapa Folium         |      ✅      |      ❌      |      ✅      |
| Rastreamento MapBox |      ❌      |      ✅      |      ❌      |
| Design Profissional |      ✅      |      ✅      |      ⚠️      |
| Mobile Responsivo   |      ✅      |      ✅      |      ⚠️      |

---

## 🚀 Recomendação de Uso

1. **Análise e Planejamento**: Use `chatbot_interface_v2.html`

   - Ver rotas otimizadas
   - Conversar com chatbot
   - Analisar métricas

2. **Monitoramento ao Vivo**: Use `rastreamento_mapbox.html`
   - Acompanhar veículos em tempo real
   - Visualizar progresso das entregas
   - Receber notificações de chegada

---

## 🛠️ Tecnologias

- **HTML5/CSS3/JavaScript ES6+**
- **MapBox GL JS 3.0** (rastreamento)
- **Folium** (via Python para mapa estático)
- **Inter Font** (Google Fonts)
- **Design System** com variáveis CSS
