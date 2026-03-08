"""Efficient CPF generator implementation."""

import random
from typing import Protocol

from ..domain.entities import CPF
from ..domain.region import Region


class CPFGeneratorProtocol(Protocol):
    """Protocol for CPF generators.
    
    This follows the Dependency Inversion Principle (SOLID),
    allowing different generation strategies.
    """

    def generate(self, region: Region) -> CPF:
        """Generate a valid CPF for a specific region.
        
        Args:
            region: The region where the CPF should be issued.
            
        Returns:
            CPF: A valid CPF object.
        """
        ...


class DeterministicCPFGenerator:
    """Deterministic CPF generator.
    
    This generator creates valid CPFs by:
    1. Generating 9 random base digits
    2. Setting the region digit (9th position)
    3. Calculating check digits using modulo 11 algorithm
    
    This approach is much more efficient than generating random 11-digit
    numbers and checking validity, as it guarantees valid CPFs on first try.
    
    Examples:
        >>> generator = DeterministicCPFGenerator()
        >>> cpf = generator.generate(Region.SAO_PAULO)
        >>> cpf.region() == Region.SAO_PAULO
        True
        >>> len(cpf.value)
        11
    """

    def generate(self, region: Region) -> CPF:
        """Generate a valid CPF for the specified region.
        
        Args:
            region: The region where the CPF should be issued.
            
        Returns:
            CPF: A valid CPF object.
        """
        # Generate first 8 random digits
        base_digits = "".join(str(random.randint(0, 9)) for _ in range(8))
        
        # Add region digit (9th position)
        base_digits += str(region.value)
        
        # Calculate first check digit
        first_check = self._calculate_check_digit(base_digits, start_weight=10)
        cpf_with_first = base_digits + str(first_check)
        
        # Calculate second check digit
        second_check = self._calculate_check_digit(cpf_with_first, start_weight=11)
        cpf_complete = cpf_with_first + str(second_check)
        
        return CPF(cpf_complete)

    @staticmethod
    def _calculate_check_digit(digits: str, start_weight: int) -> int:
        """Calculate a single check digit using modulo 11.
        
        This is the same algorithm used by the validator.
        
        Args:
            digits: String of digits to calculate check digit for.
            start_weight: Starting weight for multiplication (10 or 11).
            
        Returns:
            int: Calculated check digit (0-9).
        """
        total = 0
        weight = start_weight
        for digit in digits:
            total += int(digit) * weight
            weight -= 1
        
        remainder = total % 11
        return 0 if remainder < 2 else 11 - remainder
