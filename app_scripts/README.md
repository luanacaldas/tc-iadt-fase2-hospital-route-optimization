# 🚀 Scripts de Execução

Esta pasta contém os scripts executáveis do projeto.

## 📋 Scripts Disponíveis

### 🎨 Interface Web

```bash
# Servidor principal com dashboard completo
python scripts/run_chatbot_interface.py
# Acesse: http://localhost:5000
```

### 🤖 Chatbot API

```bash
# Servidor backend apenas (API REST)
python scripts/server_chatbot.py
# API: http://localhost:5000/api/chat
```

### 🌱 Dados de Teste

```bash
# Gerar dados realistas de hospitais de São Paulo
python scripts/seed_real_data.py
```

### ⚙️ Configuração

```bash
# Configurar e testar Ollama
python scripts/setup_ollama.py
```

### 🧪 Testes

```bash
# Testar otimização
python scripts/test_optimization.py
```

### 🎬 Demo

```bash
# Executar demonstração completa
python scripts/run_demo.py
```

---

## ⚡ Início Rápido

**Opção 1: Interface Completa** (Recomendado)
```bash
python scripts/run_chatbot_interface.py
```

**Opção 2: CLI Simples**
```bash
python cli.py
```

---

## 📝 Notas

- Todos os scripts assumem que você está no diretório raiz do projeto
- Certifique-se de ter o ambiente virtual ativado
- Ollama deve estar rodando para funcionalidades de chatbot
