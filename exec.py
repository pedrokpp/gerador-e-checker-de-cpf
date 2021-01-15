import cpf, os

def main():
    os.system("cls")
    print("\nEsse programa foi feito no Windows e pode ter mal funcionamento quando utilizado em outro OS. \nÉ recomendado que você crie o seu prório script se baseando nos tutoriais disponíveis no GitHub" if not os.name == "nt" else "")
    print("""

    Você deseja:
    1. Gerar CPFs
    2. Checar um CPF
    """)
    c = input(" ")
    if c == "1":
        print(" ")
        q = input("Quantos CPFs deseja gerar? ")
        try:
            q = int(q)
        except:
            print("ERRO: falha ao converter quantidade de CPFs para int (provavelmente não números foram digitados).")
            os.system("pause")
            exit(-1)
        print("CPFs gerados:")
        print(cpf.gerar(q))
        print(" ")
        os.system("pause")
    elif c == "2":
        print(" ")
        if cpf.checar():
            print("CPF válido")
            print(" ")
            os.system("pause")
        else:
            print("CPF inválido")
            print(" ")
            os.system("pause")
    else:
        main()

if __name__ == "__main__":
    main()