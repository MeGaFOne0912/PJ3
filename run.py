#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SteamPy 3.0 - Script de Execução
Sistema de Gerenciamento de Biblioteca de Jogos
"""

import sys
import os
from pathlib import Path

def verificar_ambiente():
    """Verifica se o ambiente está configurado corretamente."""
    print("=" * 80)
    print("VERIFICANDO AMBIENTE".center(80))
    print("=" * 80)
    print()
    
    # Verifica Python
    print(f"✓ Python {sys.version.split()[0]}")
    print(f"✓ Executável: {sys.executable}")
    print()
    
    # Verifica arquivos necessários
    arquivos_necessarios = [
        "steamPy.py",
        "menu.py",
        "jogo.py",
        "filabacklog.py",
        "pilharecentes.py",
        "sessaojogo.py",
        "dataset.csv",
    ]
    
    print("Verificando arquivos necessários:")
    todos_existem = True
    for arquivo in arquivos_necessarios:
        caminho = Path(arquivo)
        if caminho.exists():
            tamanho = caminho.stat().st_size
            if tamanho > 1024*1024:
                tamanho_str = f"{tamanho / (1024*1024):.1f} MB"
            elif tamanho > 1024:
                tamanho_str = f"{tamanho / 1024:.1f} KB"
            else:
                tamanho_str = f"{tamanho} bytes"
            print(f"  ✓ {arquivo:30s} ({tamanho_str})")
        else:
            print(f"  ✗ {arquivo:30s} FALTANDO!")
            todos_existem = False
    
    print()
    
    if not todos_existem:
        print("❌ Alguns arquivos estão faltando!")
        print("Verifique se você está no diretório correto: Projeto_3-main/")
        return False
    
    print("✅ Todos os arquivos foram encontrados!")
    print()
    return True


def main():
    """Função principal."""
    os.chdir(Path(__file__).parent)
    
    if not verificar_ambiente():
        print("Pressione ENTER para sair...")
        input()
        sys.exit(1)
    
    print("Iniciando SteamPy...")
    print()
    
    # Importa e executa o programa
    try:
        from projeto3 import main as steampy_main
        steampy_main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrompido.")
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
