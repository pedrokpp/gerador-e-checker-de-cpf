"""Integration tests for public API."""

import pytest

import src.cpf as cpf


class TestValidateAPI:
    """Integration tests for validate() function."""

    # ========================================================================
    # ISSUE #2 - Critical test cases
    # ========================================================================

    @pytest.mark.parametrize("cpf_str", [
        "49435142940",
        "494.351.429-40",
        "65492612280",
        "654.926.122-80",
        "13292301670",
        "132.923.016-70",
        "91875881450",
        "918.758.814-50",
    ])
    def test_issue_2_cpfs_are_valid(self, cpf_str: str) -> None:
        """Test that CPFs from issue #2 are correctly validated.
        
        This is the main regression test for issue #2.
        All these CPFs should return True.
        """
        result = cpf.validate(cpf_str)
        assert result is True, f"CPF {cpf_str} should be valid (issue #2 regression test)"

    # ========================================================================
    # Valid CPFs
    # ========================================================================

    @pytest.mark.parametrize("cpf_str", [
        "00000000191",  # Valid CPF from unit tests
    ])
    def test_validate_valid_cpfs(self, cpf_str: str) -> None:
        """Test validation of known valid CPFs."""
        assert cpf.validate(cpf_str) is True

    def test_validate_with_region_info(self) -> None:
        """Test validation with region information."""
        result = cpf.validate("494.351.429-40", show_region=True)
        assert isinstance(result, dict)
        assert result["valid"] is True
        assert result["region"] == "Paraná – Santa Catarina"

    # ========================================================================
    # Invalid CPFs
    # ========================================================================

    @pytest.mark.parametrize("cpf_str", [
        "111.111.111-11",
        "11111111111",
        "000.000.000-00",
        "00000000000",
        "12345678901",  # Invalid check digits
    ])
    def test_validate_invalid_cpfs(self, cpf_str: str) -> None:
        """Test validation of known invalid CPFs."""
        assert cpf.validate(cpf_str) is False

    def test_validate_invalid_with_region_info(self) -> None:
        """Test validation of invalid CPF with region info request."""
        result = cpf.validate("111.111.111-11", show_region=True)
        assert isinstance(result, dict)
        assert result["valid"] is False
        assert result["region"] is None

    def test_validate_malformed_cpf(self) -> None:
        """Test validation of malformed CPF."""
        assert cpf.validate("123") is False
        assert cpf.validate("abcdefghijk") is False
        assert cpf.validate("") is False


class TestGenerateAPI:
    """Integration tests for generate() function."""

    def test_generate_single_cpf(self) -> None:
        """Test generating a single CPF."""
        cpfs = cpf.generate()
        assert len(cpfs) == 1
        assert cpf.validate(cpfs[0]) is True

    def test_generate_multiple_cpfs(self) -> None:
        """Test generating multiple CPFs."""
        cpfs = cpf.generate(count=10)
        assert len(cpfs) == 10
        for generated_cpf in cpfs:
            assert cpf.validate(generated_cpf) is True

    def test_generate_formatted_cpf(self) -> None:
        """Test that generated CPF is formatted by default."""
        cpfs = cpf.generate(formatted=True)
        assert "." in cpfs[0]
        assert "-" in cpfs[0]
        assert len(cpfs[0]) == 14  # XXX.XXX.XXX-XX

    def test_generate_unformatted_cpf(self) -> None:
        """Test generating unformatted CPF."""
        cpfs = cpf.generate(formatted=False)
        assert "." not in cpfs[0]
        assert "-" not in cpfs[0]
        assert len(cpfs[0]) == 11  # XXXXXXXXXXX

    def test_generate_with_region_number(self) -> None:
        """Test generating CPF for specific region (by number)."""
        cpfs = cpf.generate(count=5, region=8)  # São Paulo
        for generated_cpf in cpfs:
            assert cpf.validate(generated_cpf) is True
            # Check 9th digit (index 8 in unformatted, or char 10 in formatted)
            unformatted = generated_cpf.replace(".", "").replace("-", "")
            assert unformatted[8] == "8"

    @pytest.mark.parametrize("state,expected_digit", [
        ("SP", "8"),
        ("RJ", "7"),
        ("MG", "6"),
        ("RS", "0"),
        ("PR", "9"),
        ("SC", "9"),
        ("BA", "5"),
    ])
    def test_generate_with_region_name(self, state: str, expected_digit: str) -> None:
        """Test generating CPF for specific region (by state name)."""
        cpfs = cpf.generate(count=1, region=state)
        assert len(cpfs) == 1
        assert cpf.validate(cpfs[0]) is True
        unformatted = cpfs[0].replace(".", "").replace("-", "")
        assert unformatted[8] == expected_digit

    def test_generate_random_region(self) -> None:
        """Test generating CPF with random region."""
        cpfs = cpf.generate(count=20, region=None)
        assert len(cpfs) == 20
        # Check that we get some variety in regions (probabilistic)
        region_digits = set()
        for generated_cpf in cpfs:
            unformatted = generated_cpf.replace(".", "").replace("-", "")
            region_digits.add(unformatted[8])
        # With 20 CPFs, very likely to have more than 1 region
        assert len(region_digits) > 1

    def test_generate_invalid_count(self) -> None:
        """Test that invalid count raises error."""
        with pytest.raises(ValueError, match="pelo menos 1"):
            cpf.generate(count=0)

        with pytest.raises(ValueError, match="pelo menos 1"):
            cpf.generate(count=-1)

    def test_generate_invalid_region(self) -> None:
        """Test that invalid region raises error."""
        with pytest.raises(ValueError, match="Região inválida"):
            cpf.generate(region=10)

        with pytest.raises(ValueError, match="Estado não reconhecido"):
            cpf.generate(region="INVALID")


class TestBackwardCompatibilityAPI:
    """Integration tests for backward compatibility functions."""

    def test_checar_valid_cpf(self) -> None:
        """Test checar() with valid CPF."""
        assert cpf.checar("494.351.429-40") is True
        assert cpf.checar("49435142940") is True

    def test_checar_invalid_cpf(self) -> None:
        """Test checar() with invalid CPF."""
        assert cpf.checar("111.111.111-11") is False
        assert cpf.checar("11111111111") is False

    def test_checar_issue_2_cpfs(self) -> None:
        """Test that checar() correctly validates CPFs from issue #2."""
        assert cpf.checar("49435142940") is True
        assert cpf.checar("65492612280") is True
        assert cpf.checar("13292301670") is True
        assert cpf.checar("91875881450") is True

    def test_checar_with_region_display(self, capsys: pytest.CaptureFixture) -> None:
        """Test checar() with region display (prints to stdout)."""
        result = cpf.checar("494.351.429-40", regiao=True)
        assert result is True
        
        captured = capsys.readouterr()
        assert "Paraná" in captured.out or "Santa Catarina" in captured.out

    def test_gerar_single_cpf(self) -> None:
        """Test gerar() generates single CPF by default."""
        cpfs = cpf.gerar()
        assert len(cpfs) == 1
        assert cpf.checar(cpfs[0]) is True

    def test_gerar_multiple_cpfs(self) -> None:
        """Test gerar() with multiple CPFs."""
        cpfs = cpf.gerar(quantidade=5)
        assert len(cpfs) == 5
        for generated_cpf in cpfs:
            assert cpf.checar(generated_cpf) is True

    def test_gerar_with_region(self) -> None:
        """Test gerar() with specific region."""
        cpfs = cpf.gerar(quantidade=3, regiao=8)
        assert len(cpfs) == 3
        for generated_cpf in cpfs:
            assert cpf.checar(generated_cpf) is True
            unformatted = generated_cpf.replace(".", "").replace("-", "")
            assert unformatted[8] == "8"

    def test_gerar_always_formatted(self) -> None:
        """Test that gerar() always returns formatted CPFs (backward compatibility)."""
        cpfs = cpf.gerar(quantidade=5)
        for generated_cpf in cpfs:
            assert "." in generated_cpf
            assert "-" in generated_cpf
            assert len(generated_cpf) == 14


class TestAPIConsistency:
    """Test consistency between old and new APIs."""

    def test_validate_and_checar_same_result_valid(self) -> None:
        """Test that validate() and checar() return same result for valid CPF."""
        test_cpf = "494.351.429-40"
        assert cpf.validate(test_cpf) == cpf.checar(test_cpf)

    def test_validate_and_checar_same_result_invalid(self) -> None:
        """Test that validate() and checar() return same result for invalid CPF."""
        test_cpf = "111.111.111-11"
        assert cpf.validate(test_cpf) == cpf.checar(test_cpf)

    def test_generate_and_gerar_both_valid(self) -> None:
        """Test that both generate() and gerar() produce valid CPFs."""
        new_cpfs = cpf.generate(count=10)
        old_cpfs = cpf.gerar(quantidade=10)
        
        assert len(new_cpfs) == 10
        assert len(old_cpfs) == 10
        
        for new_cpf in new_cpfs:
            assert cpf.validate(new_cpf) is True
        
        for old_cpf in old_cpfs:
            assert cpf.checar(old_cpf) is True
