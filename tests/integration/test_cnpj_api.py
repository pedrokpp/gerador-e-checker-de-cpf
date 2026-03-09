"""Integration tests for CNPJ public API."""

import pytest

import src.cnpj as cnpj


class TestValidateCNPJAPI:
    """Integration tests for validate() function."""

    # ========================================================================
    # Valid CNPJs
    # ========================================================================

    @pytest.mark.parametrize("cnpj_str", [
        "11222333000181",
        "11.222.333/0001-81",
        "11444777000161",
        "11.444.777/0001-61",
        "00000000000191",
        "00.000.000/0001-91",
    ])
    def test_validate_valid_cnpjs(self, cnpj_str: str) -> None:
        """Test validation of known valid CNPJs."""
        assert cnpj.validate(cnpj_str) is True

    def test_validate_formatted_and_unformatted(self) -> None:
        """Test that both formatted and unformatted CNPJs work."""
        formatted = "11.222.333/0001-81"
        unformatted = "11222333000181"
        
        assert cnpj.validate(formatted) is True
        assert cnpj.validate(unformatted) is True

    # ========================================================================
    # Invalid CNPJs
    # ========================================================================

    @pytest.mark.parametrize("cnpj_str", [
        "11.111.111/1111-11",
        "11111111111111",
        "00.000.000/0000-00",
        "00000000000000",
        "12345678901234",  # Invalid check digits
        "11222333000180",  # Wrong check digit
    ])
    def test_validate_invalid_cnpjs(self, cnpj_str: str) -> None:
        """Test validation of known invalid CNPJs."""
        assert cnpj.validate(cnpj_str) is False

    def test_validate_malformed_cnpj(self) -> None:
        """Test validation of malformed CNPJs."""
        assert cnpj.validate("123") is False
        assert cnpj.validate("abcdefghijklmn") is False
        assert cnpj.validate("") is False
        assert cnpj.validate("11.222.333") is False

    # ========================================================================
    # All digits equal
    # ========================================================================

    @pytest.mark.parametrize("digit", range(10))
    def test_validate_all_equal_digits(self, digit: int) -> None:
        """Test that CNPJs with all equal digits are invalid."""
        cnpj_str = str(digit) * 14
        assert cnpj.validate(cnpj_str) is False


class TestGenerateCNPJAPI:
    """Integration tests for generate() function."""

    # ========================================================================
    # Basic generation
    # ========================================================================

    def test_generate_single_cnpj(self) -> None:
        """Test generating a single CNPJ."""
        cnpjs = cnpj.generate()
        assert len(cnpjs) == 1
        assert cnpj.validate(cnpjs[0]) is True

    def test_generate_multiple_cnpjs(self) -> None:
        """Test generating multiple CNPJs."""
        cnpjs_list = cnpj.generate(count=10)
        assert len(cnpjs_list) == 10
        for generated_cnpj in cnpjs_list:
            assert cnpj.validate(generated_cnpj) is True

    # ========================================================================
    # Formatting tests
    # ========================================================================

    def test_generate_formatted_cnpj(self) -> None:
        """Test that generated CNPJ is formatted by default."""
        cnpjs = cnpj.generate(formatted=True)
        assert "." in cnpjs[0]
        assert "/" in cnpjs[0]
        assert "-" in cnpjs[0]
        assert len(cnpjs[0]) == 18  # XX.XXX.XXX/XXXX-XX

    def test_generate_unformatted_cnpj(self) -> None:
        """Test generating unformatted CNPJ."""
        cnpjs = cnpj.generate(formatted=False)
        assert "." not in cnpjs[0]
        assert "/" not in cnpjs[0]
        assert "-" not in cnpjs[0]
        assert len(cnpjs[0]) == 14  # XXXXXXXXXXXXXX

    # ========================================================================
    # Matriz/Filial tests
    # ========================================================================

    def test_generate_matriz_only(self) -> None:
        """Test generating only headquarters (matriz) CNPJs."""
        cnpjs_list = cnpj.generate(count=5, matriz_only=True)
        assert len(cnpjs_list) == 5
        
        for generated_cnpj in cnpjs_list:
            assert cnpj.validate(generated_cnpj) is True
            # Check that branch number is 0001
            unformatted = generated_cnpj.replace(".", "").replace("/", "").replace("-", "")
            assert unformatted[8:12] == "0001"

    def test_generate_with_random_filiais(self) -> None:
        """Test generating CNPJs with random branch numbers."""
        cnpjs_list = cnpj.generate(count=20, matriz_only=False)
        assert len(cnpjs_list) == 20
        
        branches = set()
        for generated_cnpj in cnpjs_list:
            assert cnpj.validate(generated_cnpj) is True
            # Extract branch number
            unformatted = generated_cnpj.replace(".", "").replace("/", "").replace("-", "")
            branches.add(unformatted[8:12])
        
        # With 20 CNPJs, very likely to have more than 1 different branch
        assert len(branches) > 1

    # ========================================================================
    # Error handling
    # ========================================================================

    def test_generate_invalid_count(self) -> None:
        """Test that invalid count raises error."""
        with pytest.raises(ValueError, match="pelo menos 1"):
            cnpj.generate(count=0)

        with pytest.raises(ValueError, match="pelo menos 1"):
            cnpj.generate(count=-1)

    # ========================================================================
    # Combined parameters
    # ========================================================================

    def test_generate_unformatted_matriz(self) -> None:
        """Test generating unformatted matriz CNPJs."""
        cnpjs_list = cnpj.generate(count=3, formatted=False, matriz_only=True)
        assert len(cnpjs_list) == 3
        
        for generated_cnpj in cnpjs_list:
            assert len(generated_cnpj) == 14
            assert cnpj.validate(generated_cnpj) is True
            assert generated_cnpj[8:12] == "0001"

    def test_generate_formatted_filiais(self) -> None:
        """Test generating formatted CNPJs with random filiais."""
        cnpjs_list = cnpj.generate(count=5, formatted=True, matriz_only=False)
        assert len(cnpjs_list) == 5
        
        for generated_cnpj in cnpjs_list:
            assert "." in generated_cnpj
            assert "/" in generated_cnpj
            assert "-" in generated_cnpj
            assert cnpj.validate(generated_cnpj) is True


class TestCNPJAPIConsistency:
    """Test consistency and integration between API functions."""

    def test_all_generated_are_valid(self) -> None:
        """Test that all generated CNPJs validate successfully."""
        # Generate various combinations
        test_cases = [
            {"count": 10, "formatted": True, "matriz_only": True},
            {"count": 10, "formatted": False, "matriz_only": True},
            {"count": 10, "formatted": True, "matriz_only": False},
            {"count": 10, "formatted": False, "matriz_only": False},
        ]
        
        for params in test_cases:
            cnpjs_list = cnpj.generate(**params)
            for generated_cnpj in cnpjs_list:
                assert cnpj.validate(generated_cnpj) is True, \
                    f"Generated CNPJ {generated_cnpj} should be valid"

    def test_format_consistency(self) -> None:
        """Test that formatting is consistent."""
        formatted = cnpj.generate(count=1, formatted=True)[0]
        unformatted = cnpj.generate(count=1, formatted=False)[0]
        
        # Both should validate
        assert cnpj.validate(formatted) is True
        assert cnpj.validate(unformatted) is True
        
        # Formatted should have special characters
        assert any(c in formatted for c in [".", "/", "-"])
        
        # Unformatted should not
        assert not any(c in unformatted for c in [".", "/", "-"])

    def test_generate_large_batch(self) -> None:
        """Test generating a large batch of CNPJs."""
        cnpjs_list = cnpj.generate(count=100, matriz_only=True)
        assert len(cnpjs_list) == 100
        
        # All should be valid
        for generated_cnpj in cnpjs_list:
            assert cnpj.validate(generated_cnpj) is True
        
        # Should have variety (not all the same)
        unique_cnpjs = set(cnpjs_list)
        assert len(unique_cnpjs) > 1

    def test_validate_accepts_various_formats(self) -> None:
        """Test that validate accepts various input formats."""
        # Generate a CNPJ
        base_cnpj = cnpj.generate(count=1, formatted=False)[0]
        
        # Format it various ways
        formatted = f"{base_cnpj[:2]}.{base_cnpj[2:5]}.{base_cnpj[5:8]}/{base_cnpj[8:12]}-{base_cnpj[12:]}"
        with_spaces = f"{base_cnpj[:2]} {base_cnpj[2:5]} {base_cnpj[5:8]} {base_cnpj[8:12]} {base_cnpj[12:]}"
        
        # All formats should validate
        assert cnpj.validate(base_cnpj) is True
        assert cnpj.validate(formatted) is True
        assert cnpj.validate(with_spaces) is True
