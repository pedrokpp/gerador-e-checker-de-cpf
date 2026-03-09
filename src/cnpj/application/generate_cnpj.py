"""Use case for CNPJ generation."""

from typing import List

from ..domain.entities import CNPJ
from ..infrastructure.cnpj_generator import DeterministicCNPJGenerator


class GenerateCNPJUseCase:
    """Use case for generating valid CNPJs.
    
    This use case orchestrates the generation process by:
    1. Validating input parameters
    2. Generating the requested number of CNPJs
    3. Formatting output according to preferences
    
    Examples:
        >>> use_case = GenerateCNPJUseCase()
        >>> cnpjs = use_case.execute(count=2, formatted=True, matriz_only=True)
        >>> len(cnpjs)
        2
    """

    def __init__(self, generator: DeterministicCNPJGenerator | None = None) -> None:
        """Initialize the use case with a generator.
        
        Args:
            generator: CNPJ generator to use. If None, uses default generator.
        """
        self.generator = generator or DeterministicCNPJGenerator()

    def execute(
        self,
        count: int = 1,
        formatted: bool = True,
        matriz_only: bool = True
    ) -> List[str]:
        """Execute CNPJ generation.
        
        Args:
            count: Number of CNPJs to generate (minimum: 1).
            formatted: If True, return formatted CNPJs (XX.XXX.XXX/XXXX-XX).
                      If False, return unformatted (XXXXXXXXXXXXXX).
            matriz_only: If True, generate only headquarters (filial 0001).
                        If False, generate random branch numbers.
            
        Returns:
            List of CNPJ strings.
            
        Raises:
            ValueError: If count < 1.
            
        Examples:
            >>> use_case = GenerateCNPJUseCase()
            >>> cnpjs = use_case.execute(count=3, formatted=True, matriz_only=True)
            >>> len(cnpjs)
            3
            >>> all("." in c for c in cnpjs)
            True
        """
        # Validate count
        if count < 1:
            raise ValueError("O parâmetro 'count' deve ser pelo menos 1.")

        # Generate CNPJs
        cnpjs: List[CNPJ] = []
        for _ in range(count):
            cnpj = self.generator.generate(matriz_only=matriz_only)
            cnpjs.append(cnpj)

        # Format output
        if formatted:
            return [cnpj.formatted() for cnpj in cnpjs]
        else:
            return [cnpj.value for cnpj in cnpjs]
