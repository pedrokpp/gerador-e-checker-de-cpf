"""Gera ou checa um CPF.
Acesse https://github.com/pedrokpp/gerador-e-checker-de-cpf para mais informações.

Funções:
-----------
    checar(cpf, regiao)
    gerar(quantidade, regiao)
"""


def checar(cpf="",regiao=False):
    """Checa um CPF.
    Se nenhum CPF for passado como parametro ``str``, um ``input()`` será pedido.

    Retorna ``True`` quando um CPF é válido e ``False`` quando é inválido 

    ``regiao`` é um parametro ``bool`` o qual checará ou não a região do CPF retornado em ``stdout``. ``False`` é o valor padrão e a região não será checada.
    """
    if not cpf:
        cpf = input("Digite o CPF que deseja checar: ")
    else:
        cpf = cpf
    num = 0
    # 000.000.000-00
    if "." in cpf and "-" in cpf:
        cpf = cpf.replace(".", "").replace("-", "")
    else:
        pass
    if len(cpf) == 11:
        pass
    else:
        return False
    for x in range(len(cpf)):
        num += int(cpf[x])
    if str(num)[0] == str(num)[1]:
        if regiao:
            reg = lambda regi: print("Regiões: " + regi)
            ident=str(cpf[8])
            if ident == "0":
                print("Região: Rio Grande do Sul")
            elif ident == "1":
                reg("Distrito Federal – Goiás – Mato Grosso – Mato Grosso do Sul – Tocantins")
            elif ident == "2":
                reg("Pará – Amazonas – Acre – Amapá – Rondônia – Roraima")
            elif ident == "3":
                reg("Ceará – Maranhão – Piauí")
            elif ident == "4":
                reg("Pernambuco – Rio Grande do Norte – Paraíba – Alagoas")
            elif ident == "5":
                reg("Bahia – Sergipe")
            elif ident == "6":
                reg("Minas Gerais")
            elif ident == "7":
                reg("Rio de Janeiro – Espírito Santo")
            elif ident == "8":
                reg("São Paulo")
            elif ident == "9":
                reg("Paraná – Santa Catarina")
        return True
    else:
        return False


def gerar(quantidade=1,regiao=-1):
    """Gera um CPF aleatório.
    Retorna uma lista com os CPFs gerados (já checados).
    ``quantidade`` é um parametro ``int`` que remete a quantos CPFs serão gerados. ``1`` é o valor padrão e será gerado apenas 1 CPF.
    ``regiao`` é um parametro ``int`` que remete à região cujos CPFs serão gerados. ``-1`` é o valor padrão e será utilizado uma região aleatória.

    Regiôes:
    -----------
         0:  Rio Grande do Sul    

         1:  Distrito Federal – Goiás – Mato Grosso – Mato Grosso do Sul – Tocantins    

         2:  Pará – Amazonas – Acre – Amapá – Rondônia – Roraima    

         3:  Ceará – Maranhão – Piauí    

         4:  Pernambuco – Rio Grande do Norte – Paraíba – Alagoas    

         5:  Bahia – Sergipe    

         6:  Minas Gerais    

         7:  Rio de Janeiro – Espírito Santo

         8:  São Paulo

         9: Paraná – Santa Catarina

    """
    import random
    valid_rcpf = []
    valid_cpfs = []
    while len(valid_rcpf) != quantidade:
        raw_cpfs = []
        for i in range(quantidade):
            rcpf = ""
            for x in range(11):
                if x == 8:
                    if regiao == -1:
                        rcpf += str(random.randint(0, 9))
                    else:
                        rcpf += str(regiao)
                else:
                    rcpf += str(random.randint(0, 9))
            raw_cpfs.append(rcpf)
            if checar(raw_cpfs[i],False):
                valid_rcpf.append(raw_cpfs[i])
    for i in range(len(valid_rcpf)):
        valid_cpfs.append(valid_rcpf[i][:3]+"."+valid_rcpf[i][3:6]+"."+valid_rcpf[i][6:9]+"-"+valid_rcpf[i][9::])
    return valid_cpfs