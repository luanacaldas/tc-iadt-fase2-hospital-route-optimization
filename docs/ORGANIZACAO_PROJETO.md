# 📂 Organização do Projeto

> Estrutura reorganizada para melhor manutenibilidade e clareza

## 🎯 Mudanças Implementadas

### ✅ 1. Documentação Consolidada (`docs/`)

**Antes:** Arquivos `.md` espalhados na raiz  
**Depois:** Todos em `docs/`

```
docs/
├── COMO_EXECUTAR.md
├── COMO_RESOLVER_OLLAMA.md
├── COMO_USAR_CHATBOT.md
├── GUIA_INTERFACE_CHATBOT.md
├── GUIA_RAPIDO_CHATBOT.md
├── INSTALACAO_FLASK.md
├── README_INTERFACE.md
├── SOLUCAO_FLASK.md
├── MELHORIAS_ALGORITMO.md
├── MELHORIAS_CHATBOT.md
├── MELHORIAS_SENIOR.md
├── UX_HEADER_REDESIGN.md
└── VERIFICACAO_REQUISITOS.md
```

---

### ✅ 2. Interfaces HTML Separadas (`interfaces/`)

**Antes:** `.html` misturados na raiz  
**Depois:** Pasta dedicada `interfaces/`

```
interfaces/
├── chatbot_interface_v2.html  ⭐ Principal
├── chatbot_interface.html     (v1 - legado)
├── rastreamento_mapbox.html   🗺️ Rastreamento ao vivo
└── README.md                   Documentação das interfaces
```

**Acesso:**

- Dashboard: `python app_scripts/open_interface.py`
- Rastreamento: Clicar em "Rastrear" no dashboard

---

### ✅ 3. Scripts Executáveis (`app_scripts/`)

**Antes:** `.py` executáveis na raiz  
**Depois:** Organizados em `app_scripts/`

```
app_scripts/
├── run_chatbot_interface.py  (servidor Flask - deprecado)
├── open_interface.py         🚀 Abre HTMLs diretamente
├── run_chatbot_v2.py
├── run_demo.py
├── seed_real_data.py         🌱 Gerar dados
├── server_chatbot.py         🤖 API chatbot
├── setup_ollama.py           ⚙️ Configurar LLM
├── test_optimization.py      🧪 Testes
└── README.md                 Documentação dos scripts
```

**Uso:**

```bash
# CORRETO (novo)
python app_scripts/run_chatbot_interface.py

# INCORRETO (antigo)
python run_chatbot_interface.py  ❌
```

---

### ✅ 4. Outputs Isolados (`output/`)

**Antes:** Arquivos gerados na raiz  
**Depois:** Pasta dedicada `output/` (gitignored)

```
output/
├── route_map.html           (gerado dinamicamente)
├── driver_instructions.txt  (gerado dinamicamente)
├── route_analysis.txt       (gerado dinamicamente)
└── README.md                Documentação dos outputs
```

**Nota:** Todos arquivos em `output/` são gitignored automaticamente.

---

### ✅ 5. `.gitignore` Limpo

**Antes:** Muito restritivo (ignorava tudo)  
**Depois:** Específico e organizado

**Agora ignora:**

- ✅ Virtual env (bin/, Lib/, app_scripts/, Include/)
- ✅ Pacotes instalados (blinker/, click/, flask/, etc)
- ✅ Outputs gerados (output/_.html, output/_.txt)
- ✅ Cache Python (**pycache**/, \*.pyc)
- ✅ IDEs (.vscode/, .idea/)
- ✅ OS files (.DS_Store, Thumbs.db)

---

## 📊 Estrutura Final

```
hospital_routes/
│
├── 📁 core/              # Interfaces e modelos
├── 📁 optimization/      # Algoritmo genético
├── 📁 llm/               # Chatbot e LLMs
├── 📁 visualization/     # Geradores de mapa
├── 📁 domain/            # Entidades negócio
├── 📁 utils/             # Utilitários
├── 📁 examples/          # Exemplos de uso
│
├── 📁 interfaces/        # 🆕 HTMLs organizados
├── 📁 app_scripts/           # 🆕 Executáveis Python
├── 📁 docs/              # 🆕 Documentação consolidada
├── 📁 output/            # 🆕 Arquivos gerados
│
├── cli.py                # CLI principal (raiz OK)
├── requirements.txt      # Dependências
├── .gitignore            # ✨ Atualizado
└── README.md             # ✨ Atualizado com novos paths
```

---

## 🔄 Migração para Desenvolvedores

### Comandos Atualizados

| Antigo ❌                         | Novo ✅                                     |
| --------------------------------- | ------------------------------------------- |
| `python run_chatbot_interface.py` | `python app_scripts/open_interface.py`      |
| `python seed_real_data.py`        | `python app_scripts/seed_real_data.py`      |
| `python server_chatbot.py`        | `python app_scripts/server_chatbot.py`      |
| Abrir `rastreamento_mapbox.html`  | Abrir `interfaces/rastreamento_mapbox.html` |
| Ler `COMO_EXECUTAR.md`            | Ler `docs/COMO_EXECUTAR.md`                 |

### Imports Atualizados

Os scripts em `app_scripts/` foram atualizados com:

```python
# Antes
PROJECT_ROOT = Path(__file__).parent

# Depois
PROJECT_ROOT = Path(__file__).parent.parent  # Subir um nível
```

Isso garante que imports como `from optimization.genetic_algorithm import ...` continuem funcionando.

---

## ✅ Benefícios

1. **🧹 Raiz Limpa**: Apenas arquivos essenciais (cli.py, README.md, requirements.txt)
2. **📚 Docs Organizados**: Fácil encontrar guias e tutoriais
3. **🎨 Interfaces Separadas**: HTMLs não misturam com código Python
4. **🚀 Scripts Claros**: Executáveis em pasta dedicada
5. **📤 Outputs Isolados**: Arquivos gerados não poluem raiz
6. **🔍 Git Limpo**: .gitignore específico, sem ignorar tudo

---

## 📝 Checklist de Conformidade

- [x] Todos `.md` de docs em `docs/`
- [x] Todos `.html` em `interfaces/`
- [x] Todos scripts executáveis em `app_scripts/`
- [x] Outputs gerados em `output/`
- [x] `.gitignore` atualizado
- [x] `README.md` principal atualizado
- [x] READMEs nas subpastas criados
- [x] Paths nos scripts corrigidos
- [x] Documentação de migração criada

---

## 🎉 Status

**✅ REORGANIZAÇÃO COMPLETA!**

O projeto agora segue uma estrutura profissional, com separação clara de responsabilidades e fácil navegação.
