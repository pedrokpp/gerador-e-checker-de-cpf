"""Application layer for CNPJ - Use cases."""

from .generate_cnpj import GenerateCNPJUseCase
from .validate_cnpj import ValidateCNPJUseCase

__all__ = ["ValidateCNPJUseCase", "GenerateCNPJUseCase"]
