"""
STEAMPY - Sistema de Gerenciamento de Biblioteca de Jogos
Ponto de entrada principal do programa

Este arquivo configura o caminho e executa o menu interativo do SteamPy.
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório atual ao PYTHONPATH
projeto_path = Path(__file__).resolve().parent
sys.path.insert(0, str(projeto_path))

from menu import MenuSteamPy

def main():
    """
    Função principal que inicia o sistema SteamPy.
    """
    print("\n" + "="*80)
    print("🎮 BEM-VINDO AO STEAMPY 3.0".center(80))
    print("Sistema de Gerenciamento de Biblioteca de Jogos".center(80))
    print("="*80 + "\n")
    
    try:
        menu = MenuSteamPy()
        
        # Tenta carregar dataset automaticamente
        dataset_path = Path(projeto_path) / "dataset.csv"
        if dataset_path.exists():
            print("📂 Carregando catálogo automaticamente...\n")
            if menu.steampy.carregarJogos("dataset.csv"):
                menu.jogos_carregados = True
            print()
        
        menu.executar()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrompido pelo usuário.")
        print("💾 Obrigado por usar SteamPy!\n")
    except ImportError as e:
        print(f"\n❌ ERRO DE IMPORTAÇÃO: {e}")
        print("Por favor, verifique se os arquivos estão nos diretórios corretos.")
        print(f"Caminho esperado: {projeto_path}\n")
    except Exception as e:
        print(f"\n❌ ERRO INESPERADO: {e}")
        print("Se o problema persistir, consulte a documentação.\n")


if __name__ == "__main__":
    main()
