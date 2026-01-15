"""
Exemplo interativo de uso do Chatbot para Operadores.

Permite que operadores façam perguntas sobre rotas otimizadas.
"""

import sys
from pathlib import Path

# Adicionar raiz do projeto ao PYTHONPATH
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from hospital_routes.llm.chatbot import RouteChatbot
from hospital_routes.llm.ollama_helper import check_ollama_running, get_best_available_model
from hospital_routes.optimization.genetic_algorithm import GeneticAlgorithmOptimizer
from seed_real_data import (
    generate_deliveries,
    generate_vehicles,
    get_optimization_config,
    get_depot_location,
)


def main():
    """Função principal do chatbot interativo."""
    print("🤖 Chatbot para Operadores - Sistema de Rotas Hospitalares")
    print("=" * 70)
    print()
    
    # Verificar Ollama
    if not check_ollama_running():
        print("❌ Ollama não está rodando.")
        print("   Certifique-se de que o Ollama está instalado e rodando.")
        return 1
    
    model = get_best_available_model()
    if not model:
        print("❌ Nenhum modelo Ollama disponível.")
        print("   Execute: ollama pull llama3.2")
        return 1
    
    print(f"✅ Ollama detectado! Modelo: {model}")
    print()
    
    # Carregar dados e otimizar
    print("📦 Carregando dados e otimizando rotas...")
    deliveries = generate_deliveries()
    vehicles = generate_vehicles()
    config = get_optimization_config()
    depot = get_depot_location()
    
    optimizer = GeneticAlgorithmOptimizer()
    result = optimizer.optimize(
        deliveries=deliveries,
        vehicles=vehicles,
        config=config,
        depot_location=depot,
    )
    
    print("✅ Otimização concluída!")
    print()
    
    # Inicializar chatbot
    print("🤖 Inicializando chatbot...")
    chatbot = RouteChatbot()
    chatbot.set_optimization_context(result)
    print("✅ Chatbot pronto!")
    print()
    
    # Loop interativo
    print("=" * 70)
    print("💬 Chatbot Ativo - Faça suas perguntas!")
    print("=" * 70)
    print()
    print("Comandos especiais:")
    print("  /help - Mostrar ajuda")
    print("  /clear - Limpar histórico")
    print("  /history - Ver histórico")
    print("  /quit ou /exit - Sair")
    print()
    print("-" * 70)
    print()
    
    while True:
        try:
            user_input = input("Você: ").strip()
            
            if not user_input:
                continue
            
            # Comandos especiais
            if user_input.lower() in ["/quit", "/exit", "/q"]:
                print("\n👋 Até logo!")
                break
            
            elif user_input.lower() == "/help":
                print("\n💡 Exemplos de perguntas:")
                print("  • Quantos veículos foram usados?")
                print("  • Qual a distância total?")
                print("  • Quais entregas são críticas?")
                print("  • Analise a eficiência das rotas")
                print("  • Há alguma melhoria possível?")
                print()
                continue
            
            elif user_input.lower() == "/clear":
                chatbot.clear_history()
                print("\n✅ Histórico limpo!")
                print()
                continue
            
            elif user_input.lower() == "/history":
                history = chatbot.get_history()
                if history:
                    print("\n📜 Histórico de conversa:")
                    for msg in history[-5:]:  # Últimas 5 mensagens
                        role_emoji = "👤" if msg.role == "user" else "🤖"
                        print(f"  {role_emoji} {msg.role}: {msg.content[:100]}...")
                else:
                    print("\n📜 Nenhuma mensagem no histórico.")
                print()
                continue
            
            # Processar pergunta
            print("\n🤖 Processando...")
            response = chatbot.chat(user_input)
            print(f"\n🤖 Assistente: {response}\n")
            print("-" * 70)
            print()
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrompido pelo usuário. Até logo!")
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
