"""
Script para configurar Ollama automaticamente.

Verifica se Ollama está rodando e instala modelo se necessário.
"""

import subprocess
import sys


def check_ollama_running() -> bool:
    """Verifica se Ollama está rodando."""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def list_models() -> list:
    """Lista modelos instalados."""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split("\n")[1:]  # Pular cabeçalho
            models = []
            for line in lines:
                if line.strip():
                    model_name = line.split()[0]
                    models.append(model_name)
            return models
        return []
    except Exception:
        return []


def install_model(model_name: str = "llama3.2") -> bool:
    """Instala um modelo Ollama."""
    print(f"📥 Instalando modelo '{model_name}'...")
    print("   (Isso pode levar alguns minutos dependendo da sua conexão)")
    print()
    
    try:
        process = subprocess.Popen(
            ["ollama", "pull", model_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        
        # Mostrar progresso
        for line in process.stdout:
            print(f"   {line.strip()}")
        
        process.wait()
        return process.returncode == 0
    except Exception as e:
        print(f"❌ Erro ao instalar modelo: {e}")
        return False


def main():
    """Função principal."""
    print("🔧 Configuração do Ollama")
    print("=" * 70)
    print()
    
    # Verificar se Ollama está rodando
    print("1️⃣ Verificando se Ollama está rodando...")
    if not check_ollama_running():
        print("❌ Ollama não está rodando!")
        print()
        print("💡 Para resolver:")
        print("   1. Instale o Ollama: https://ollama.ai/download")
        print("   2. Inicie o Ollama (geralmente inicia automaticamente)")
        print("   3. Execute este script novamente")
        return 1
    
    print("✅ Ollama está rodando!")
    print()
    
    # Listar modelos instalados
    print("2️⃣ Verificando modelos instalados...")
    models = list_models()
    
    if models:
        print(f"✅ Modelos encontrados: {', '.join(models)}")
        print()
        print("🎉 Tudo pronto! Você pode usar o sistema agora.")
        return 0
    else:
        print("⚠️  Nenhum modelo instalado.")
        print()
        
        # Perguntar se quer instalar
        print("3️⃣ Instalar modelo recomendado (llama3.2)?")
        print()
        print("   Este modelo é:")
        print("   - Pequeno e rápido (~2GB)")
        print("   - Boa qualidade para português")
        print("   - Ideal para chatbot e análises")
        print()
        
        resposta = input("   Instalar agora? (s/n): ").strip().lower()
        
        if resposta in ["s", "sim", "y", "yes"]:
            print()
            if install_model("llama3.2"):
                print()
                print("✅ Modelo instalado com sucesso!")
                print()
                print("🎉 Agora você pode usar:")
                print("   - Chatbot para operadores")
                print("   - Análise inteligente de rotas")
                print("   - Geração de relatórios")
                return 0
            else:
                print()
                print("❌ Erro ao instalar modelo.")
                print()
                print("💡 Tente instalar manualmente:")
                print("   ollama pull llama3.2")
                return 1
        else:
            print()
            print("ℹ️  Instalação cancelada.")
            print()
            print("💡 Para instalar manualmente, execute:")
            print("   ollama pull llama3.2")
            print()
            print("   Ou outros modelos:")
            print("   ollama pull llama3.1")
            print("   ollama pull mistral")
            print("   ollama pull phi3")
            return 0


if __name__ == "__main__":
    sys.exit(main())
