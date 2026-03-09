"""CNPJ entity and value object."""

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class CNPJ:
    """CNPJ (Cadastro Nacional da Pessoa Jurídica) value object.
    
    Represents a Brazilian CNPJ number with validation.
    CNPJ format: XX.XXX.XXX/XXXX-XX or XXXXXXXXXXXXXX (14 digits)
    
    Structure:
        - 8 base digits: Company identification number
        - 4 branch digits: Branch number (0001 = headquarters/matriz)
        - 2 check digits: Verification digits calculated using modulo 11
    
    Attributes:
        value: The CNPJ number (digits only, no formatting).
        
    Examples:
        >>> cnpj = CNPJ("11222333000181")
        >>> cnpj.value
        '11222333000181'
        >>> cnpj.formatted()
        '11.222.333/0001-81'
        >>> cnpj.is_matriz()
        True
    """

    value: str

    def __post_init__(self) -> None:
        """Validate CNPJ format after initialization."""
        if not self._is_valid_format(self.value):
            raise ValueError(
                f"CNPJ inválido: {self.value}. "
                f"Deve conter exatamente 14 dígitos numéricos."
            )

    @staticmethod
    def _is_valid_format(cnpj: str) -> bool:
        """Check if CNPJ has valid format (14 digits).
        
        Args:
            cnpj: CNPJ string to validate.
            
        Returns:
            bool: True if format is valid, False otherwise.
        """
        return bool(re.match(r"^\d{14}$", cnpj))

    @classmethod
    def parse(cls, cnpj: str) -> "CNPJ":
        """Parse a CNPJ string, removing formatting if present.
        
        Args:
            cnpj: CNPJ string (formatted or not).
            
        Returns:
            CNPJ: CNPJ object with normalized value.
            
        Raises:
            ValueError: If CNPJ format is invalid.
            
        Examples:
            >>> CNPJ.parse("11.222.333/0001-81")
            CNPJ(value='11222333000181')
            >>> CNPJ.parse("11222333000181")
            CNPJ(value='11222333000181')
        """
        # Remove all non-digit characters
        normalized = re.sub(r"\D", "", cnpj)
        return cls(normalized)

    def formatted(self) -> str:
        """Return CNPJ in formatted representation.
        
        Returns:
            str: CNPJ formatted as XX.XXX.XXX/XXXX-XX.
            
        Examples:
            >>> CNPJ("11222333000181").formatted()
            '11.222.333/0001-81'
        """
        return (
            f"{self.value[:2]}.{self.value[2:5]}.{self.value[5:8]}/"
            f"{self.value[8:12]}-{self.value[12:]}"
        )

    def is_matriz(self) -> bool:
        """Check if this CNPJ is a headquarters (matriz).
        
        A CNPJ is considered headquarters if the branch digits (positions 8-11) are 0001.
        
        Returns:
            bool: True if this is a headquarters, False otherwise.
            
        Examples:
            >>> CNPJ("11222333000181").is_matriz()
            True
            >>> CNPJ("11222333000281").is_matriz()
            False
        """
        return self.value[8:12] == "0001"

    def branch_number(self) -> str:
        """Get the branch number (filial) of this CNPJ.
        
        Returns:
            str: The 4-digit branch number.
            
        Examples:
            >>> CNPJ("11222333000181").branch_number()
            '0001'
            >>> CNPJ("11222333012345").branch_number()
            '1234'
        """
        return self.value[8:12]

    def __str__(self) -> str:
        """Return formatted CNPJ representation."""
        return self.formatted()
