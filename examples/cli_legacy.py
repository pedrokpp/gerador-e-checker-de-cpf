#!/usr/bin/env python3
"""
Exemplo de CLI para geração e validação de CPF (estilo legado v2.x).

Este script demonstra o uso da API legada (checar/gerar) que mantém
100% de compatibilidade com a versão 2.x.

Uso:
    python examples/cli_legacy.py
"""

import os
import sys

# Permite importar cpf mesmo rodando de examples/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import cpf


def clear_screen():
    """Limpa a tela do terminal (cross-platform)."""
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    clear_screen()
    
    print("""
    ╔════════════════════════════════════════╗
    ║   Gerador e Validador de CPF v3.0.0   ║
    ║        (Modo Legado - API v2.x)       ║
    ╚════════════════════════════════════════╝
    
    Escolha uma opção:
    
    1. Gerar CPFs
    2. Validar um CPF
    3. Sair
    """)
    
    escolha = input("Opção: ").strip()
    
    if escolha == "1":
        gerar_cpfs()
    elif escolha == "2":
        validar_cpf()
    elif escolha == "3":
        print("\n👋 Até logo!\n")
        sys.exit(0)
    else:
        print("\n❌ Opção inválida! Tente novamente.\n")
        input("Pressione ENTER para continuar...")
        main()


def gerar_cpfs():
    """Menu para gerar CPFs."""
    clear_screen()
    print("\n=== GERAR CPFs ===\n")
    
    # Quantidade
    while True:
        try:
            quantidade = input("Quantos CPFs deseja gerar? (padrão: 1): ").strip()
            quantidade = int(quantidade) if quantidade else 1
            if quantidade < 1:
                print("❌ Quantidade deve ser pelo menos 1!")
                continue
            break
        except ValueError:
            print("❌ Por favor, digite um número válido!")
    
    # Região
    print("\nRegiões disponíveis:")
    print("  -1: Aleatória (padrão)")
    print("   0: Rio Grande do Sul")
    print("   1: DF, GO, MS, MT, TO")
    print("   2: AC, AM, AP, PA, RO, RR")
    print("   3: CE, MA, PI")
    print("   4: AL, PB, PE, RN")
    print("   5: BA, SE")
    print("   6: MG")
    print("   7: ES, RJ")
    print("   8: SP")
    print("   9: PR, SC")
    
    while True:
        try:
            regiao = input("\nQual região? (ENTER para aleatória): ").strip()
            regiao = int(regiao) if regiao else -1
            if regiao < -1 or regiao > 9:
                print("❌ Região deve ser entre -1 e 9!")
                continue
            break
        except ValueError:
            print("❌ Por favor, digite um número válido!")
    
    # Gerar CPFs usando API legada
    print("\n🎲 Gerando CPFs...\n")
    cpfs = cpf.gerar(quantidade=quantidade, regiao=regiao)
    
    print("✅ CPFs gerados:")
    for i, cpf_gerado in enumerate(cpfs, 1):
        print(f"  {i}. {cpf_gerado}")
    
    print()
    input("Pressione ENTER para voltar ao menu...")
    main()


def validar_cpf():
    """Menu para validar CPF."""
    clear_screen()
    print("\n=== VALIDAR CPF ===\n")
    
    cpf_input = input("Digite o CPF (com ou sem formatação): ").strip()
    
    if not cpf_input:
        print("❌ CPF não pode estar vazio!")
        input("\nPressione ENTER para voltar...")
        main()
        return
    
    # Validar usando API legada
    print("\n🔍 Validando...\n")
    
    # checar com regiao=True imprime a região automaticamente
    resultado = cpf.checar(cpf_input, regiao=True)
    
    if resultado:
        print("✅ CPF VÁLIDO!\n")
    else:
        print("❌ CPF INVÁLIDO!\n")
    
    input("Pressione ENTER para voltar ao menu...")
    main()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Até logo!\n")
        sys.exit(0)
