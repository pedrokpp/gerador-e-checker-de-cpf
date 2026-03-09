"""CNPJ - Gerador e validador de CNPJ brasileiro.

Este pacote fornece funções para validar e gerar CNPJs (Cadastro Nacional 
da Pessoa Jurídica) de acordo com o padrão brasileiro, usando o algoritmo 
módulo 11.

Funções principais:
    validate(cnpj) - Valida um CNPJ
    generate(count=1, formatted=True, matriz_only=True) - Gera CNPJs válidos

Exemplos:
    >>> import cnpj
    >>> cnpj.validate("11.222.333/0001-81")
    True
    
    >>> cnpj.generate(count=3)
    ['11.222.333/0001-81', '45.678.901/0001-23', ...]
    
    >>> cnpj.generate(count=2, formatted=False)
    ['11222333000181', '45678901000123']
    
    >>> cnpj.generate(count=5, matriz_only=False)
    ['11.222.333/0245-67', '45.678.901/1234-56', ...]

Para mais informações, acesse: https://github.com/pedrokpp/gerador-e-checker-de-cpf
"""

__version__ = "3.1.0"
__author__ = "pedrokp"
__email__ = "pedrkp@proton.me"

from .presentation.api import generate, validate

__all__ = [
    "validate",
    "generate",
    "__version__",
]
