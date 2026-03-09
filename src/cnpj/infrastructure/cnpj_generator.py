"""Efficient CNPJ generator implementation."""

import random
from typing import Protocol

from ..domain.entities import CNPJ


class CNPJGeneratorProtocol(Protocol):
    """Protocol for CNPJ generators.
    
    This follows the Dependency Inversion Principle (SOLID),
    allowing different generation strategies.
    """

    def generate(self, matriz_only: bool = True) -> CNPJ:
        """Generate a valid CNPJ.
        
        Args:
            matriz_only: If True, generates only headquarters (0001).
                        If False, generates random branch numbers.
            
        Returns:
            CNPJ: A valid CNPJ object.
        """
        ...


class DeterministicCNPJGenerator:
    """Deterministic CNPJ generator.
    
    This generator creates valid CNPJs by:
    1. Generating 8 random base digits
    2. Setting branch digits (0001 for matriz, or random for filial)
    3. Calculating check digits using modulo 11 algorithm
    
    This approach is much more efficient than generating random 14-digit
    numbers and checking validity, as it guarantees valid CNPJs on first try.
    
    Examples:
        >>> generator = DeterministicCNPJGenerator()
        >>> cnpj = generator.generate(matriz_only=True)
        >>> cnpj.is_matriz()
        True
        >>> len(cnpj.value)
        14
    """

    # Weight sequences for CNPJ validation (same as validator)
    FIRST_DIGIT_WEIGHTS = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    SECOND_DIGIT_WEIGHTS = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    def generate(self, matriz_only: bool = True) -> CNPJ:
        """Generate a valid CNPJ.
        
        Args:
            matriz_only: If True, generates only headquarters (0001).
                        If False, generates random branch numbers.
            
        Returns:
            CNPJ: A valid CNPJ object.
        """
        # Generate first 8 random digits (base number)
        base_digits = "".join(str(random.randint(0, 9)) for _ in range(8))
        
        # Add branch digits (9th to 12th position)
        if matriz_only:
            branch_digits = "0001"  # Headquarters
        else:
            # Random branch number (0001-9999)
            branch_num = random.randint(1, 9999)
            branch_digits = f"{branch_num:04d}"
        
        base_with_branch = base_digits + branch_digits
        
        # Calculate first check digit
        first_check = self._calculate_check_digit(
            base_with_branch, 
            self.FIRST_DIGIT_WEIGHTS
        )
        cnpj_with_first = base_with_branch + str(first_check)
        
        # Calculate second check digit
        second_check = self._calculate_check_digit(
            cnpj_with_first, 
            self.SECOND_DIGIT_WEIGHTS
        )
        cnpj_complete = cnpj_with_first + str(second_check)
        
        return CNPJ(cnpj_complete)

    @staticmethod
    def _calculate_check_digit(digits: str, weights: list[int]) -> int:
        """Calculate a single check digit using modulo 11.
        
        This is the same algorithm used by the validator.
        
        Args:
            digits: String of digits to calculate check digit for.
            weights: List of weights to multiply each digit by.
            
        Returns:
            int: Calculated check digit (0-9).
        """
        total = sum(int(digit) * weight for digit, weight in zip(digits, weights))
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder
