# Gerador e Checker de CPF
Um script em python que checa e gera CPFs

![Sample Image](./assets/image.png "Exemplo da versão compilada e do exec.py")

## Atenção
Esse script não dá a total certeza se o CPF é válido ou não, ele valida e/ou invalida baseado nos padrões de CPF brasileiros.

## Modos de uso
Você pode importar o arquivo ``cpf.py`` para o seu projeto ou baixar e utilizar ``exec.py`` ou a [versão compilada disponível nas releases](https://github.com/pedrokpp/gerador-e-checker-de-cpf/releases/download/1.0/exec.exe)

## Funções
Para usar, basta baixar o ``cpf.py`` e colocar ele na mesma pasta do seu projeto com ``import cpf``
- ``checar(cpf)``
Checa um CPF.

Se nenhum CPF for passado como parametro ``str``, um ``input()`` será pedido.

Retorna ``True`` quando um CPF é válido e ``False`` quando é inválido

- ``gerar(quantidade)``
Gera um CPF aleatório.

Retorna uma **lista** com os CPFs gerados (já checados).

``quantidade`` é um parametro ``int`` que remete a quantos CPFs serão gerados. ``1`` é o valor padrão e será gerado apenas 1 CPF.

## Exemplos
```python
import cpf
print(cpf.checar("136.718.360-08"))
# output: False

print(cpf.checar("13671836008"))
# output: False

print(cpf.checar("896.163.770-35"))
# output: True

print(cpf.checar("89616377035"))
# output: True

print(cpf.gerar())
# output: ['96996085437']

print(cpf.gerar(5))
# output: ['24544465966', '20271600780', '95935038418', '00484061849', '63073191860']

print(cpf.checar(cpf.gerar()[0]))
# output: True
```

## TODO
- [x] Checker
- [x] Gerador
- [ ] Adicionar opção de região e reconhecimento de região
