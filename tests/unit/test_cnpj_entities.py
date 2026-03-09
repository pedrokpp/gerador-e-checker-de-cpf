"""Unit tests for CNPJ entity."""

import pytest

from src.cnpj.domain.entities import CNPJ


class TestCNPJEntity:
    """Test suite for CNPJ entity."""

    # ========================================================================
    # Valid CNPJ creation
    # ========================================================================

    def test_create_valid_cnpj(self) -> None:
        """Test creating a CNPJ with valid format."""
        cnpj = CNPJ("11222333000181")
        assert cnpj.value == "11222333000181"

    def test_cnpj_is_immutable(self) -> None:
        """Test that CNPJ is immutable (frozen dataclass)."""
        cnpj = CNPJ("11222333000181")
        with pytest.raises(Exception):  # FrozenInstanceError
            cnpj.value = "99999999999999"  # type: ignore

    # ========================================================================
    # Invalid CNPJ creation
    # ========================================================================

    @pytest.mark.parametrize("invalid_cnpj", [
        "123",  # Too short
        "123456789012345",  # Too long
        "1234567890123",  # 13 digits
        "abcdefghijklmn",  # Letters
        "11.222.333/0001-81",  # Formatted (not normalized)
        "",  # Empty
        "11 222 333 0001 81",  # With spaces
    ])
    def test_create_invalid_format_raises(self, invalid_cnpj: str) -> None:
        """Test that invalid CNPJ formats raise ValueError."""
        with pytest.raises(ValueError, match="CNPJ inválido"):
            CNPJ(invalid_cnpj)

    # ========================================================================
    # Parse method
    # ========================================================================

    def test_parse_formatted_cnpj(self) -> None:
        """Test parsing a formatted CNPJ."""
        cnpj = CNPJ.parse("11.222.333/0001-81")
        assert cnpj.value == "11222333000181"

    def test_parse_unformatted_cnpj(self) -> None:
        """Test parsing an unformatted CNPJ."""
        cnpj = CNPJ.parse("11222333000181")
        assert cnpj.value == "11222333000181"

    def test_parse_cnpj_with_spaces(self) -> None:
        """Test parsing a CNPJ with spaces."""
        cnpj = CNPJ.parse("11 222 333 0001 81")
        assert cnpj.value == "11222333000181"

    def test_parse_cnpj_with_mixed_formatting(self) -> None:
        """Test parsing a CNPJ with mixed formatting."""
        cnpj = CNPJ.parse("11.222.333-0001/81")
        assert cnpj.value == "11222333000181"

    def test_parse_invalid_cnpj_raises(self) -> None:
        """Test that parsing invalid CNPJ raises ValueError."""
        with pytest.raises(ValueError):
            CNPJ.parse("123")

    # ========================================================================
    # Formatted output
    # ========================================================================

    def test_formatted_output(self) -> None:
        """Test formatted CNPJ output."""
        cnpj = CNPJ("11222333000181")
        assert cnpj.formatted() == "11.222.333/0001-81"

    def test_str_returns_formatted(self) -> None:
        """Test that str() returns formatted CNPJ."""
        cnpj = CNPJ("11222333000181")
        assert str(cnpj) == "11.222.333/0001-81"

    # ========================================================================
    # Matriz/Filial methods
    # ========================================================================

    def test_is_matriz_true(self) -> None:
        """Test is_matriz returns True for headquarters."""
        cnpj = CNPJ("11222333000181")
        assert cnpj.is_matriz() is True

    def test_is_matriz_false(self) -> None:
        """Test is_matriz returns False for branches."""
        cnpj = CNPJ("11222333000281")
        assert cnpj.is_matriz() is False

    def test_branch_number_matriz(self) -> None:
        """Test branch_number returns 0001 for headquarters."""
        cnpj = CNPJ("11222333000181")
        assert cnpj.branch_number() == "0001"

    def test_branch_number_filial(self) -> None:
        """Test branch_number returns correct value for branches."""
        cnpj = CNPJ("11222333123481")
        assert cnpj.branch_number() == "1234"

    @pytest.mark.parametrize("cnpj_str,expected_branch", [
        ("11222333000181", "0001"),
        ("11222333000281", "0002"),
        ("11222333009981", "0099"),
        ("11222333123481", "1234"),
        ("11222333999981", "9999"),
    ])
    def test_branch_numbers(self, cnpj_str: str, expected_branch: str) -> None:
        """Test various branch numbers."""
        cnpj = CNPJ(cnpj_str)
        assert cnpj.branch_number() == expected_branch
