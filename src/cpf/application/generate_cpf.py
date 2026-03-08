"""Use case for CPF generation."""

import random
from typing import List, Union

from ..domain.region import Region
from ..infrastructure.cpf_generator import CPFGeneratorProtocol, DeterministicCPFGenerator


class GenerateCPFUseCase:
    """Use case for generating valid CPF numbers.
    
    This class orchestrates the CPF generation process, following the
    Single Responsibility Principle (SOLID).
    
    Attributes:
        generator: The generator implementation to use.
    """

    def __init__(self, generator: CPFGeneratorProtocol | None = None) -> None:
        """Initialize the use case with a generator.
        
        Args:
            generator: Optional generator implementation.
                      Defaults to DeterministicCPFGenerator.
        """
        self.generator = generator or DeterministicCPFGenerator()

    def execute(
        self,
        count: int = 1,
        region: Union[int, str, None] = None,
        formatted: bool = True
    ) -> List[str]:
        """Execute CPF generation.
        
        Args:
            count: Number of CPFs to generate (default: 1).
            region: Region specification:
                   - None or -1: Random region for each CPF
                   - int (0-9): Specific region number
                   - str: State name or abbreviation (e.g., "SP", "São Paulo")
            formatted: If True, return formatted CPFs (XXX.XXX.XXX-XX).
                      If False, return unformatted (XXXXXXXXXXX).
            
        Returns:
            List of generated CPF strings.
            
        Raises:
            ValueError: If count is less than 1 or region is invalid.
            
        Examples:
            >>> use_case = GenerateCPFUseCase()
            >>> cpfs = use_case.execute(count=2)
            >>> len(cpfs)
            2
            >>> cpfs = use_case.execute(count=1, region=8, formatted=False)
            >>> len(cpfs[0])
            11
            >>> cpfs = use_case.execute(count=1, region="SP")
            >>> # Returns formatted CPF from São Paulo region
        """
        if count < 1:
            raise ValueError("O número de CPFs deve ser pelo menos 1")
        
        cpfs: List[str] = []
        
        for _ in range(count):
            # Determine region for this CPF
            cpf_region = self._resolve_region(region)
            
            # Generate CPF
            cpf = self.generator.generate(cpf_region)
            
            # Format according to preference
            cpf_str = cpf.formatted() if formatted else cpf.value
            cpfs.append(cpf_str)
        
        return cpfs

    def _resolve_region(self, region: Union[int, str, None]) -> Region:
        """Resolve region specification to Region enum.
        
        Args:
            region: Region specification (int, str, or None).
            
        Returns:
            Region: Resolved region enum value.
            
        Raises:
            ValueError: If region specification is invalid.
        """
        # None or -1 means random region
        if region is None or region == -1:
            return Region(random.randint(0, 9))
        
        # Integer region (0-9)
        if isinstance(region, int):
            if 0 <= region <= 9:
                return Region(region)
            else:
                raise ValueError(
                    f"Região inválida: {region}. "
                    f"Deve ser um número de 0 a 9, -1 para aleatório, "
                    f"ou nome/sigla de estado."
                )
        
        # String region (state name or abbreviation)
        if isinstance(region, str):
            try:
                return Region.from_name(region)
            except ValueError as e:
                raise ValueError(str(e)) from e
        
        raise ValueError(
            f"Tipo de região inválido: {type(region)}. "
            f"Use int (0-9), str (nome/sigla do estado), ou None/-1 para aleatório."
        )
