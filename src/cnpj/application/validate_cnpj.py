"""Use case for CNPJ validation."""

from ..domain.entities import CNPJ
from ..infrastructure.cnpj_validator import ModuloElevenCNPJValidator


class ValidateCNPJUseCase:
    """Use case for validating a CNPJ.
    
    This use case orchestrates the validation process by:
    1. Parsing the input CNPJ string
    2. Delegating validation to the validator
    3. Handling any errors gracefully
    
    Examples:
        >>> use_case = ValidateCNPJUseCase()
        >>> use_case.execute("11.222.333/0001-81")
        True
        >>> use_case.execute("11.111.111/1111-11")
        False
    """

    def __init__(self, validator: ModuloElevenCNPJValidator | None = None) -> None:
        """Initialize the use case with a validator.
        
        Args:
            validator: CNPJ validator to use. If None, uses default validator.
        """
        self.validator = validator or ModuloElevenCNPJValidator()

    def execute(self, cnpj_str: str) -> bool:
        """Execute CNPJ validation.
        
        Args:
            cnpj_str: CNPJ string to validate (formatted or unformatted).
            
        Returns:
            bool: True if CNPJ is valid, False otherwise.
            
        Examples:
            >>> use_case = ValidateCNPJUseCase()
            >>> use_case.execute("11.222.333/0001-81")
            True
            >>> use_case.execute("11222333000181")
            True
            >>> use_case.execute("invalid")
            False
        """
        try:
            # Parse and normalize CNPJ
            cnpj = CNPJ.parse(cnpj_str)
            
            # Validate using modulo 11 algorithm
            return self.validator.validate(cnpj)
            
        except (ValueError, IndexError, AttributeError):
            # Invalid format or parsing error
            return False
