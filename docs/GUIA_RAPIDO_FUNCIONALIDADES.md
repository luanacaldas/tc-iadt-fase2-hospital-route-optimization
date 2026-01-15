# 🚀 Guia Rápido: Funcionalidades da Interface

## 📋 Como Usar

### 1. 📅 Timeline de Entregas
- **Como acessar**: Clique no botão **"📅 Timeline"** no header da interface
- **O que mostra**:
  - Cronograma visual de todas as entregas
  - Horários estimados de chegada
  - Status de cada entrega (dentro do prazo, próximo ao limite, atrasada)
  - Informações do veículo e localização
- **Funcionalidades**:
  - Visualizar todas as entregas em ordem cronológica
  - Ver estatísticas de pontualidade
  - Exportar timeline (botão "Exportar")

### 2. ⚖️ Comparação de Cenários
- **Como acessar**: Clique no botão **"⚖️ Comparar"** no header da interface
- **O que mostra**:
  - Comparação entre a solução atual, algoritmo Greedy e Baseline
  - Métricas: distância total, custo, veículos usados, tempo, violações
  - Economia gerada (R$ e percentual)
  - CO₂ evitado
- **Funcionalidades**:
  - Visualizar gráficos comparativos (em desenvolvimento)
  - Exportar relatório de comparação

### 3. 📍 Rastreamento em Tempo Real (Simulado)
- **Como acessar**: Clique no botão **"📍 Rastrear"** no header da interface
- **O que mostra**:
  - Status de cada veículo em tempo real
  - Próxima parada
  - Distância até o destino
  - ETA (tempo estimado de chegada)
  - Velocidade atual
  - Barra de progresso da rota
- **Funcionalidades**:
  - Atualização automática a cada 5 segundos
  - Contatar motorista (placeholder)
  - Atualizar localização (placeholder)

### 4. 📥 Exportar Relatórios
- **Como acessar**: Clique no botão **"📥 Exportar"** no header da interface
- **Formatos disponíveis**:
  - **PDF Executivo**: Relatório resumido para gestão
  - **PDF Motoristas**: Instruções detalhadas por veículo
  - **Excel**: Planilha completa com todos os dados
  - **JSON/API**: Dados estruturados para integração
- **Funcionalidades**:
  - Exportar em múltiplos formatos
  - Download automático (em produção)

## 🎯 Dicas de Uso

1. **Timeline**: Use para verificar se todas as entregas estão dentro do prazo
2. **Comparação**: Use para justificar a otimização e mostrar economia
3. **Rastreamento**: Use para monitorar veículos em tempo real durante a execução
4. **Exportação**: Use para compartilhar relatórios com equipes e gestores

## ⚠️ Notas Importantes

- As funcionalidades de **Rastreamento** e **Exportação** estão usando dados simulados
- Em produção, essas funcionalidades se conectarão ao backend para dados reais
- Todos os formatos de exportação são **gratuitos** e usam bibliotecas open-source

## 🔧 Solução de Problemas

Se os botões não funcionarem:
1. Verifique se o servidor Flask está rodando (`python run_chatbot_v2.py`)
2. Abra o console do navegador (F12) para ver erros JavaScript
3. Certifique-se de que todos os modais estão definidos no HTML
