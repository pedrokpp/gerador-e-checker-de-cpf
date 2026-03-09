"""Public API for CNPJ validation and generation.

This module provides the modern API (validate, generate) for CNPJ operations.
"""

from typing import List

from ..application.generate_cnpj import GenerateCNPJUseCase
from ..application.validate_cnpj import ValidateCNPJUseCase

# Initialize use cases (dependency injection)
_validate_use_case = ValidateCNPJUseCase()
_generate_use_case = GenerateCNPJUseCase()


def validate(cnpj: str) -> bool:
    """Validate a Brazilian CNPJ number.
    
    This function validates CNPJ numbers using the official modulo 11 algorithm.
    It accepts both formatted (XX.XXX.XXX/XXXX-XX) and unformatted (XXXXXXXXXXXXXX) CNPJs.
    
    Args:
        cnpj: CNPJ string to validate (formatted or unformatted).
    
    Returns:
        bool: True if CNPJ is valid, False otherwise.
    
    Examples:
        >>> validate("11.222.333/0001-81")
        True
        
        >>> validate("11222333000181")
        True
        
        >>> validate("11.111.111/1111-11")
        False
        
        >>> validate("invalid")
        False
    
    Note:
        CNPJs with all digits equal (e.g., 00.000.000/0000-00, 11.111.111/1111-11)
        are considered invalid even if they pass the checksum test.
    """
    return _validate_use_case.execute(cnpj)


def generate(
    count: int = 1,
    formatted: bool = True,
    matriz_only: bool = True
) -> List[str]:
    """Generate valid Brazilian CNPJ numbers.
    
    Generates one or more valid CNPJ numbers. CNPJs are guaranteed to be valid
    according to the modulo 11 algorithm.
    
    Args:
        count: Number of CNPJs to generate (default: 1, minimum: 1).
        formatted: If True, return formatted CNPJs (XX.XXX.XXX/XXXX-XX).
                  If False, return unformatted (XXXXXXXXXXXXXX).
        matriz_only: If True, generate only headquarters with filial 0001 (default).
                    If False, generate random branch numbers (0001-9999).
    
    Returns:
        List of CNPJ strings.
    
    Raises:
        ValueError: If count < 1.
    
    Examples:
        >>> cnpjs = generate()
        >>> len(cnpjs)
        1
        
        >>> cnpjs = generate(count=3)
        >>> len(cnpjs)
        3
        
        >>> cnpjs = generate(count=2, matriz_only=True)
        >>> # Returns 2 formatted CNPJs with filial 0001
        
        >>> cnpjs = generate(count=1, formatted=False)
        >>> len(cnpjs[0])
        14
        
        >>> cnpjs = generate(count=5, matriz_only=False)
        >>> # Returns 5 formatted CNPJs with random branch numbers
    """
    return _generate_use_case.execute(count, formatted, matriz_only)
