"""Unit tests for CNPJ generator."""

import pytest

from src.cnpj.infrastructure.cnpj_generator import DeterministicCNPJGenerator
from src.cnpj.infrastructure.cnpj_validator import ModuloElevenCNPJValidator


class TestDeterministicCNPJGenerator:
    """Test suite for DeterministicCNPJGenerator."""

    @pytest.fixture
    def generator(self) -> DeterministicCNPJGenerator:
        """Create a generator instance for testing."""
        return DeterministicCNPJGenerator()

    @pytest.fixture
    def validator(self) -> ModuloElevenCNPJValidator:
        """Create a validator instance for testing."""
        return ModuloElevenCNPJValidator()

    # ========================================================================
    # Basic generation tests
    # ========================================================================

    def test_generate_valid_cnpj(
        self,
        generator: DeterministicCNPJGenerator,
        validator: ModuloElevenCNPJValidator
    ) -> None:
        """Test that generated CNPJ is valid."""
        cnpj = generator.generate(matriz_only=True)
        assert validator.validate(cnpj) is True

    def test_generate_correct_length(self, generator: DeterministicCNPJGenerator) -> None:
        """Test that generated CNPJ has 14 digits."""
        cnpj = generator.generate(matriz_only=True)
        assert len(cnpj.value) == 14

    # ========================================================================
    # Matriz generation tests
    # ========================================================================

    def test_generate_matriz_only(self, generator: DeterministicCNPJGenerator) -> None:
        """Test generating only headquarters (matriz) CNPJs."""
        cnpj = generator.generate(matriz_only=True)
        assert cnpj.is_matriz() is True
        assert cnpj.branch_number() == "0001"

    def test_generate_multiple_matriz(self, generator: DeterministicCNPJGenerator) -> None:
        """Test that multiple matriz CNPJs are generated correctly."""
        cnpjs = [generator.generate(matriz_only=True) for _ in range(10)]
        for cnpj in cnpjs:
            assert cnpj.is_matriz() is True
            assert cnpj.branch_number() == "0001"

    # ========================================================================
    # Filial generation tests
    # ========================================================================

    def test_generate_with_random_filial(
        self,
        generator: DeterministicCNPJGenerator,
        validator: ModuloElevenCNPJValidator
    ) -> None:
        """Test generating CNPJs with random branch numbers."""
        cnpj = generator.generate(matriz_only=False)
        assert validator.validate(cnpj) is True
        # Branch number should be between 0001 and 9999
        branch = int(cnpj.branch_number())
        assert 1 <= branch <= 9999

    def test_generate_multiple_filiais(
        self,
        generator: DeterministicCNPJGenerator
    ) -> None:
        """Test that multiple filial CNPJs can have different branch numbers."""
        cnpjs = [generator.generate(matriz_only=False) for _ in range(50)]
        branches = set(cnpj.branch_number() for cnpj in cnpjs)
        # With 50 CNPJs, very likely to have more than 1 different branch
        assert len(branches) > 1

    # ========================================================================
    # Multiple generation tests
    # ========================================================================

    def test_generate_multiple_different_cnpjs(
        self,
        generator: DeterministicCNPJGenerator
    ) -> None:
        """Test that multiple generated CNPJs are different (probabilistic)."""
        cnpjs = [generator.generate(matriz_only=True) for _ in range(100)]
        # It's extremely unlikely that all 100 CNPJs are the same
        unique_cnpjs = set(cnpj.value for cnpj in cnpjs)
        assert len(unique_cnpjs) > 1, "Generated CNPJs should be different"

    def test_generated_cnpj_is_always_valid(
        self,
        generator: DeterministicCNPJGenerator,
        validator: ModuloElevenCNPJValidator
    ) -> None:
        """Test that generator always produces valid CNPJs (deterministic)."""
        # Generate 1000 CNPJs and ensure all are valid
        for i in range(1000):
            matriz_only = i % 2 == 0  # Alternate between matriz and filial
            cnpj = generator.generate(matriz_only=matriz_only)
            assert validator.validate(cnpj) is True, \
                f"Generated CNPJ {cnpj.value} should be valid"

    # ========================================================================
    # Branch number position tests
    # ========================================================================

    def test_branch_position_matriz(
        self,
        generator: DeterministicCNPJGenerator
    ) -> None:
        """Test that branch digits are correctly placed for matriz."""
        cnpj = generator.generate(matriz_only=True)
        # Positions 8-11 (indices 8, 9, 10, 11) should be "0001"
        assert cnpj.value[8:12] == "0001"

    def test_branch_position_filial(
        self,
        generator: DeterministicCNPJGenerator
    ) -> None:
        """Test that branch digits are correctly placed for filial."""
        cnpj = generator.generate(matriz_only=False)
        # Positions 8-11 should contain valid branch number
        branch = cnpj.value[8:12]
        assert len(branch) == 4
        assert branch.isdigit()
        branch_num = int(branch)
        assert 1 <= branch_num <= 9999

    # ========================================================================
    # Check digit calculation tests
    # ========================================================================

    def test_check_digits_are_calculated_correctly(
        self,
        generator: DeterministicCNPJGenerator,
        validator: ModuloElevenCNPJValidator
    ) -> None:
        """Test that check digits are calculated correctly."""
        cnpj = generator.generate(matriz_only=True)
        
        # Validate the entire CNPJ
        assert validator.validate(cnpj) is True
        
        # Check digit positions
        first_check = cnpj.value[12]
        second_check = cnpj.value[13]
        
        # Both should be digits
        assert first_check.isdigit()
        assert second_check.isdigit()

    def test_calculate_check_digit_method(self) -> None:
        """Test the _calculate_check_digit static method directly."""
        weights = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        
        # Test with known values
        digit = DeterministicCNPJGenerator._calculate_check_digit(
            "112223330001", 
            weights
        )
        assert 0 <= digit <= 9
        
        # Test that it returns consistent results
        digit2 = DeterministicCNPJGenerator._calculate_check_digit(
            "112223330001", 
            weights
        )
        assert digit == digit2
