# 📤 Output - Arquivos Gerados

Esta pasta contém os arquivos gerados automaticamente pelo sistema.

## 📄 Arquivos Típicos

### 🗺️ Mapas

**`route_map.html`**

- Mapa interativo com rotas otimizadas
- Gerado por: `MapGenerator` (Folium)
- Marcadores de hospitais e depósito
- Rotas coloridas por veículo
- Popups informativos

**Como gerar:**

```bash
python cli.py
# ou
python scripts/run_chatbot_interface.py
```

---

### 📋 Relatórios

**`driver_instructions.txt`**

- Instruções detalhadas para motoristas
- Gerado por: `OllamaReporter.generate_driver_instructions()`
- Contém: ordem de entregas, distâncias, tempos

**`route_analysis.txt`**

- Análise técnica das rotas
- Métricas de eficiência
- Comparações de performance

---

## 🚫 Git Ignore

Os arquivos nesta pasta são **gitignored** por padrão:

```
output/*.html
output/*.txt
output/*.json
```

**Motivo:** Arquivos gerados dinamicamente, não devem estar no controle de versão.

---

## 🔧 Localização dos Geradores

| Arquivo                   | Gerador          | Localização                      |
| ------------------------- | ---------------- | -------------------------------- |
| `route_map.html`          | `MapGenerator`   | `visualization/map_generator.py` |
| `driver_instructions.txt` | `OllamaReporter` | `llm/ollama_reporter.py`         |
| `route_analysis.txt`      | `RouteAnalyzer`  | `llm/route_analyzer.py`          |

---

## 📝 Notas

- Esta pasta é criada automaticamente na primeira execução
- Arquivos antigos podem ser sobrescritos
- Mantenha esta pasta no `.gitignore`
