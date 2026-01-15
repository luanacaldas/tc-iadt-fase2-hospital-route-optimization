"""
Script simples para abrir interfaces HTML diretamente no navegador.
"""

import webbrowser
from pathlib import Path
import time

PROJECT_ROOT = Path(__file__).parent.parent
INTERFACES_DIR = PROJECT_ROOT / 'interfaces'

def main():
    print("\n" + "=" * 70)
    print("🏥 SISTEMA DE ROTAS HOSPITALARES")
    print("=" * 70)
    
    dashboard = INTERFACES_DIR / 'chatbot_interface_v2.html'
    rastreamento = INTERFACES_DIR / 'rastreamento_mapbox.html'
    
    if not dashboard.exists():
        print(f"\n❌ Dashboard não encontrado em: {dashboard}")
        return
    
    if not rastreamento.exists():
        print(f"\n❌ Rastreamento não encontrado em: {rastreamento}")
        return
    
    print("\n✅ Abrindo Dashboard...")
    webbrowser.open(f"file:///{dashboard.as_posix()}")
    
    print("✅ Dashboard aberto!")
    print("\n💡 Dicas:")
    print("   - Para abrir o Rastreamento, clique no botão 'Rastrear' no dashboard")
    print(f"   - Ou abra manualmente: file:///{rastreamento.as_posix()}")
    print("\n📝 Nota: Chatbot não funcionará sem servidor (precisa API)")
    print("   Mas você pode ver o mapa e as métricas!")
    
    print("\n" + "=" * 70)


if __name__ == '__main__':
    main()
