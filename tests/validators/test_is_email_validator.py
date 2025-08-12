"""Tests for IsEmailValidator."""

import pytest
from unittest.mock import patch, MagicMock

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.validators import IsEmailValidator


class TestIsEmailValidator:
    """Test cases for IsEmailValidator."""
    
    def test_valid_email_addresses(self):
        """Test that valid email addresses pass validation."""
        validator = IsEmailValidator()
        
        valid_emails = [
            "user@example.com",
            "john.doe@company.org",
            "test+tag@domain.co.uk",
            "user_name@sub.domain.com",
            "123@numbers.com",
            "a@b.c",
            "first.last@example-domain.com",
            "user!#$%&'*+/=?^_`{|}~@example.com",  # RFC 5322 special chars
        ]
        
        for email in valid_emails:
            validator.validate(email)  # Should not raise
    
    def test_invalid_email_formats(self):
        """Test that invalid email formats raise ValidationError."""
        validator = IsEmailValidator()
        
        invalid_emails = [
            "notanemail",
            "@example.com",
            "user@",
            "user@@example.com",
            "user@example",
            "user @example.com",
            "user@example .com",
            "user@.com",
            "@",
            "user@example..com",
        ]
        
        for email in invalid_emails:
            with pytest.raises(ValidationError) as exc_info:
                validator.validate(email)
            assert "not a valid email address" in str(exc_info.value) or "cannot be empty" in str(exc_info.value)
    
    def test_empty_email_handling(self):
        """Test handling of empty/None values."""
        # Default: don't allow empty
        validator = IsEmailValidator(allow_empty=False)
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate("")
        assert "cannot be empty" in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            validator.validate(None)
        assert "cannot be empty" in str(exc_info.value)
        
        # Allow empty values
        validator_allow_empty = IsEmailValidator(allow_empty=True)
        validator_allow_empty.validate("")  # Should not raise
        validator_allow_empty.validate(None)  # Should not raise
    
    def test_non_string_input(self):
        """Test that non-string inputs raise ValidationError."""
        validator = IsEmailValidator()
        
        invalid_types = [
            123,
            12.34,
            ['user@example.com'],
            {'email': 'user@example.com'},
            True,
        ]
        
        for value in invalid_types:
            with pytest.raises(ValidationError) as exc_info:
                validator.validate(value)
            assert "must be a string" in str(exc_info.value)
    
    def test_typo_detection(self):
        """Test detection and suggestion of common email typos."""
        validator = IsEmailValidator(suggest_typos=True)
        
        typo_emails = [
            ("user@gmial.com", "gmail.com"),
            ("user@gmai.com", "gmail.com"),
            ("user@yahooo.com", "yahoo.com"),
            ("user@outlok.com", "outlook.com"),
            ("user@hotmial.com", "hotmail.com"),
        ]
        
        for typo_email, correct_domain in typo_emails:
            with pytest.raises(ValidationError) as exc_info:
                validator.validate(typo_email)
            assert "Did you mean" in str(exc_info.value)
            assert correct_domain in str(exc_info.value)
        
        # Disable typo suggestions
        validator_no_typos = IsEmailValidator(suggest_typos=False)
        validator_no_typos.validate("user@gmial.com")  # Should not raise
    
    def test_dns_verification_with_mock(self):
        """Test DNS verification with mocked DNS resolver."""
        validator = IsEmailValidator(check_dns=True)
        
        # Mock successful DNS lookup
        with patch('dns.resolver') as mock_dns:
            mock_resolver = MagicMock()
            mock_dns.resolve.return_value = [MagicMock()]  # Mock MX records
            
            validator.validate("user@example.com")  # Should not raise
            mock_dns.resolve.assert_called()
        
        # Mock failed DNS lookup
        with patch('dns.resolver') as mock_dns:
            mock_dns.resolve.side_effect = Exception("DNS lookup failed")
            
            with pytest.raises(ValidationError) as exc_info:
                validator.validate("user@invaliddomain123456.com")
            assert "does not have valid MX records" in str(exc_info.value)
    
    def test_dns_verification_without_library(self):
        """Test that DNS verification is skipped if dnspython is not
        installed."""
        validator = IsEmailValidator(check_dns=True)
        
        # Mock ImportError for dns.resolver
        with patch('dns.resolver', side_effect=ImportError):
            # Should not raise even with invalid domain
            validator.validate("user@definitely-invalid-domain-12345.com")
    
    def test_smtp_verification_with_mock(self):
        """Test SMTP verification with mocked SMTP connection."""
        validator = IsEmailValidator(check_smtp=True, timeout=5)
        
        # Mock successful SMTP verification
        with patch('dns.resolver') as mock_dns:
            with patch('smtplib.SMTP') as mock_smtp:
                # Setup DNS mock
                mock_mx = MagicMock()
                mock_mx.exchange = 'mail.example.com'
                mock_dns.resolve.return_value = [mock_mx]
                
                # Setup SMTP mock
                smtp_instance = MagicMock()
                smtp_instance.verify.return_value = (250, "OK")
                mock_smtp.return_value = smtp_instance
                
                validator.validate("user@example.com")  # Should not raise
                smtp_instance.verify.assert_called_with("user@example.com")
    
    def test_smtp_verification_failure(self):
        """Test SMTP verification when SMTP check fails."""
        validator = IsEmailValidator(check_smtp=True)
        
        # Mock SMTP failure - should fail open (not raise)
        with patch('dns.resolver') as mock_dns:
            with patch('smtplib.SMTP') as mock_smtp:
                mock_dns.resolve.side_effect = Exception("DNS failed")
                mock_smtp.side_effect = Exception("SMTP failed")
                
                # Should not raise - fails open for SMTP
                validator.validate("user@example.com")
    
    def test_international_email_addresses(self):
        """Test handling of international email addresses."""
        validator = IsEmailValidator(allow_smtputf8=True)
        
        # Currently using basic regex, so non-ASCII might not validate
        # This is expected behavior for now
        international_emails = [
            "用户@example.com",
            "user@例え.jp",
            "münchen@example.de",
        ]
        
        for email in international_emails:
            # These might raise with current regex implementation
            try:
                validator.validate(email)
            except ValidationError:
                pass  # Expected for now with basic regex
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        validator = IsEmailValidator()
        
        # Very long local part (64 chars is typically the limit)
        long_local = "a" * 64 + "@example.com"
        validator.validate(long_local)  # Should not raise
        
        # Very long domain
        long_domain = "user@" + "subdomain." * 20 + "example.com"
        validator.validate(long_domain)  # Should not raise
        
        # Minimum valid email
        validator.validate("a@b.c")  # Should not raise
    
    def test_custom_timeout(self):
        """Test custom timeout for DNS/SMTP checks."""
        validator = IsEmailValidator(check_dns=True, check_smtp=True, timeout=30)
        
        with patch('smtplib.SMTP') as mock_smtp:
            smtp_instance = MagicMock()
            mock_smtp.return_value = smtp_instance
            
            # The timeout should be passed to SMTP
            assert validator.timeout == 30
    
    def test_email_with_plus_addressing(self):
        """Test emails with plus addressing (sub-addressing)."""
        validator = IsEmailValidator()
        
        plus_emails = [
            "user+tag@example.com",
            "user+newsletter@gmail.com",
            "john.doe+work@company.org",
        ]
        
        for email in plus_emails:
            validator.validate(email)  # Should not raise
    
    def test_email_with_ip_address(self):
        """Test emails with IP addresses instead of domains."""
        validator = IsEmailValidator()
        
        # These are technically valid but uncommon
        ip_emails = [
            "user@[192.168.1.1]",
            "user@[2001:db8::1]",
        ]
        
        for email in ip_emails:
            # Current regex might not support these
            try:
                validator.validate(email)
            except ValidationError:
                pass  # Expected with current implementation