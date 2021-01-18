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
        r = input("Qual região deseja por em todos os CPFs? (aperte ENTER para região aleatória) ")
        if r:
            try:
                r = int(r)
            except:
                print("ERRO: falha ao converter região dos CPFs para int (provavelmente não números foram digitados).")
                os.system("pause")
                exit(-1)
        else:
            r=-1
        print("CPFs gerados:")
        print(cpf.gerar(q,r))
        print(" ")
        os.system("pause")
    elif c == "2":
        print(" ")
        if cpf.checar("",True):
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