#!/usr/bin/env python3
"""
Exemplo de CLI para geração e validação de CPF (API moderna v3.0).

Este script demonstra o uso da nova API (validate/generate) com todos
os recursos da versão 3.0, incluindo região por nome e formatação customizável.

Uso:
    python examples/cli_modern.py
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
    ║          (API Moderna v3.0)           ║
    ╚════════════════════════════════════════╝
    
    Escolha uma opção:
    
    1. Gerar CPFs
    2. Validar um CPF
    3. Validar CPFs em lote
    4. Sair
    """)
    
    escolha = input("Opção: ").strip()
    
    if escolha == "1":
        gerar_cpfs()
    elif escolha == "2":
        validar_cpf()
    elif escolha == "3":
        validar_lote()
    elif escolha == "4":
        print("\n👋 Até logo!\n")
        sys.exit(0)
    else:
        print("\n❌ Opção inválida! Tente novamente.\n")
        input("Pressione ENTER para continuar...")
        main()


def gerar_cpfs():
    """Menu para gerar CPFs com a nova API."""
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
    
    # Região (suporta nome e número!)
    print("\n🗺️  Região (NOVO: aceita sigla ou nome!):")
    print("  Exemplos: SP, São Paulo, RJ, Rio de Janeiro, etc.")
    print("  Ou números: 0-9 (ou ENTER para aleatória)")
    
    regiao_input = input("\nQual região? (ENTER para aleatória): ").strip()
    
    # Se vazio, região aleatória
    regiao = None if not regiao_input else regiao_input
    
    # Se for número, converter
    if regiao and regiao.isdigit():
        regiao = int(regiao)
    
    # Formatação
    print("\n📝 Formatação:")
    print("  1. Com formatação (XXX.XXX.XXX-XX) - padrão")
    print("  2. Sem formatação (XXXXXXXXXXX)")
    
    formato = input("\nEscolha (ENTER para padrão): ").strip()
    formatted = formato != "2"
    
    # Gerar CPFs usando API moderna
    print("\n🎲 Gerando CPFs...\n")
    
    try:
        cpfs = cpf.generate(count=quantidade, region=regiao, formatted=formatted)
        
        print("✅ CPFs gerados:")
        for i, cpf_gerado in enumerate(cpfs, 1):
            # Validar cada CPF gerado
            is_valid = cpf.validate(cpf_gerado)
            status = "✅" if is_valid else "❌"
            print(f"  {i}. {cpf_gerado} {status}")
        
        # Mostrar estatísticas
        if regiao:
            regiao_str = regiao if isinstance(regiao, str) else f"Código {regiao}"
            print(f"\n📍 Região: {regiao_str}")
        else:
            print("\n📍 Regiões: Aleatórias")
        
        print(f"📦 Formato: {'Formatado' if formatted else 'Não formatado'}")
        
    except ValueError as e:
        print(f"\n❌ Erro: {e}")
    
    print()
    input("Pressione ENTER para voltar ao menu...")
    main()


def validar_cpf():
    """Menu para validar um único CPF."""
    clear_screen()
    print("\n=== VALIDAR CPF ===\n")
    
    cpf_input = input("Digite o CPF (com ou sem formatação): ").strip()
    
    if not cpf_input:
        print("❌ CPF não pode estar vazio!")
        input("\nPressione ENTER para voltar...")
        main()
        return
    
    # Validar usando API moderna com show_region=True
    print("\n🔍 Validando...\n")
    
    resultado = cpf.validate(cpf_input, show_region=True)
    
    if isinstance(resultado, dict):
        if resultado['valid']:
            print("✅ CPF VÁLIDO!\n")
            print(f"📍 Região: {resultado['region']}")
        else:
            print("❌ CPF INVÁLIDO!\n")
    else:
        if resultado:
            print("✅ CPF VÁLIDO!\n")
        else:
            print("❌ CPF INVÁLIDO!\n")
    
    print()
    input("Pressione ENTER para voltar ao menu...")
    main()


def validar_lote():
    """Validar múltiplos CPFs de uma vez."""
    clear_screen()
    print("\n=== VALIDAR CPFs EM LOTE ===\n")
    print("Digite os CPFs (um por linha).")
    print("Digite uma linha vazia para finalizar.\n")
    
    cpfs_input = []
    while True:
        cpf_input = input(f"CPF #{len(cpfs_input) + 1} (ou ENTER para finalizar): ").strip()
        if not cpf_input:
            break
        cpfs_input.append(cpf_input)
    
    if not cpfs_input:
        print("\n❌ Nenhum CPF fornecido!")
        input("\nPressione ENTER para voltar...")
        main()
        return
    
    print(f"\n🔍 Validando {len(cpfs_input)} CPFs...\n")
    
    validos = 0
    invalidos = 0
    
    for i, cpf_input in enumerate(cpfs_input, 1):
        resultado = cpf.validate(cpf_input, show_region=True)
        
        if isinstance(resultado, dict) and resultado['valid']:
            print(f"  {i}. ✅ {cpf_input} - VÁLIDO")
            print(f"      📍 {resultado['region']}")
            validos += 1
        else:
            print(f"  {i}. ❌ {cpf_input} - INVÁLIDO")
            invalidos += 1
    
    # Estatísticas
    total = len(cpfs_input)
    print(f"\n{'='*50}")
    print(f"📊 Resumo:")
    print(f"  Total: {total}")
    print(f"  ✅ Válidos: {validos} ({validos/total*100:.1f}%)")
    print(f"  ❌ Inválidos: {invalidos} ({invalidos/total*100:.1f}%)")
    print(f"{'='*50}")
    
    print()
    input("Pressione ENTER para voltar ao menu...")
    main()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Até logo!\n")
        sys.exit(0)
