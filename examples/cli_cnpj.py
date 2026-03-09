#!/usr/bin/env python3
"""
Exemplo de CLI para geração e validação de CNPJ (API moderna v3.1).

Este script demonstra o uso da API CNPJ (validate/generate) com todos
os recursos, incluindo geração de matriz/filiais e formatação customizável.

Uso:
    python examples/cli_cnpj.py
"""

import os
import sys

# Permite importar cnpj mesmo rodando de examples/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import cnpj


def clear_screen():
    """Limpa a tela do terminal (cross-platform)."""
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    clear_screen()
    
    print("""
    ╔════════════════════════════════════════╗
    ║   Gerador e Validador de CNPJ v3.1.0  ║
    ║          (API Moderna v3.1)           ║
    ╚════════════════════════════════════════╝
    
    Escolha uma opção:
    
    1. Gerar CNPJs
    2. Validar um CNPJ
    3. Validar CNPJs em lote
    4. Sair
    """)
    
    escolha = input("Opção: ").strip()
    
    if escolha == "1":
        gerar_cnpjs()
    elif escolha == "2":
        validar_cnpj_unico()
    elif escolha == "3":
        validar_lote()
    elif escolha == "4":
        print("\nAté logo!\n")
        sys.exit(0)
    else:
        print("\n❌ Opção inválida! Tente novamente.\n")
        input("Pressione ENTER para continuar...")
        main()


def gerar_cnpjs():
    """Menu para geração de CNPJs."""
    clear_screen()
    
    print("""
    ╔═══════════════════════════════╗
    ║      Gerar CNPJs Válidos      ║
    ╚═══════════════════════════════╝
    """)
    
    # Quantidade
    while True:
        try:
            quantidade_str = input("\nQuantidade de CNPJs a gerar (1-100): ").strip()
            quantidade = int(quantidade_str)
            if 1 <= quantidade <= 100:
                break
            print("❌ Digite um número entre 1 e 100.")
        except ValueError:
            print("❌ Digite um número válido.")
    
    # Tipo (matriz ou filial)
    print("\nTipo de CNPJ:")
    print("  1. Apenas matrizes (filial 0001)")
    print("  2. Filiais aleatórias (filial 0001-9999)")
    
    while True:
        tipo = input("Escolha (1 ou 2): ").strip()
        if tipo in ["1", "2"]:
            break
        print("❌ Digite 1 ou 2.")
    
    matriz_only = tipo == "1"
    
    # Formatação
    print("\nFormatação:")
    print("  1. Formatado (XX.XXX.XXX/XXXX-XX)")
    print("  2. Sem formatação (XXXXXXXXXXXXXX)")
    
    while True:
        fmt = input("Escolha (1 ou 2): ").strip()
        if fmt in ["1", "2"]:
            break
        print("❌ Digite 1 ou 2.")
    
    formatted = fmt == "1"
    
    # Gerar CNPJs
    print("\n" + "="*60)
    print(f"Gerando {quantidade} CNPJ(s)...")
    print("="*60 + "\n")
    
    try:
        cnpjs = cnpj.generate(count=quantidade, formatted=formatted, matriz_only=matriz_only)
        
        for i, cnpj_gerado in enumerate(cnpjs, 1):
            tipo_str = "Matriz" if matriz_only else "Filial"
            
            # Extrair filial para mostrar
            unformatted = cnpj_gerado.replace(".", "").replace("/", "").replace("-", "")
            filial = unformatted[8:12]
            
            if formatted:
                print(f"  {i:3d}. {cnpj_gerado} ({tipo_str}: {filial})")
            else:
                # Formatar apenas para exibição
                formatted_display = f"{unformatted[:2]}.{unformatted[2:5]}.{unformatted[5:8]}/{unformatted[8:12]}-{unformatted[12:]}"
                print(f"  {i:3d}. {cnpj_gerado}  →  {formatted_display} ({tipo_str}: {filial})")
        
        print("\n" + "="*60)
        print(f"✅ {quantidade} CNPJ(s) gerado(s) com sucesso!")
        
    except Exception as e:
        print(f"\n❌ Erro ao gerar CNPJs: {e}")
    
    print("="*60)
    input("\nPressione ENTER para voltar ao menu...")
    main()


def validar_cnpj_unico():
    """Menu para validação de um único CNPJ."""
    clear_screen()
    
    print("""
    ╔═══════════════════════════════╗
    ║       Validar um CNPJ         ║
    ╚═══════════════════════════════╝
    """)
    
    cnpj_str = input("\nDigite o CNPJ (com ou sem formatação): ").strip()
    
    if not cnpj_str:
        print("\n❌ CNPJ não pode ser vazio!")
        input("\nPressione ENTER para voltar ao menu...")
        main()
        return
    
    print("\n" + "="*60)
    print("Validando...")
    print("="*60 + "\n")
    
    is_valid = cnpj.validate(cnpj_str)
    
    # Normalizar para exibir formatado
    unformatted = cnpj_str.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
    
    if is_valid and len(unformatted) == 14:
        formatted_display = f"{unformatted[:2]}.{unformatted[2:5]}.{unformatted[5:8]}/{unformatted[8:12]}-{unformatted[12:]}"
        filial = unformatted[8:12]
        tipo_str = "Matriz" if filial == "0001" else f"Filial {filial}"
        
        print(f"✅ CNPJ VÁLIDO")
        print(f"\n   CNPJ: {formatted_display}")
        print(f"   Tipo: {tipo_str}")
    else:
        print(f"❌ CNPJ INVÁLIDO")
        print(f"\n   CNPJ fornecido: {cnpj_str}")
        
        if len(unformatted) != 14:
            print(f"   Motivo: Formato incorreto (esperado 14 dígitos, recebido {len(unformatted)})")
        else:
            print(f"   Motivo: Dígitos verificadores incorretos ou todos dígitos iguais")
    
    print("\n" + "="*60)
    input("\nPressione ENTER para voltar ao menu...")
    main()


def validar_lote():
    """Menu para validação de múltiplos CNPJs."""
    clear_screen()
    
    print("""
    ╔═══════════════════════════════╗
    ║    Validar CNPJs em Lote      ║
    ╚═══════════════════════════════╝
    
    Digite os CNPJs (um por linha).
    Digite uma linha vazia para finalizar.
    """)
    
    cnpjs_para_validar = []
    
    print()
    while True:
        cnpj_str = input(f"CNPJ #{len(cnpjs_para_validar) + 1} (ou ENTER para finalizar): ").strip()
        if not cnpj_str:
            break
        cnpjs_para_validar.append(cnpj_str)
    
    if not cnpjs_para_validar:
        print("\n❌ Nenhum CNPJ fornecido!")
        input("\nPressione ENTER para voltar ao menu...")
        main()
        return
    
    print("\n" + "="*60)
    print(f"Validando {len(cnpjs_para_validar)} CNPJ(s)...")
    print("="*60 + "\n")
    
    validos = 0
    invalidos = 0
    
    for i, cnpj_str in enumerate(cnpjs_para_validar, 1):
        is_valid = cnpj.validate(cnpj_str)
        
        # Normalizar para exibir
        unformatted = cnpj_str.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
        
        if is_valid and len(unformatted) == 14:
            formatted_display = f"{unformatted[:2]}.{unformatted[2:5]}.{unformatted[5:8]}/{unformatted[8:12]}-{unformatted[12:]}"
            print(f"  {i:3d}. ✅ {formatted_display}")
            validos += 1
        else:
            print(f"  {i:3d}. ❌ {cnpj_str}")
            invalidos += 1
    
    print("\n" + "="*60)
    print(f"Resumo: {validos} válido(s), {invalidos} inválido(s)")
    print("="*60)
    input("\nPressione ENTER para voltar ao menu...")
    main()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nPrograma interrompido pelo usuário. Até logo!\n")
        sys.exit(0)
