"""CPF - Gerador e validador de CPF brasileiro.

Este pacote fornece funções para validar e gerar CPFs (Cadastro de Pessoas Físicas)
de acordo com o padrão brasileiro, usando o algoritmo módulo 11.

Funções principais:
    validate(cpf, show_region=False) - Valida um CPF
    generate(count=1, region=None, formatted=True) - Gera CPFs válidos

Funções legadas (backward compatibility):
    checar(cpf, regiao=False) - Alias para validate()
    gerar(quantidade=1, regiao=-1) - Alias para generate()

Exemplos:
    >>> import cpf
    >>> cpf.validate("494.351.429-40")
    True
    
    >>> cpf.generate(count=3, region="SP")
    ['123.456.789-09', '987.654.321-00', ...]
    
    >>> cpf.validate("494.351.429-40", show_region=True)
    {'valid': True, 'region': 'Paraná – Santa Catarina'}

Para mais informações, acesse: https://github.com/pedrokpp/gerador-e-checker-de-cpf
"""

__version__ = "3.0.1"
__author__ = "pedrokp"
__email__ = "pedrkp@proton.me"

from .presentation.api import checar, gerar, generate, validate

__all__ = [
    # Modern API (recommended)
    "validate",
    "generate",
    # Legacy API (backward compatibility)
    "checar",
    "gerar",
    # Metadata
    "__version__",
]
