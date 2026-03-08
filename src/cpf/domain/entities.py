"""CPF entity and value object."""

import re
from dataclasses import dataclass
from typing import Optional

from .region import Region


@dataclass(frozen=True)
class CPF:
    """CPF (Cadastro de Pessoas Físicas) value object.
    
    Represents a Brazilian CPF number with validation.
    CPF format: XXX.XXX.XXX-XX or XXXXXXXXXXX (11 digits)
    
    Attributes:
        value: The CPF number (digits only, no formatting).
        
    Examples:
        >>> cpf = CPF("12345678909")
        >>> cpf.value
        '12345678909'
        >>> cpf.formatted()
        '123.456.789-09'
        >>> cpf.region()
        <Region.SAO_PAULO: 8>
    """

    value: str

    def __post_init__(self) -> None:
        """Validate CPF format after initialization."""
        if not self._is_valid_format(self.value):
            raise ValueError(
                f"CPF inválido: {self.value}. "
                f"Deve conter exatamente 11 dígitos numéricos."
            )

    @staticmethod
    def _is_valid_format(cpf: str) -> bool:
        """Check if CPF has valid format (11 digits).
        
        Args:
            cpf: CPF string to validate.
            
        Returns:
            bool: True if format is valid, False otherwise.
        """
        return bool(re.match(r"^\d{11}$", cpf))

    @classmethod
    def parse(cls, cpf: str) -> "CPF":
        """Parse a CPF string, removing formatting if present.
        
        Args:
            cpf: CPF string (formatted or not).
            
        Returns:
            CPF: CPF object with normalized value.
            
        Raises:
            ValueError: If CPF format is invalid.
            
        Examples:
            >>> CPF.parse("123.456.789-09")
            CPF(value='12345678909')
            >>> CPF.parse("12345678909")
            CPF(value='12345678909')
        """
        # Remove all non-digit characters
        normalized = re.sub(r"\D", "", cpf)
        return cls(normalized)

    def formatted(self) -> str:
        """Return CPF in formatted representation.
        
        Returns:
            str: CPF formatted as XXX.XXX.XXX-XX.
            
        Examples:
            >>> CPF("12345678909").formatted()
            '123.456.789-09'
        """
        return f"{self.value[:3]}.{self.value[3:6]}.{self.value[6:9]}-{self.value[9:]}"

    def region(self) -> Region:
        """Get the region where this CPF was issued.
        
        The 9th digit (index 8) indicates the issuing region.
        
        Returns:
            Region: The region enum value.
            
        Examples:
            >>> CPF("12345678809").region()
            <Region.SAO_PAULO: 8>
        """
        region_digit = int(self.value[8])
        return Region(region_digit)

    def __str__(self) -> str:
        """Return formatted CPF representation."""
        return self.formatted()
