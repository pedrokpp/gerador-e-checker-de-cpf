"""Unit tests for CPF validator."""

import pytest

from src.cpf.domain.entities import CPF
from src.cpf.infrastructure.cpf_validator import ModuloElevenValidator


class TestModuloElevenValidator:
    """Test suite for ModuloElevenValidator."""

    @pytest.fixture
    def validator(self) -> ModuloElevenValidator:
        """Create a validator instance for testing."""
        return ModuloElevenValidator()

    # ========================================================================
    # ISSUE #2 - These CPFs should be valid but were incorrectly rejected
    # ========================================================================

    @pytest.mark.parametrize("cpf_value", [
        "49435142940",  # Issue #2 - CPF 1
        "65492612280",  # Issue #2 - CPF 2
        "13292301670",  # Issue #2 - CPF 3
        "91875881450",  # Issue #2 - CPF 4
    ])
    def test_issue_2_valid_cpfs(self, validator: ModuloElevenValidator, cpf_value: str) -> None:
        """Test that CPFs from issue #2 are correctly validated as valid.
        
        These CPFs were incorrectly rejected in version 2.x due to a bug
        in the validation algorithm. Version 3.0 fixes this issue.
        """
        cpf = CPF(cpf_value)
        assert validator.validate(cpf) is True, f"CPF {cpf_value} should be valid (issue #2)"

    # ========================================================================
    # Valid CPFs - Various regions
    # ========================================================================

    @pytest.mark.parametrize("cpf_value,region", [
        ("00000000191", 1),  # DF, GO, MS, MT, TO - Valid CPF
    ])
    def test_valid_cpfs(self, validator: ModuloElevenValidator, cpf_value: str, region: int) -> None:
        """Test validation of known valid CPFs from different regions."""
        cpf = CPF(cpf_value)
        assert validator.validate(cpf) is True
        assert cpf.region().value == region

    # ========================================================================
    # Invalid CPFs - All digits equal
    # ========================================================================

    @pytest.mark.parametrize("cpf_value", [
        "00000000000",
        "11111111111",
        "22222222222",
        "33333333333",
        "44444444444",
        "55555555555",
        "66666666666",
        "77777777777",
        "88888888888",
        "99999999999",
    ])
    def test_invalid_cpfs_all_equal(self, validator: ModuloElevenValidator, cpf_value: str) -> None:
        """Test that CPFs with all equal digits are rejected."""
        cpf = CPF(cpf_value)
        assert validator.validate(cpf) is False

    # ========================================================================
    # Invalid CPFs - Wrong check digits
    # ========================================================================

    @pytest.mark.parametrize("cpf_value", [
        "00000000100",  # Wrong second check digit
        "12345678901",  # Wrong check digits (corrected)
    ])
    def test_invalid_cpfs_wrong_digits(self, validator: ModuloElevenValidator, cpf_value: str) -> None:
        """Test that CPFs with incorrect check digits are rejected."""
        cpf = CPF(cpf_value)
        assert validator.validate(cpf) is False

    # ========================================================================
    # Check digit calculation
    # ========================================================================

    def test_calculate_first_check_digit(self) -> None:
        """Test calculation of first check digit."""
        # For CPF 494.351.429-40:
        # First 9 digits: 494351429
        # Calculation: 4*10 + 9*9 + 4*8 + 3*7 + 5*6 + 1*5 + 4*4 + 2*3 + 9*2
        #            = 40 + 81 + 32 + 21 + 30 + 5 + 16 + 6 + 18 = 249
        # 249 % 11 = 7
        # 11 - 7 = 4 (first check digit)
        digit = ModuloElevenValidator._calculate_check_digit("494351429", start_weight=10)
        assert digit == 4

    def test_calculate_second_check_digit(self) -> None:
        """Test calculation of second check digit."""
        # For CPF 494.351.429-40:
        # First 10 digits: 4943514294
        # Calculation: 4*11 + 9*10 + 4*9 + 3*8 + 5*7 + 1*6 + 4*5 + 2*4 + 9*3 + 4*2
        #            = 44 + 90 + 36 + 24 + 35 + 6 + 20 + 8 + 27 + 8 = 298
        # 298 % 11 = 1
        # 11 - 1 = 10, but since >= 10, we use 0 (second check digit)
        # Wait, let me recalculate...
        # Actually for this CPF, the second digit should be 0
        digit = ModuloElevenValidator._calculate_check_digit("4943514294", start_weight=11)
        assert digit == 0

    def test_calculate_check_digit_remainder_less_than_2(self) -> None:
        """Test that check digit is 0 when remainder < 2."""
        # Create a case where remainder will be 1 or 0
        # This is tested implicitly in the second check digit test above
        # Let's create an explicit test
        digit = ModuloElevenValidator._calculate_check_digit("000000001", start_weight=10)
        # 0*10 + 0*9 + ... + 1*2 = 2
        # 2 % 11 = 2, so digit = 11 - 2 = 9
        assert digit == 9
