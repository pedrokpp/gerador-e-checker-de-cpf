"""CNPJ validator implementation using Modulo 11 algorithm.

This validator implements the official Brazilian CNPJ validation algorithm,
which uses a modified modulo 11 method to calculate and verify check digits.
"""

from typing import Protocol

from ..domain.entities import CNPJ


class CNPJValidatorProtocol(Protocol):
    """Protocol for CNPJ validators.
    
    This follows the Dependency Inversion Principle (SOLID),
    allowing different validation strategies.
    """

    def validate(self, cnpj: CNPJ) -> bool:
        """Validate a CNPJ.
        
        Args:
            cnpj: CNPJ object to validate.
            
        Returns:
            bool: True if CNPJ is valid, False otherwise.
        """
        ...


class ModuloElevenCNPJValidator:
    """CNPJ validator using the Modulo 11 algorithm.
    
    The Brazilian CNPJ uses a modulo 11 algorithm with specific weight sequences
    to calculate two check digits:
    
    1. First check digit (position 13):
       - Multiply first 12 digits by weights [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
       - Sum all products
       - Calculate: remainder = sum % 11
       - If remainder < 2: digit = 0
       - Else: digit = 11 - remainder
    
    2. Second check digit (position 14):
       - Multiply first 13 digits by weights [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
       - Sum all products
       - Calculate: remainder = sum % 11
       - If remainder < 2: digit = 0
       - Else: digit = 11 - remainder
    
    Invalid CNPJs:
        - All digits equal (e.g., 00.000.000/0000-00, 11.111.111/1111-11)
        - Check digits don't match calculated values
        
    Examples:
        >>> validator = ModuloElevenCNPJValidator()
        >>> cnpj = CNPJ("11222333000181")
        >>> validator.validate(cnpj)
        True
        >>> cnpj_invalid = CNPJ("11111111111111")
        >>> validator.validate(cnpj_invalid)
        False
    """

    # Weight sequences for CNPJ validation
    FIRST_DIGIT_WEIGHTS = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    SECOND_DIGIT_WEIGHTS = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    def validate(self, cnpj: CNPJ) -> bool:
        """Validate CNPJ using modulo 11 algorithm.
        
        Args:
            cnpj: CNPJ object to validate.
            
        Returns:
            bool: True if CNPJ is valid according to modulo 11 rules.
        """
        cnpj_digits = cnpj.value

        # Check if all digits are the same (invalid CNPJs)
        if cnpj_digits == cnpj_digits[0] * 14:
            return False

        # Calculate first check digit
        first_digit = self._calculate_check_digit(
            cnpj_digits[:12], 
            self.FIRST_DIGIT_WEIGHTS
        )
        if int(cnpj_digits[12]) != first_digit:
            return False

        # Calculate second check digit
        second_digit = self._calculate_check_digit(
            cnpj_digits[:13], 
            self.SECOND_DIGIT_WEIGHTS
        )
        if int(cnpj_digits[13]) != second_digit:
            return False

        return True

    @staticmethod
    def _calculate_check_digit(digits: str, weights: list[int]) -> int:
        """Calculate a single check digit using modulo 11.
        
        Args:
            digits: String of digits to calculate check digit for.
            weights: List of weights to multiply each digit by.
            
        Returns:
            int: Calculated check digit (0-9).
            
        Examples:
            >>> weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
            >>> ModuloElevenCNPJValidator._calculate_check_digit("112223330001", weights)
            8
        """
        # Multiply each digit by its corresponding weight
        total = sum(int(digit) * weight for digit, weight in zip(digits, weights))
        
        # Apply modulo 11 rule
        remainder = total % 11
        
        # If remainder < 2, digit is 0; otherwise, digit is 11 - remainder
        return 0 if remainder < 2 else 11 - remainder
