"""Gera ou checa um CPF.
Acesse https://github.com/pedrokpp/gerador-e-checker-de-cpf para mais informações.

funções:
-----------
    checar(cpf)
    gerar(quantidade)
"""


def checar(cpf=""):
    """Checa um CPF.
    Se nenhum CPF for passado como parametro ``str``, um ``input()`` será pedido.

    Retorna ``True`` quando um CPF é válido e ``False`` quando é inválido 
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
    if len(cpf) == 11 or len(cpf) == 10:
        pass
    else:
        return False
    for x in range(len(cpf)):
        num += int(cpf[x])
    if str(num)[0] == str(num)[1]:
        return True
    else:
        return False


def gerar(quantidade=1):
    """Gera um CPF aleatório.
    Retorna uma lista com os CPFs gerados (já checados).
    ``quantidade`` é um parametro ``int`` que remete a quantos CPFs serão gerados. ``1`` é o valor padrão e será gerado apenas 1 CPF.
    """
    import random
    valid_rcpf = []
    while len(valid_rcpf) != quantidade:
        raw_cpfs = []
        for i in range(quantidade):
            rcpf = ""
            for _ in range(11):
                rcpf += str(random.randint(0, 9))
            raw_cpfs.append(rcpf)
            if checar(raw_cpfs[i]):
                valid_rcpf.append(raw_cpfs[i])
    return valid_rcpf