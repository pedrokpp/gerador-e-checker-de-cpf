"""Unit tests for domain entities."""

import pytest

from src.cpf.domain.entities import CPF
from src.cpf.domain.region import Region


class TestCPF:
    """Test suite for CPF entity."""

    def test_create_valid_cpf(self) -> None:
        """Test creating a CPF with valid format."""
        cpf = CPF("12345678909")
        assert cpf.value == "12345678909"

    def test_create_cpf_invalid_length(self) -> None:
        """Test that CPF with invalid length raises ValueError."""
        with pytest.raises(ValueError, match="CPF inválido"):
            CPF("123456789")  # Too short

        with pytest.raises(ValueError, match="CPF inválido"):
            CPF("123456789012")  # Too long

    def test_create_cpf_non_numeric(self) -> None:
        """Test that CPF with non-numeric characters raises ValueError."""
        with pytest.raises(ValueError, match="CPF inválido"):
            CPF("123.456.789-09")  # Has formatting

        with pytest.raises(ValueError, match="CPF inválido"):
            CPF("1234567890a")  # Has letter

    def test_parse_formatted_cpf(self) -> None:
        """Test parsing a formatted CPF string."""
        cpf = CPF.parse("123.456.789-09")
        assert cpf.value == "12345678909"

    def test_parse_unformatted_cpf(self) -> None:
        """Test parsing an unformatted CPF string."""
        cpf = CPF.parse("12345678909")
        assert cpf.value == "12345678909"

    def test_parse_removes_all_formatting(self) -> None:
        """Test that parse removes all non-digit characters."""
        cpf = CPF.parse("123.456.789-09")
        assert cpf.value == "12345678909"

        cpf = CPF.parse("123 456 789 09")
        assert cpf.value == "12345678909"

    def test_formatted_output(self) -> None:
        """Test formatted representation of CPF."""
        cpf = CPF("12345678909")
        assert cpf.formatted() == "123.456.789-09"

    def test_str_representation(self) -> None:
        """Test string representation of CPF."""
        cpf = CPF("12345678909")
        assert str(cpf) == "123.456.789-09"

    def test_get_region(self) -> None:
        """Test getting region from CPF."""
        cpf = CPF("12345678809")  # 8 at position 8 = São Paulo
        assert cpf.region() == Region.SAO_PAULO

        cpf = CPF("12345678909")  # 9 at position 8 = PR/SC
        assert cpf.region() == Region.SUL

        cpf = CPF("12345678009")  # 0 at position 8 = RS
        assert cpf.region() == Region.RIO_GRANDE_DO_SUL

    def test_cpf_immutability(self) -> None:
        """Test that CPF is immutable (frozen dataclass)."""
        cpf = CPF("12345678909")
        with pytest.raises(AttributeError):
            cpf.value = "98765432100"  # type: ignore

    def test_cpf_equality(self) -> None:
        """Test CPF equality comparison."""
        cpf1 = CPF("12345678909")
        cpf2 = CPF("12345678909")
        cpf3 = CPF("98765432100")

        assert cpf1 == cpf2
        assert cpf1 != cpf3


class TestRegion:
    """Test suite for Region enum."""

    def test_region_values(self) -> None:
        """Test that region enum has correct values."""
        assert Region.RIO_GRANDE_DO_SUL.value == 0
        assert Region.CENTRO_OESTE.value == 1
        assert Region.NORTE.value == 2
        assert Region.SAO_PAULO.value == 8
        assert Region.SUL.value == 9

    def test_region_descriptions(self) -> None:
        """Test region descriptions."""
        assert Region.SAO_PAULO.get_description() == "São Paulo"
        assert "Rio Grande do Sul" in Region.RIO_GRANDE_DO_SUL.get_description()
        assert "Paraná" in Region.SUL.get_description()

    @pytest.mark.parametrize("state_abbr,expected_region", [
        ("SP", Region.SAO_PAULO),
        ("RJ", Region.SUDESTE_NORTE),
        ("MG", Region.MINAS_GERAIS),
        ("RS", Region.RIO_GRANDE_DO_SUL),
        ("PR", Region.SUL),
        ("SC", Region.SUL),
        ("BA", Region.NORDESTE_SUL),
        ("CE", Region.NORDESTE_NORTE),
        ("DF", Region.CENTRO_OESTE),
        ("AM", Region.NORTE),
    ])
    def test_from_name_abbreviations(self, state_abbr: str, expected_region: Region) -> None:
        """Test getting region from state abbreviations."""
        assert Region.from_name(state_abbr) == expected_region

    @pytest.mark.parametrize("state_name,expected_region", [
        ("São Paulo", Region.SAO_PAULO),
        ("Sao Paulo", Region.SAO_PAULO),
        ("SAO PAULO", Region.SAO_PAULO),
        ("Rio de Janeiro", Region.SUDESTE_NORTE),
        ("Minas Gerais", Region.MINAS_GERAIS),
        ("Rio Grande do Sul", Region.RIO_GRANDE_DO_SUL),
        ("Paraná", Region.SUL),
        ("Santa Catarina", Region.SUL),
    ])
    def test_from_name_full_names(self, state_name: str, expected_region: Region) -> None:
        """Test getting region from full state names."""
        assert Region.from_name(state_name) == expected_region

    def test_from_name_case_insensitive(self) -> None:
        """Test that from_name is case insensitive."""
        assert Region.from_name("sp") == Region.SAO_PAULO
        assert Region.from_name("SP") == Region.SAO_PAULO
        assert Region.from_name("Sp") == Region.SAO_PAULO
        assert Region.from_name("são paulo") == Region.SAO_PAULO
        assert Region.from_name("SÃO PAULO") == Region.SAO_PAULO

    def test_from_name_invalid_state(self) -> None:
        """Test that invalid state name raises ValueError."""
        with pytest.raises(ValueError, match="Estado não reconhecido"):
            Region.from_name("Invalid State")

        with pytest.raises(ValueError, match="Estado não reconhecido"):
            Region.from_name("XY")

    def test_all_regions_have_descriptions(self) -> None:
        """Test that all regions have descriptions."""
        for region in Region:
            description = region.get_description()
            assert isinstance(description, str)
            assert len(description) > 0
