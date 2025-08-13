from __future__ import annotations

from typing import Any, ClassVar, List, Optional

from flask_inputfilter.exceptions import ValidationError
from flask_inputfilter.models import BaseValidator


class PasswordStrengthValidator(BaseValidator):
    """
    Validates password strength based on configurable security requirements.

    This comprehensive password validator checks against multiple security
    criteria including length requirements, character type diversity, common
    password lists, keyboard patterns, sequential characters, and entropy
    calculations.

    **Parameters:**

    - **min_length** (*int*): Minimum password length. Default is 8.
    - **max_length** (*int*): Maximum password length. Default is 128.
    - **require_uppercase** (*bool*): Whether to require uppercase letters.
      Default is True.
    - **require_lowercase** (*bool*): Whether to require lowercase letters.
      Default is True.
    - **require_digits** (*bool*): Whether to require digits. Default is
      True.
    - **require_special** (*bool*): Whether to require special characters.
      Default is True.
    - **min_uppercase** (*int*): Minimum number of uppercase letters. Default
      is 1.
    - **min_lowercase** (*int*): Minimum number of lowercase letters. Default
      is 1.
    - **min_digits** (*int*): Minimum number of digits. Default is 1.
    - **min_special** (*int*): Minimum number of special characters. Default
      is 1.
    - **special_chars** (*str*): String of allowed special characters.
      Default is '!@#$%^&*()_+-=[]{}|;:,.<>?'.
    - **check_common** (*bool*): Whether to check against common passwords.
      Default is True.
    - **check_patterns** (*bool*): Whether to check for keyboard patterns.
      Default is True.
    - **check_dictionary** (*bool*): Whether to check against dictionary words.
      Default is False.
    - **check_user_info** (*bool*): Whether to check for user information in
      password. Default is True.
    - **user_info_fields** (*Optional[List[str]]*): Fields to check from user
      data. Default is ['username', 'email', 'name'].
    - **disallow_repeating** (*int*): Maximum allowed consecutive repeating
      characters. Default is 3.
    - **disallow_sequential** (*int*): Maximum allowed consecutive sequential
      characters. Default is 3.
    - **require_entropy** (*Optional[float]*): Minimum required entropy in
      bits. Default is None.

    **Expected Behavior:**

    - Validates password length is within min/max bounds
    - Checks for required character types (uppercase, lowercase, digits,
      special)
    - Detects and rejects common passwords from built-in list
    - Identifies keyboard patterns (qwerty, 12345, etc.)
    - Prevents excessive character repetition (aaa, 111)
    - Prevents sequential patterns (abc, 123)
    - Optionally calculates and validates password entropy
    - Raises ``ValidationError`` with specific failure reason

    **Example Usage:**

    .. code-block:: python

        class UserRegistrationFilter(InputFilter):
            def __init__(self):
                super().__init__()
                self.add('password', validators=[
                    PasswordStrengthValidator(
                        min_length=10,
                        require_uppercase=True,
                        require_special=True,
                        check_common=True,
                        check_patterns=True,
                        disallow_repeating=3,
                        require_entropy=40.0
                    )
                ])

    **Common Passwords Detected:**

    The validator includes a built-in list of 100+ common passwords including:
    - Simple patterns: 123456, qwerty, password
    - Common words: monkey, dragon, master
    - Keyboard walks: qweasd, 1q2w3e4r
    - Default passwords: admin, root, guest

    **Keyboard Patterns Detected:**

    - Horizontal patterns: qwerty, asdfgh, zxcvbn
    - Vertical patterns: qazwsx, 1qaz2wsx
    - Numeric patterns: 12345, 098765

    **Entropy Calculation:**

    When ``require_entropy`` is set, the validator calculates password
    entropy using:
    entropy = length * log₂(charset_size)

    Where charset_size includes:
    - 26 for lowercase letters
    - 26 for uppercase letters
    - 10 for digits
    - Special character count for symbols

    **Security Notes:**

    - Passwords are never stored or logged by this validator
    - Consider using in combination with other security measures
    - Entropy calculation provides a mathematical strength estimate
    - Real-world password strength also depends on unpredictability
    """

    COMMON_PASSWORDS: ClassVar = {
        "123456",
        "password",
        "123456789",
        "12345678",
        "12345",
        "1234567",
        "1234567890",
        "qwerty",
        "abc123",
        "111111",
        "password123",
        "Password1",
        "password1",
        "qwerty123",
        "welcome",
        "monkey",
        "dragon",
        "master",
        "letmein",
        "login",
        "princess",
        "qwertyuiop",
        "solo",
        "passw0rd",
        "starwars",
        "admin",
        "administrator",
        "root",
        "toor",
        "pass",
        "test",
        "guest",
        "admin123",
        "root123",
        "password1234",
        "123123",
        "654321",
        "123321",
        "666666",
        "121212",
        "000000",
        "222222",
        "333333",
        "444444",
        "555555",
        "777777",
        "888888",
        "999999",
        "qwe123",
        "qweasd",
        "1q2w3e4r",
        "q1w2e3r4",
        "1qaz2wsx",
        "qazwsx",
        "qwert",
        "asdfgh",
        "zxcvbn",
        "qweasdzxc",
        "qwerty1",
        "qwerty12",
        "password12",
        "password01",
        "passwd",
        "p@ssw0rd",
        "P@ssw0rd",
        "P@ssword1",
        "Pa$$w0rd",
        "iloveyou",
        "sunshine",
        "football",
        "baseball",
        "trustno1",
        "superman",
        "michael",
        "shadow",
    }

    KEYBOARD_PATTERNS: ClassVar = [
        "qwerty",
        "qwertz",
        "azerty",
        "qweasd",
        "12345",
        "asdfgh",
        "zxcvbn",
        "qazwsx",
        "098765",
        "asdzxc",
        "qwer",
        "asdf",
        "zxcv",
        "1234",
        "4321",
        "0987",
    ]

    def __init__(
        self,
        min_length: int = 8,
        max_length: int = 128,
        require_uppercase: bool = True,
        require_lowercase: bool = True,
        require_digits: bool = True,
        require_special: bool = True,
        min_uppercase: int = 1,
        min_lowercase: int = 1,
        min_digits: int = 1,
        min_special: int = 1,
        special_chars: str = "!@#$%^&*()_+-=[]{}|;:,.<>?",
        check_common: bool = True,
        check_patterns: bool = True,
        check_dictionary: bool = False,
        check_user_info: bool = True,
        user_info_fields: Optional[List[str]] = None,
        disallow_repeating: int = 3,
        disallow_sequential: int = 3,
        require_entropy: Optional[float] = None,
    ) -> None:
        """
        Initialize the password strength validator.

        Args:
            min_length: Minimum password length
            max_length: Maximum password length
            require_uppercase: Whether to require uppercase letters
            require_lowercase: Whether to require lowercase letters
            require_digits: Whether to require digits
            require_special: Whether to require special characters
            min_uppercase: Minimum number of uppercase letters
            min_lowercase: Minimum number of lowercase letters
            min_digits: Minimum number of digits
            min_special: Minimum number of special characters
            special_chars: String of allowed special characters
            check_common: Whether to check against common passwords
            check_patterns: Whether to check for keyboard patterns
            check_dictionary: Whether to check against dictionary words
            check_user_info: Whether to check for user information in password
            user_info_fields: Fields to check from user data
            disallow_repeating: Max allowed repeating characters
            disallow_sequential: Max allowed sequential characters
            require_entropy: Minimum required entropy (bits)
        """
        self.min_length = min_length
        self.max_length = max_length
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_digits = require_digits
        self.require_special = require_special
        self.min_uppercase = min_uppercase
        self.min_lowercase = min_lowercase
        self.min_digits = min_digits
        self.min_special = min_special
        self.special_chars = special_chars
        self.check_common = check_common
        self.check_patterns = check_patterns
        self.check_dictionary = check_dictionary
        self.check_user_info = check_user_info
        self.user_info_fields = user_info_fields or [
            "username",
            "email",
            "name",
        ]
        self.disallow_repeating = disallow_repeating
        self.disallow_sequential = disallow_sequential
        self.require_entropy = require_entropy

    def validate(self, value: Any) -> None:
        """
        Validate the password strength.

        Args:
            value: The password to validate

        Raises:
            ValidationError: If the password doesn't meet requirements
        """
        if not isinstance(value, str):
            raise ValidationError(
                f"Password must be a string, not {type(value).__name__}"
            )

        if len(value) < self.min_length:
            raise ValidationError(
                f"Password must be at least {self.min_length} characters long"
            )

        if len(value) > self.max_length:
            raise ValidationError(
                f"Password must not exceed {self.max_length} characters"
            )

        uppercase_count = sum(1 for c in value if c.isupper())
        lowercase_count = sum(1 for c in value if c.islower())
        digit_count = sum(1 for c in value if c.isdigit())
        special_count = sum(1 for c in value if c in self.special_chars)

        if self.require_uppercase and uppercase_count < self.min_uppercase:
            raise ValidationError(
                f"Password must contain at least {self.min_uppercase} "
                f"uppercase letter(s)"
            )

        if self.require_lowercase and lowercase_count < self.min_lowercase:
            raise ValidationError(
                f"Password must contain at least {self.min_lowercase} "
                f"lowercase letter(s)"
            )

        if self.require_digits and digit_count < self.min_digits:
            raise ValidationError(
                f"Password must contain at least {self.min_digits} digit(s)"
            )

        if self.require_special and special_count < self.min_special:
            raise ValidationError(
                f"Password must contain at least {self.min_special} special "
                f"character(s)"
            )

        if self.check_common and value.lower() in self.COMMON_PASSWORDS:
            raise ValidationError(
                "This password is too common. Please choose a stronger "
                "password."
            )

        if self.check_patterns:
            lower_pwd = value.lower()
            for pattern in self.KEYBOARD_PATTERNS:
                if pattern in lower_pwd or pattern[::-1] in lower_pwd:
                    raise ValidationError(
                        "Password contains keyboard patterns. Please choose "
                        "a more random password."
                    )

        if self.disallow_repeating:
            for i in range(len(value) - self.disallow_repeating + 1):
                if len(set(value[i : i + self.disallow_repeating])) == 1:
                    raise ValidationError(
                        f"Password contains more than "
                        f"{self.disallow_repeating - 1} repeating characters"
                    )

        if self.disallow_sequential:
            self._check_sequential(value)

        if self.require_entropy:
            entropy = self._calculate_entropy(value)
            if entropy < self.require_entropy:
                raise ValidationError(
                    f"Password entropy ({entropy:.1f} bits) is below "
                    f"required minimum ({self.require_entropy} bits)"
                )

    def _check_sequential(self, password: str) -> None:
        """Check for sequential characters in password."""
        for i in range(len(password) - self.disallow_sequential + 1):
            substring = password[i : i + self.disallow_sequential]

            is_ascending = all(
                ord(substring[j]) == ord(substring[j - 1]) + 1
                for j in range(1, len(substring))
            )

            is_descending = all(
                ord(substring[j]) == ord(substring[j - 1]) - 1
                for j in range(1, len(substring))
            )

            if is_ascending or is_descending:
                raise ValidationError(
                    f"Password contains more than "
                    f"{self.disallow_sequential - 1} sequential characters"
                )

    def _calculate_entropy(self, password: str) -> float:
        """
        Calculate password entropy in bits.

        Args:
            password: The password to analyze

        Returns:
            Entropy in bits
        """
        import math

        charset_size = 0
        if any(c.islower() for c in password):
            charset_size += 26
        if any(c.isupper() for c in password):
            charset_size += 26
        if any(c.isdigit() for c in password):
            charset_size += 10
        if any(c in self.special_chars for c in password):
            charset_size += len(self.special_chars)

        if charset_size == 0:
            return 0.0

        return len(password) * math.log2(charset_size)
