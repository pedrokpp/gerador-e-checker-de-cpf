"""Public API for CPF validation and generation.

This module provides both the modern API (validate, generate) and
backward-compatible functions (checar, gerar) for existing users.
"""

import warnings
from typing import Dict, List, Optional, Union

from ..application.generate_cpf import GenerateCPFUseCase
from ..application.validate_cpf import ValidateCPFUseCase

# Initialize use cases (dependency injection)
_validate_use_case = ValidateCPFUseCase()
_generate_use_case = GenerateCPFUseCase()


def validate(cpf: str, show_region: bool = False) -> Union[bool, Dict[str, Union[bool, Optional[str]]]]:
    """Validate a Brazilian CPF number.
    
    This function validates CPF numbers using the official modulo 11 algorithm.
    It accepts both formatted (XXX.XXX.XXX-XX) and unformatted (XXXXXXXXXXX) CPFs.
    
    Args:
        cpf: CPF string to validate (formatted or unformatted).
        show_region: If True, return dict with validation result and region info.
                    If False, return just boolean result (default).
    
    Returns:
        If show_region is False: bool indicating if CPF is valid.
        If show_region is True: dict with keys:
            - 'valid' (bool): Whether the CPF is valid
            - 'region' (str | None): Region description if valid, None otherwise
    
    Examples:
        >>> validate("494.351.429-40")
        True
        
        >>> validate("49435142940")
        True
        
        >>> validate("111.111.111-11")
        False
        
        >>> validate("494.351.429-40", show_region=True)
        {'valid': True, 'region': 'Paraná – Santa Catarina'}
        
        >>> validate("12345678900", show_region=True)
        {'valid': False, 'region': None}
    
    Note:
        CPFs with all digits equal (e.g., 000.000.000-00, 111.111.111-11)
        are considered invalid even if they pass the checksum test.
    """
    return _validate_use_case.execute(cpf, show_region)


def generate(
    count: int = 1,
    region: Union[int, str, None] = None,
    formatted: bool = True
) -> List[str]:
    """Generate valid Brazilian CPF numbers.
    
    Generates one or more valid CPF numbers. CPFs are guaranteed to be valid
    according to the modulo 11 algorithm.
    
    Args:
        count: Number of CPFs to generate (default: 1, minimum: 1).
        region: Region specification (default: None for random):
               - None or -1: Random region for each CPF
               - int (0-9): Specific region number:
                   0 = Rio Grande do Sul
                   1 = DF, GO, MS, MT, TO
                   2 = AC, AM, AP, PA, RO, RR
                   3 = CE, MA, PI
                   4 = AL, PB, PE, RN
                   5 = BA, SE
                   6 = MG
                   7 = ES, RJ
                   8 = SP
                   9 = PR, SC
               - str: State name or abbreviation (e.g., "SP", "São Paulo", "RJ")
        formatted: If True, return formatted CPFs (XXX.XXX.XXX-XX).
                  If False, return unformatted (XXXXXXXXXXX).
    
    Returns:
        List of CPF strings.
    
    Raises:
        ValueError: If count < 1 or region is invalid.
    
    Examples:
        >>> cpfs = generate()
        >>> len(cpfs)
        1
        
        >>> cpfs = generate(count=3)
        >>> len(cpfs)
        3
        
        >>> cpfs = generate(count=2, region=8)
        >>> # Returns 2 formatted CPFs from São Paulo region
        
        >>> cpfs = generate(count=1, region="SP", formatted=False)
        >>> len(cpfs[0])
        11
        
        >>> cpfs = generate(count=5, region="Rio de Janeiro")
        >>> # Returns 5 formatted CPFs from RJ/ES region
    """
    return _generate_use_case.execute(count, region, formatted)


# ============================================================================
# BACKWARD COMPATIBILITY API
# ============================================================================
# The functions below maintain 100% backward compatibility with version 2.x
# while internally using the new architecture.
# ============================================================================


def checar(cpf: str = "", regiao: bool = False) -> bool:
    """Checa um CPF (backward compatible function).
    
    DEPRECATED: Esta função é mantida para compatibilidade com versões anteriores.
    Use 'validate()' para novos projetos.
    
    Args:
        cpf: CPF string para validar. Se vazio, solicita input do usuário.
        regiao: Se True, imprime a região no stdout (comportamento legado).
    
    Returns:
        bool: True se o CPF é válido, False caso contrário.
    
    Examples:
        >>> checar("494.351.429-40")
        True
        
        >>> checar("111.111.111-11")
        False
    
    Note:
        Esta função mantém o comportamento exato da versão 2.x, incluindo
        o parâmetro 'regiao' que imprime no stdout (efeito colateral).
    """
    # Warn about deprecation (optional - can be removed to avoid noise)
    # warnings.warn(
    #     "A função 'checar()' está deprecated. Use 'validate()' para novos projetos.",
    #     DeprecationWarning,
    #     stacklevel=2
    # )
    
    # Handle empty CPF (legacy behavior - interactive input)
    if not cpf:
        cpf = input("Digite o CPF que deseja checar: ")
    
    # Validate using new implementation
    result = validate(cpf, show_region=regiao)
    
    # Handle region display (legacy behavior - print to stdout)
    if regiao and isinstance(result, dict):
        valid_value = result["valid"]
        region_value = result["region"]
        if valid_value and region_value:
            # Legacy used "Regiões:" or "Região:" prefix
            region_str = str(region_value)
            if "–" in region_str:
                print(f"Regiões: {region_str}")
            else:
                print(f"Região: {region_str}")
        return bool(valid_value)
    
    # Return boolean result
    if isinstance(result, bool):
        return result
    else:
        return bool(result.get("valid", False))


def gerar(quantidade: int = 1, regiao: int = -1) -> List[str]:
    """Gera CPFs válidos (backward compatible function).
    
    DEPRECATED: Esta função é mantida para compatibilidade com versões anteriores.
    Use 'generate()' para novos projetos.
    
    Args:
        quantidade: Número de CPFs a gerar (padrão: 1).
        regiao: Região dos CPFs (padrão: -1 para aleatório):
               -1 = Aleatório
                0 = Rio Grande do Sul
                1 = DF, GO, MS, MT, TO
                2 = AC, AM, AP, PA, RO, RR
                3 = CE, MA, PI
                4 = AL, PB, PE, RN
                5 = BA, SE
                6 = MG
                7 = ES, RJ
                8 = SP
                9 = PR, SC
    
    Returns:
        Lista de CPFs formatados (XXX.XXX.XXX-XX).
    
    Examples:
        >>> cpfs = gerar()
        >>> len(cpfs)
        1
        
        >>> cpfs = gerar(5, 8)
        >>> len(cpfs)
        5
    
    Note:
        Esta função mantém o comportamento exato da versão 2.x,
        sempre retornando CPFs formatados.
    """
    # Warn about deprecation (optional)
    # warnings.warn(
    #     "A função 'gerar()' está deprecated. Use 'generate()' para novos projetos.",
    #     DeprecationWarning,
    #     stacklevel=2
    # )
    
    # Use new implementation (always formatted for backward compatibility)
    return generate(count=quantidade, region=regiao, formatted=True)
