Error Handling
==============

This guide covers comprehensive error handling patterns, custom error messages, and debugging techniques for flask-inputfilter.

Understanding Error Structure
-----------------------------

Flask-inputfilter returns errors in a structured JSON format when validation fails:

Basic Error Format
~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
        "field_name": "Error message for this specific field",
        "another_field": "Another error message",
        "_condition": "Error message for condition validation"
    }

Detailed Error Example
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
        "email": "This field is required.",
        "age": "Value must be between 18 and 99.",
        "password": "Password must contain at least one uppercase letter.",
        "_condition": "Exactly one of the following fields must be present: phone, email"
    }

Custom Error Messages
---------------------

Field-Level Custom Messages
~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can customize error messages for individual validators:

.. code-block:: python

    class UserRegistrationFilter(InputFilter):
        username: str = field(
            required=True,
            validators=[
                LengthValidator(
                    min_length=3,
                    max_length=20,
                    error_message="Username must be between 3 and 20 characters long"
                ),
                RegexValidator(
                    pattern=r'^[a-zA-Z0-9_]+$',
                    error_message="Username can only contain letters, numbers, and underscores"
                )
            ]
        )

        email: str = field(
            required=True,
            validators=[
                IsEmailValidator(error_message="Please provide a valid email address")
            ]
        )

        password: str = field(
            required=True,
            validators=[
                LengthValidator(
                    min_length=8,
                    error_message="Password must be at least 8 characters long"
                ),
                RegexValidator(
                    pattern=r'(?=.*[A-Z])',
                    error_message="Password must contain at least one uppercase letter"
                ),
                RegexValidator(
                    pattern=r'(?=.*[0-9])',
                    error_message="Password must contain at least one number"
                )
            ]
        )

Condition Custom Messages
~~~~~~~~~~~~~~~~~~~~~~~~~

Customize error messages for conditions:

.. code-block:: python

    class ContactFilter(InputFilter):
        email: str = field(required=False)
        phone: str = field(required=False)
        address: str = field(required=False)

        _conditions = [
            ExactlyOneOfCondition(
                fields=['email', 'phone', 'address'],
                error_message="Please provide either an email, phone number, or address"
            )
        ]

Internationalization (i18n)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

For multi-language applications, you can use translation functions:

.. code-block:: python

    from flask_babel import gettext as _

    class LocalizedFilter(InputFilter):
        name: str = field(
            required=True,
            validators=[
                LengthValidator(
                    min_length=2,
                    error_message=lambda: _("Name must be at least 2 characters long")
                )
            ]
        )

        email: str = field(
            required=True,
            validators=[
                IsEmailValidator(
                    error_message=lambda: _("Please provide a valid email address")
                )
            ]
        )

Error Handling Patterns
-----------------------

Decorator Pattern (Automatic)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When using the `@validate()` decorator, errors are automatically returned as HTTP 400 responses:

.. code-block:: python

    @app.route('/register', methods=['POST'])
    @UserRegistrationFilter.validate()
    def register():
        # This code only runs if validation passes
        data = g.validated_data
        # Process valid data...
        return jsonify({"success": True})

    # If validation fails, automatic response:
    # HTTP 400 with JSON error structure

Manual Pattern (Controlled)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For more control over error handling:

.. code-block:: python

    @app.route('/register', methods=['POST'])
    def register():
        input_filter = UserRegistrationFilter()
        input_filter.set_data(request.get_json())

        if input_filter.is_valid():
            validated_data = input_filter.get_data()
            # Process valid data...
            return jsonify({"success": True, "data": validated_data})
        else:
            errors = input_filter.get_errors()

            # Custom error handling logic
            if 'email' in errors:
                # Log email validation failures
                app.logger.warning(f"Email validation failed: {errors['email']}")

            # Custom response format
            return jsonify({
                "success": False,
                "message": "Validation failed",
                "errors": errors,
                "error_count": len(errors)
            }), 400

Advanced Error Handling
-----------------------

Partial Validation
~~~~~~~~~~~~~~~~~~

Sometimes you want to collect all possible errors, even from optional fields:

.. code-block:: python

    class FlexibleValidationFilter(InputFilter):
        def validate_partial(self, data):
            """Validate all fields that are present, ignoring required constraints"""
            self.set_data(data)
            errors = {}

            for field_name, field_config in self._get_fields().items():
                if field_name in data:
                    try:
                        self._validate_field(field_name, data[field_name])
                    except ValidationError as e:
                        errors[field_name] = str(e)

            return len(errors) == 0, errors

    # Usage
    input_filter = FlexibleValidationFilter()
    is_valid, errors = input_filter.validate_partial(request.get_json())

Error Aggregation
~~~~~~~~~~~~~~~~~

Collect and categorize multiple errors:

.. code-block:: python

    def categorize_errors(errors):
        """Categorize errors by type for better UX"""
        categorized = {
            "required_fields": [],
            "format_errors": [],
            "business_rules": [],
            "external_api": []
        }

        for field, message in errors.items():
            if field == "_condition":
                categorized["business_rules"].append({
                    "field": field,
                    "message": message
                })
            elif "required" in message.lower():
                categorized["required_fields"].append({
                    "field": field,
                    "message": message
                })
            elif "format" in message.lower() or "invalid" in message.lower():
                categorized["format_errors"].append({
                    "field": field,
                    "message": message
                })
            else:
                categorized["external_api"].append({
                    "field": field,
                    "message": message
                })

        return categorized

    @app.route('/register', methods=['POST'])
    def register_with_categorized_errors():
        input_filter = UserRegistrationFilter()
        input_filter.set_data(request.get_json())

        if not input_filter.is_valid():
            raw_errors = input_filter.get_errors()
            categorized_errors = categorize_errors(raw_errors)

            return jsonify({
                "success": False,
                "errors": categorized_errors,
                "summary": f"Found {len(raw_errors)} validation errors"
            }), 400

Debugging Techniques
--------------------

Verbose Error Logging
~~~~~~~~~~~~~~~~~~~~~

Enable detailed logging for debugging validation issues:

.. code-block:: python

    import logging
    from flask_inputfilter.exceptions import ValidationError

    class DebuggableFilter(InputFilter):
        def __init__(self, debug=False):
            super().__init__()
            self.debug = debug
            if debug:
                logging.basicConfig(level=logging.DEBUG)
                self.logger = logging.getLogger(__name__)

        def _validate_field(self, field_name, value):
            if self.debug:
                self.logger.debug(f"Validating field '{field_name}' with value: {value}")

            try:
                result = super()._validate_field(field_name, value)
                if self.debug:
                    self.logger.debug(f"Field '{field_name}' validation passed")
                return result
            except ValidationError as e:
                if self.debug:
                    self.logger.debug(f"Field '{field_name}' validation failed: {e}")
                raise

Validation Step Tracing
~~~~~~~~~~~~~~~~~~~~~~~

Trace each step of the validation process:

.. code-block:: python

    def trace_validation_steps(input_filter, data):
        """Debug helper to trace validation steps"""
        print(f"Input data: {data}")

        input_filter.set_data(data)

        # Check each field
        for field_name in input_filter._get_fields():
            field_value = data.get(field_name)
            print(f"\\nProcessing field '{field_name}': {field_value}")

            # Apply filters
            try:
                filtered_value = input_filter._apply_filters(field_name, field_value)
                print(f"  After filters: {filtered_value}")
            except Exception as e:
                print(f"  Filter error: {e}")

            # Apply validators
            try:
                input_filter._validate_field(field_name, filtered_value)
                print(f"  Validation: PASSED")
            except ValidationError as e:
                print(f"  Validation: FAILED - {e}")

        # Check conditions
        try:
            input_filter._validate_conditions()
            print(f"\\nConditions: PASSED")
        except ValidationError as e:
            print(f"\\nConditions: FAILED - {e}")

    # Usage
    trace_validation_steps(MyFilter(), request.get_json())

Error Recovery Strategies
------------------------

Graceful Degradation
~~~~~~~~~~~~~~~~~~~~

Continue processing with partial data when non-critical validations fail:

.. code-block:: python

    class ResilientFilter(InputFilter):
        def __init__(self):
            super().__init__()
            self.critical_fields = ['email', 'user_id']
            self.optional_fields = ['profile_image', 'bio', 'preferences']

        def validate_with_recovery(self, data):
            """Validate critical fields strictly, optional fields with recovery"""
            errors = {}
            validated_data = {}

            # Strict validation for critical fields
            for field in self.critical_fields:
                try:
                    validated_data[field] = self._validate_field(field, data.get(field))
                except ValidationError as e:
                    errors[field] = str(e)

            # Graceful validation for optional fields
            for field in self.optional_fields:
                try:
                    if field in data:
                        validated_data[field] = self._validate_field(field, data[field])
                except ValidationError as e:
                    # Log the error but don't fail the request
                    app.logger.warning(f"Optional field '{field}' validation failed: {e}")
                    # Use default or skip the field
                    validated_data[field] = self._get_default_value(field)

            # Fail only if critical fields have errors
            if any(field in errors for field in self.critical_fields):
                return False, errors, None

            return True, {}, validated_data

Custom Exception Types
----------------------

Create specific exception types for different error scenarios:

.. code-block:: python

    class BusinessRuleError(ValidationError):
        """Raised when business logic validation fails"""
        pass

    class ExternalApiError(ValidationError):
        """Raised when external API validation fails"""
        pass

    class SecurityValidationError(ValidationError):
        """Raised when security validation fails"""
        pass

    class CustomSecurityFilter(InputFilter):
        def _validate_security_constraints(self, data):
            # Check for suspicious patterns
            if self._detect_sql_injection(data):
                raise SecurityValidationError("Potential security threat detected")

            # Check rate limiting
            if self._check_rate_limit(data.get('user_id')):
                raise SecurityValidationError("Rate limit exceeded")

        def validate(self):
            try:
                return super().validate()
            except SecurityValidationError as e:
                # Log security issues
                app.logger.error(f"Security validation failed: {e}")
                # Return generic error message
                return False, {"error": "Validation failed"}

Testing Error Scenarios
-----------------------

Unit Testing Error Cases
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import pytest
    from flask_inputfilter.exceptions import ValidationError

    class TestUserValidation:
        def test_missing_required_fields(self):
            filter_instance = UserRegistrationFilter()
            filter_instance.set_data({})

            assert not filter_instance.is_valid()
            errors = filter_instance.get_errors()
            assert 'email' in errors
            assert 'username' in errors

        def test_invalid_email_format(self):
            filter_instance = UserRegistrationFilter()
            filter_instance.set_data({
                'username': 'testuser',
                'email': 'invalid-email'
            })

            assert not filter_instance.is_valid()
            errors = filter_instance.get_errors()
            assert 'email' in errors
            assert 'valid email' in errors['email'].lower()

        def test_custom_error_messages(self):
            filter_instance = UserRegistrationFilter()
            filter_instance.set_data({
                'username': 'ab',  # Too short
                'email': 'test@example.com'
            })

            assert not filter_instance.is_valid()
            errors = filter_instance.get_errors()
            assert 'between 3 and 20 characters' in errors['username']

Integration Testing
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def test_error_response_format(client):
        """Test that error responses follow expected format"""
        response = client.post('/register', json={
            'email': 'invalid-email',
            'username': 'ab'
        })

        assert response.status_code == 400
        data = response.get_json()

        assert 'email' in data
        assert 'username' in data
        assert isinstance(data, dict)

Best Practices
--------------

1. **Consistent Error Format**: Always use the same error structure across your API
2. **User-Friendly Messages**: Write error messages that users can understand and act upon
3. **Security Considerations**: Don't expose sensitive information in error messages
4. **Logging**: Log validation errors for debugging and monitoring
5. **Error Recovery**: Implement graceful degradation where appropriate
6. **Testing**: Thoroughly test error scenarios
7. **Documentation**: Document expected error responses for API consumers

Error Message Guidelines
~~~~~~~~~~~~~~~~~~~~~~~

**Good Error Messages:**
- "Email address is required"
- "Password must be at least 8 characters long"
- "Please provide either a phone number or email address"

**Poor Error Messages:**
- "Invalid input"
- "Error in field X"
- "Validation failed"

**Security-Safe Messages:**
- Instead of: "User with email john@example.com not found"
- Use: "Invalid login credentials"