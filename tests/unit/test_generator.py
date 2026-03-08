"""Unit tests for CPF generator."""

import pytest

from src.cpf.domain.region import Region
from src.cpf.infrastructure.cpf_generator import DeterministicCPFGenerator
from src.cpf.infrastructure.cpf_validator import ModuloElevenValidator


class TestDeterministicCPFGenerator:
    """Test suite for DeterministicCPFGenerator."""

    @pytest.fixture
    def generator(self) -> DeterministicCPFGenerator:
        """Create a generator instance for testing."""
        return DeterministicCPFGenerator()

    @pytest.fixture
    def validator(self) -> ModuloElevenValidator:
        """Create a validator instance for testing."""
        return ModuloElevenValidator()

    def test_generate_valid_cpf(
        self,
        generator: DeterministicCPFGenerator,
        validator: ModuloElevenValidator
    ) -> None:
        """Test that generated CPF is valid."""
        cpf = generator.generate(Region.SAO_PAULO)
        assert validator.validate(cpf) is True

    def test_generate_correct_length(self, generator: DeterministicCPFGenerator) -> None:
        """Test that generated CPF has 11 digits."""
        cpf = generator.generate(Region.SAO_PAULO)
        assert len(cpf.value) == 11

    @pytest.mark.parametrize("region", list(Region))
    def test_generate_for_all_regions(
        self,
        generator: DeterministicCPFGenerator,
        validator: ModuloElevenValidator,
        region: Region
    ) -> None:
        """Test that generator works for all regions."""
        cpf = generator.generate(region)
        assert validator.validate(cpf) is True
        assert cpf.region() == region

    def test_generate_multiple_different_cpfs(
        self,
        generator: DeterministicCPFGenerator
    ) -> None:
        """Test that multiple generated CPFs are different (probabilistic)."""
        cpfs = [generator.generate(Region.SAO_PAULO) for _ in range(100)]
        # It's extremely unlikely that all 100 CPFs are the same
        unique_cpfs = set(cpf.value for cpf in cpfs)
        assert len(unique_cpfs) > 1, "Generated CPFs should be different"

    def test_generate_region_digit_position(
        self,
        generator: DeterministicCPFGenerator
    ) -> None:
        """Test that region digit is correctly placed at position 8 (9th digit)."""
        cpf = generator.generate(Region.SAO_PAULO)
        assert cpf.value[8] == "8"

        cpf = generator.generate(Region.RIO_GRANDE_DO_SUL)
        assert cpf.value[8] == "0"

        cpf = generator.generate(Region.SUL)
        assert cpf.value[8] == "9"

    def test_generated_cpf_is_always_valid(
        self,
        generator: DeterministicCPFGenerator,
        validator: ModuloElevenValidator
    ) -> None:
        """Test that generator always produces valid CPFs (deterministic)."""
        # Generate 1000 CPFs and ensure all are valid
        for _ in range(1000):
            region = Region((_ % 10))  # Cycle through all regions
            cpf = generator.generate(region)
            assert validator.validate(cpf) is True, f"Generated CPF {cpf.value} should be valid"
