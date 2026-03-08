"""Use case for CPF validation."""

from typing import Dict, Optional, Union

from ..domain.entities import CPF
from ..infrastructure.cpf_validator import CPFValidatorProtocol, ModuloElevenValidator


class ValidateCPFUseCase:
    """Use case for validating CPF numbers.
    
    This class orchestrates the CPF validation process, following the
    Single Responsibility Principle (SOLID).
    
    Attributes:
        validator: The validator implementation to use.
    """

    def __init__(self, validator: CPFValidatorProtocol | None = None) -> None:
        """Initialize the use case with a validator.
        
        Args:
            validator: Optional validator implementation.
                      Defaults to ModuloElevenValidator.
        """
        self.validator = validator or ModuloElevenValidator()

    def execute(self, cpf_str: str, show_region: bool = False) -> Union[bool, Dict[str, Union[bool, Optional[str]]]]:
        """Execute CPF validation.
        
        Args:
            cpf_str: CPF string to validate (formatted or not).
            show_region: If True, return dict with validation result and region info.
                        If False, return just boolean result.
            
        Returns:
            If show_region is False: bool indicating if CPF is valid.
            If show_region is True: dict with 'valid' and 'region' keys.
            
        Examples:
            >>> use_case = ValidateCPFUseCase()
            >>> use_case.execute("494.351.429-40")
            True
            >>> use_case.execute("494.351.429-40", show_region=True)
            {'valid': True, 'region': 'Paraná – Santa Catarina'}
            >>> use_case.execute("111.111.111-11")
            False
        """
        try:
            cpf = CPF.parse(cpf_str)
            is_valid = self.validator.validate(cpf)
            
            if not show_region:
                return is_valid
            
            if is_valid:
                region = cpf.region()
                return {
                    "valid": True,
                    "region": region.get_description()
                }
            else:
                result: Dict[str, Union[bool, Optional[str]]] = {
                    "valid": False,
                    "region": None
                }
                return result
                
        except ValueError:
            # Invalid format
            if show_region:
                result: Dict[str, Union[bool, Optional[str]]] = {"valid": False, "region": None}
                return result
            return False
