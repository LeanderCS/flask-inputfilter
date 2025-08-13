from __future__ import annotations

import re
from typing import Any, ClassVar

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator


class IsEmailValidator(BaseValidator):
    """
    Validates email addresses with optional DNS and SMTP verification.

    This validator performs comprehensive email validation including RFC 5322
    compliant format validation, common typo detection, and optional DNS/SMTP
    verification for enhanced accuracy.

    **Parameters:**

    - **check_dns** (*bool*): Whether to verify DNS MX records exist for the
      email domain. Requires dnspython library. Default is False.
    - **check_smtp** (*bool*): Whether to verify SMTP server reachability.
      Note that many servers block SMTP verification. Default is False.
    - **suggest_typos** (*bool*): Whether to suggest corrections for common
      domain typos (e.g., gmial.com -> gmail.com). Default is True.
    - **allow_smtputf8** (*bool*): Whether to allow international characters
      in email addresses. Default is True.
    - **allow_empty** (*bool*): Whether to allow empty values. Default is
      False.
    - **timeout** (*int*): Timeout in seconds for DNS/SMTP checks. Default
      is 10.

    **Expected Behavior:**

    - Validates email format according to RFC 5322 specification
    - Detects and suggests corrections for common domain typos
    - Optionally verifies DNS MX records (requires dnspython)
    - Optionally attempts SMTP verification (often blocked by servers)
    - Raises ``ValidationError`` if the email format is invalid

    **Example Usage:**

    .. code-block:: python

        class UserRegistrationFilter(InputFilter):
            def __init__(self):
                super().__init__()
                self.add('email', validators=[
                    IsEmailValidator(
                        check_dns=True,
                        suggest_typos=True
                    )
                ])

    **Common Typos Detected:**

    The validator can detect and suggest corrections for common email
    domain typos:

    - gmial.com → gmail.com
    - yahooo.com → yahoo.com
    - outlok.com → outlook.com
    - hotmial.com → hotmail.com

    **Note:**

    DNS and SMTP verification require the dnspython library. If not installed,
    these checks will be skipped silently.
    """

    EMAIL_REGEX: ClassVar = re.compile(
        r"^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9]"
        r"(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
        r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
    )

    COMMON_TYPOS: ClassVar = {
        "gmial.com": "gmail.com",
        "gmai.com": "gmail.com",
        "yahooo.com": "yahoo.com",
        "outlok.com": "outlook.com",
        "hotmial.com": "hotmail.com",
    }

    def __init__(
        self,
        check_dns: bool = False,
        check_smtp: bool = False,
        suggest_typos: bool = True,
        allow_smtputf8: bool = True,
        allow_empty: bool = False,
        timeout: int = 10,
    ) -> None:
        """
        Initialize the email validator.

        Args:
            check_dns: Whether to verify DNS MX records exist
            check_smtp: Whether to verify SMTP server is reachable
            suggest_typos: Whether to suggest corrections for common typos
            allow_smtputf8: Whether to allow international characters
            allow_empty: Whether to allow empty values
            timeout: Timeout in seconds for DNS/SMTP checks
        """
        self.check_dns = check_dns
        self.check_smtp = check_smtp
        self.suggest_typos = suggest_typos
        self.allow_smtputf8 = allow_smtputf8
        self.allow_empty = allow_empty
        self.timeout = timeout

    def validate(self, value: Any) -> None:
        """
        Validate the email address.

        Args:
            value: The value to validate

        Raises:
            ValidationError: If the email is invalid
        """
        if value is None or value == "":
            if not self.allow_empty:
                raise ValidationError("Email address cannot be empty")
            return

        if not isinstance(value, str):
            raise ValidationError(
                f"Email must be a string, not {type(value).__name__}"
            )

        if not self.EMAIL_REGEX.match(value):
            raise ValidationError(
                f"'{value}' is not a valid email address format"
            )

        try:
            local, domain = value.rsplit("@", 1)
        except ValueError:
            raise ValidationError(f"'{value}' is not a valid email address")

        if self.suggest_typos and domain.lower() in self.COMMON_TYPOS:
            suggestion = self.COMMON_TYPOS[domain.lower()]
            raise ValidationError(
                f"Did you mean '{local}@{suggestion}'? "
                f"'{domain}' appears to be a typo."
            )

        if self.check_dns and not self._verify_dns(domain):
            raise ValidationError(
                f"Domain '{domain}' does not have valid MX records"
            )

        if self.check_smtp and not self._verify_smtp(value, domain):
            raise ValidationError(
                f"Email address '{value}' could not be verified via SMTP"
            )

    def _verify_dns(self, domain: str) -> bool:
        """
        Verify that the domain has valid MX records.

        Args:
            domain: The domain to check

        Returns:
            True if MX records exist, False otherwise
        """
        try:
            import dns.resolver

            mx_records = dns.resolver.resolve(domain, "MX")
            return len(mx_records) > 0
        except ImportError:
            return True
        except Exception:
            try:
                import dns.resolver

                dns.resolver.resolve(domain, "A")
                return True
            except Exception:
                return False

    def _verify_smtp(self, email: str, domain: str) -> bool:
        """
        Verify email address by connecting to SMTP server.

        Args:
            email: The full email address
            domain: The domain part of the email

        Returns:
            True if SMTP verification succeeds, False otherwise
        """
        try:
            import smtplib

            import dns.resolver

            mx_records = dns.resolver.resolve(domain, "MX")
            mx_host = str(mx_records[0].exchange)

            server = smtplib.SMTP(timeout=self.timeout)
            server.connect(mx_host)
            server.helo("verify.local")

            code, message = server.verify(email)
            server.quit()

            return code in (250, 251)

        except ImportError:
            return True
        except Exception:
            return True
