"""CPF validator implementation using Modulo 11 algorithm.

This validator implements the official Brazilian CPF validation algorithm,
which uses the modulo 11 method to calculate and verify check digits.
"""

from typing import Protocol

from ..domain.entities import CPF


class CPFValidatorProtocol(Protocol):
    """Protocol for CPF validators.
    
    This follows the Dependency Inversion Principle (SOLID),
    allowing different validation strategies.
    """

    def validate(self, cpf: CPF) -> bool:
        """Validate a CPF.
        
        Args:
            cpf: CPF object to validate.
            
        Returns:
            bool: True if CPF is valid, False otherwise.
        """
        ...


class ModuloElevenValidator:
    """CPF validator using the Modulo 11 algorithm.
    
    The Brazilian CPF uses a modulo 11 algorithm to calculate two check digits:
    
    1. First check digit (position 10):
       - Multiply first 9 digits by (10, 9, 8, 7, 6, 5, 4, 3, 2)
       - Sum all products
       - Calculate: remainder = sum % 11
       - If remainder < 2: digit = 0
       - Else: digit = 11 - remainder
    
    2. Second check digit (position 11):
       - Multiply first 10 digits by (11, 10, 9, 8, 7, 6, 5, 4, 3, 2)
       - Sum all products
       - Calculate: remainder = sum % 11
       - If remainder < 2: digit = 0
       - Else: digit = 11 - remainder
    
    Invalid CPFs:
        - All digits equal (e.g., 111.111.111-11)
        - Check digits don't match calculated values
        
    Examples:
        >>> validator = ModuloElevenValidator()
        >>> cpf = CPF("49435142940")
        >>> validator.validate(cpf)
        True
        >>> cpf_invalid = CPF("11111111111")
        >>> validator.validate(cpf_invalid)
        False
    """

    def validate(self, cpf: CPF) -> bool:
        """Validate CPF using modulo 11 algorithm.
        
        Args:
            cpf: CPF object to validate.
            
        Returns:
            bool: True if CPF is valid according to modulo 11 rules.
        """
        cpf_digits = cpf.value

        # Check if all digits are the same (invalid CPFs)
        if cpf_digits == cpf_digits[0] * 11:
            return False

        # Calculate first check digit
        first_digit = self._calculate_check_digit(cpf_digits[:9], start_weight=10)
        if int(cpf_digits[9]) != first_digit:
            return False

        # Calculate second check digit
        second_digit = self._calculate_check_digit(cpf_digits[:10], start_weight=11)
        if int(cpf_digits[10]) != second_digit:
            return False

        return True

    @staticmethod
    def _calculate_check_digit(digits: str, start_weight: int) -> int:
        """Calculate a single check digit using modulo 11.
        
        Args:
            digits: String of digits to calculate check digit for.
            start_weight: Starting weight for multiplication (10 or 11).
            
        Returns:
            int: Calculated check digit (0-9).
            
        Examples:
            >>> ModuloElevenValidator._calculate_check_digit("123456789", 10)
            0
            >>> ModuloElevenValidator._calculate_check_digit("494351429", 10)
            4
        """
        # Multiply each digit by weights (start_weight, start_weight-1, ..., 2)
        total = 0
        weight = start_weight
        for digit in digits:
            total += int(digit) * weight
            weight -= 1
        
        # Apply modulo 11 rule
        remainder = total % 11
        
        # If remainder < 2, digit is 0; otherwise, digit is 11 - remainder
        return 0 if remainder < 2 else 11 - remainder
