"""Tests for PasswordStrengthValidator."""

import pytest
import math

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import PasswordStrengthValidator


class TestPasswordStrengthValidator:
    """Test cases for PasswordStrengthValidator."""
    
    def test_valid_passwords(self):
        """Test that valid passwords pass validation."""
        validator = PasswordStrengthValidator(
            min_length=8,
            require_uppercase=True,
            require_lowercase=True,
            require_digits=True,
            require_special=True
        )
        
        valid_passwords = [
            "Password123!",
            "Str0ng&Secure",
            "MyP@ssw0rd2023",
            "C0mpl3x!Pass",
            "V@lidP4ssword",
        ]
        
        for password in valid_passwords:
            validator.validate(password)  # Should not raise
    
    def test_length_requirements(self):
        """Test minimum and maximum length requirements."""
        validator = PasswordStrengthValidator(
            min_length=8,
            max_length=20,
            require_uppercase=False,
            require_lowercase=False,
            require_digits=False,
            require_special=False
        )
        
        # Too short
        with pytest.raises(ValidationError) as exc_info:
            validator.validate("short")
        assert "at least 8 characters" in str(exc_info.value)
        
        # Too long
        with pytest.raises(ValidationError) as exc_info:
            validator.validate("a" * 21)
        assert "must not exceed 20 characters" in str(exc_info.value)
        
        # Just right
        validator.validate("a" * 8)  # Min length
        validator.validate("a" * 20)  # Max length
    
    def test_character_type_requirements(self):
        """Test character type requirements."""
        # Require uppercase
        validator_upper = PasswordStrengthValidator(
            min_length=1,
            require_uppercase=True,
            min_uppercase=2,
            require_lowercase=False,
            require_digits=False,
            require_special=False
        )
        
        with pytest.raises(ValidationError) as exc_info:
            validator_upper.validate("password")
        assert "uppercase letter" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            validator_upper.validate("Password")  # Only 1 uppercase
        assert "at least 2 uppercase" in str(exc_info.value)
        
        validator_upper.validate("PASSword")  # 4 uppercase, passes
        
        # Require lowercase
        validator_lower = PasswordStrengthValidator(
            min_length=1,
            require_uppercase=False,
            require_lowercase=True,
            min_lowercase=2,
            require_digits=False,
            require_special=False
        )
        
        with pytest.raises(ValidationError) as exc_info:
            validator_lower.validate("PASSWORD")
        assert "lowercase letter" in str(exc_info.value)
        
        validator_lower.validate("password")  # Passes
        
        # Require digits
        validator_digit = PasswordStrengthValidator(
            min_length=1,
            require_uppercase=False,
            require_lowercase=False,
            require_digits=True,
            min_digits=2,
            require_special=False
        )
        
        with pytest.raises(ValidationError) as exc_info:
            validator_digit.validate("password")
        assert "digit" in str(exc_info.value)
        
        validator_digit.validate("pass123")  # Passes
        
        # Require special characters
        validator_special = PasswordStrengthValidator(
            min_length=1,
            require_uppercase=False,
            require_lowercase=False,
            require_digits=False,
            require_special=True,
            min_special=2,
            special_chars="!@#$"
        )
        
        with pytest.raises(ValidationError) as exc_info:
            validator_special.validate("password")
        assert "special character" in str(exc_info.value)
        
        validator_special.validate("pass!@")  # Passes
    
    def test_common_passwords(self):
        """Test detection of common passwords."""
        validator = PasswordStrengthValidator(
            min_length=1,
            require_uppercase=False,
            require_lowercase=False,
            require_digits=False,
            require_special=False,
            check_common=True
        )
        
        common_passwords = [
            "password",
            "123456",
            "qwerty",
            "admin",
            "letmein",
            "monkey",
            "dragon",
        ]
        
        for password in common_passwords:
            with pytest.raises(ValidationError) as exc_info:
                validator.validate(password)
            assert "too common" in str(exc_info.value)
        
        # Case insensitive check
        with pytest.raises(ValidationError) as exc_info:
            validator.validate("PASSWORD")
        assert "too common" in str(exc_info.value)
        
        # Disable common password check
        validator_no_common = PasswordStrengthValidator(
            min_length=1,
            require_uppercase=False,
            require_lowercase=False,
            require_digits=False,
            require_special=False,
            check_common=False
        )
        validator_no_common.validate("password")  # Should not raise
    
    def test_keyboard_patterns(self):
        """Test detection of keyboard patterns."""
        validator = PasswordStrengthValidator(
            min_length=1,
            require_uppercase=False,
            require_lowercase=False,
            require_digits=False,
            require_special=False,
            check_patterns=True
        )
        
        keyboard_patterns = [
            "qwerty123",
            "asdfgh456",
            "zxcvbn789",
            "12345abc",
            "qazwsxedc",
        ]
        
        for password in keyboard_patterns:
            with pytest.raises(ValidationError) as exc_info:
                validator.validate(password)
            assert "keyboard patterns" in str(exc_info.value)
        
        # Reverse patterns
        with pytest.raises(ValidationError) as exc_info:
            validator.validate("ytrewq")
        assert "keyboard patterns" in str(exc_info.value)
        
        # Disable pattern check
        validator_no_patterns = PasswordStrengthValidator(
            min_length=1,
            require_uppercase=False,
            require_lowercase=False,
            require_digits=False,
            require_special=False,
            check_patterns=False
        )
        validator_no_patterns.validate("qwerty")  # Should not raise
    
    def test_repeating_characters(self):
        """Test detection of repeating characters."""
        validator = PasswordStrengthValidator(
            min_length=1,
            require_uppercase=False,
            require_lowercase=False,
            require_digits=False,
            require_special=False,
            disallow_repeating=3
        )
        
        # 3 repeating characters (threshold)
        with pytest.raises(ValidationError) as exc_info:
            validator.validate("paasssword")  # 3 s's
        assert "repeating characters" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate("111password")
        assert "repeating characters" in str(exc_info.value)
        
        # 2 repeating is fine
        validator.validate("paassword")  # Should not raise
        
        # Disable repeating check
        validator_no_repeat = PasswordStrengthValidator(
            min_length=1,
            require_uppercase=False,
            require_lowercase=False,
            require_digits=False,
            require_special=False,
            disallow_repeating=0
        )
        validator_no_repeat.validate("aaaaaa")  # Should not raise
    
    def test_sequential_characters(self):
        """Test detection of sequential characters."""
        validator = PasswordStrengthValidator(
            min_length=1,
            require_uppercase=False,
            require_lowercase=False,
            require_digits=False,
            require_special=False,
            disallow_sequential=3
        )
        
        # Sequential letters
        with pytest.raises(ValidationError) as exc_info:
            validator.validate("abcpassword")
        assert "sequential characters" in str(exc_info.value)
        
        # Sequential numbers
        with pytest.raises(ValidationError) as exc_info:
            validator.validate("password123")
        assert "sequential characters" in str(exc_info.value)
        
        # Reverse sequential
        with pytest.raises(ValidationError) as exc_info:
            validator.validate("cbapassword")
        assert "sequential characters" in str(exc_info.value)
        
        # 2 sequential is fine
        validator.validate("abpassword")  # Should not raise
        
        # Disable sequential check
        validator_no_seq = PasswordStrengthValidator(
            min_length=1,
            require_uppercase=False,
            require_lowercase=False,
            require_digits=False,
            require_special=False,
            disallow_sequential=0
        )
        validator_no_seq.validate("abcdef")  # Should not raise
    
    def test_entropy_calculation(self):
        """Test password entropy calculation."""
        validator = PasswordStrengthValidator(
            min_length=1,
            require_uppercase=False,
            require_lowercase=False,
            require_digits=False,
            require_special=False,
            require_entropy=30.0
        )
        
        # Low entropy password
        with pytest.raises(ValidationError) as exc_info:
            validator.validate("password")  # Only lowercase
        assert "entropy" in str(exc_info.value).lower()
        
        # Calculate expected entropy
        # "Password1!" = 10 chars, lowercase + uppercase + digit + special
        # charset = 26 + 26 + 10 + ~30 = ~92
        # entropy = 10 * log2(92) ≈ 65.5 bits
        validator_high = PasswordStrengthValidator(
            min_length=1,
            require_uppercase=False,
            require_lowercase=False,
            require_digits=False,
            require_special=False,
            require_entropy=60.0
        )
        validator_high.validate("Password1!")  # Should pass
        
        # Test with only lowercase (26 chars)
        # "abcdefghij" = 10 chars * log2(26) ≈ 47 bits
        validator_47 = PasswordStrengthValidator(
            min_length=1,
            require_uppercase=False,
            require_lowercase=False,
            require_digits=False,
            require_special=False,
            require_entropy=45.0
        )
        validator_47.validate("abcdefghij")  # Should pass
    
    def test_non_string_input(self):
        """Test that non-string inputs raise ValidationError."""
        validator = PasswordStrengthValidator()
        
        invalid_types = [
            123456,
            12.34,
            ['password'],
            {'password': 'test'},
            True,
            None,
        ]
        
        for value in invalid_types:
            with pytest.raises(ValidationError) as exc_info:
                validator.validate(value)
            assert "must be a string" in str(exc_info.value)
    
    def test_custom_special_characters(self):
        """Test custom special character sets."""
        validator = PasswordStrengthValidator(
            min_length=1,
            require_uppercase=False,
            require_lowercase=False,
            require_digits=False,
            require_special=True,
            special_chars="!@#"
        )
        
        # Valid special char
        validator.validate("password!")
        
        # Invalid special char (not in custom set)
        with pytest.raises(ValidationError) as exc_info:
            validator.validate("password$")  # $ not in "!@#"
        assert "special character" in str(exc_info.value)
    
    def test_all_requirements_combined(self):
        """Test password with all requirements enabled."""
        validator = PasswordStrengthValidator(
            min_length=12,
            max_length=30,
            require_uppercase=True,
            require_lowercase=True,
            require_digits=True,
            require_special=True,
            min_uppercase=2,
            min_lowercase=2,
            min_digits=2,
            min_special=2,
            check_common=True,
            check_patterns=True,
            disallow_repeating=3,
            disallow_sequential=3,
            require_entropy=50.0
        )
        
        # Valid complex password
        validator.validate("MyS3cur3P@ssw0rd!!")
        
        # Invalid - too simple despite meeting basic requirements
        with pytest.raises(ValidationError):
            validator.validate("AAaa11!!")  # Too short
        
        with pytest.raises(ValidationError):
            validator.validate("Password123!")  # Common base word
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        validator = PasswordStrengthValidator(
            min_length=1,
            max_length=1000,
            require_uppercase=False,
            require_lowercase=False,
            require_digits=False,
            require_special=False
        )
        
        # Single character
        validator.validate("a")
        
        # Very long password
        validator.validate("a" * 1000)
        
        # Unicode characters
        validator.validate("пароль密码パスワード")
        
        # Mixed unicode and ASCII
        validator.validate("Password密码123")
    
    def test_empty_password(self):
        """Test empty password handling."""
        validator = PasswordStrengthValidator(min_length=0)
        
        # Empty string should fail even with min_length=0
        # because it fails other checks
        validator_permissive = PasswordStrengthValidator(
            min_length=0,
            require_uppercase=False,
            require_lowercase=False,
            require_digits=False,
            require_special=False
        )
        validator_permissive.validate("")  # Should pass with all requirements disabled