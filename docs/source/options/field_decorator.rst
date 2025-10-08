Field Decorator
===============

Overview
--------

The ``field()`` decorator is the core component for defining individual input fields in the
Declarative API. It provides comprehensive configuration options for field validation,
filtering, and processing.

.. autofunction:: flask_inputfilter.declarative.field.field

Basic Usage
-----------

The simplest field definition:

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.declarative import field

    class SimpleFilter(InputFilter):
        name = field()  # Optional field with no validation

Required Fields
~~~~~~~~~~~~~~~

.. code-block:: python

    class UserFilter(InputFilter):
        username = field(required=True)
        email = field(required=True)

Field Configuration Options
---------------------------

The ``field()`` decorator accepts the following parameters:

required
~~~~~~~~

**Type**: ``bool``
**Default**: ``False``

Specifies whether the field must be present in the input data.

.. code-block:: python

    class RegistrationFilter(InputFilter):
        username = field(required=True)    # Must be provided
        nickname = field(required=False)   # Optional

**Examples**:

.. code-block:: python

    # Required field - will raise ValidationError if missing
    email = field(required=True)

    # Optional field - won't raise error if missing
    phone = field(required=False)

default
~~~~~~~

**Type**: ``Any``
**Default**: ``None``

Provides a default value when the field is not present in the input data.
Only applies to optional fields (``required=False``).

.. code-block:: python

    class UserFilter(InputFilter):
        name = field(required=True)
        role = field(required=False, default="user")
        active = field(required=False, default=True)
        tags = field(required=False, default=[])

**Important**: Use ``default=[]`` carefully with mutable objects. Consider using a factory function:

.. code-block:: python

    from flask_inputfilter.filters import DefaultValueFilter

    class SafeDefaultFilter(InputFilter):
        # Safe for mutable defaults
        tags = field(required=False, filters=[DefaultValueFilter(lambda: [])])

fallback
~~~~~~~~

**Type**: ``Any``
**Default**: ``None``

Specifies a value to use when validation fails or when processing encounters errors.
Unlike ``default``, ``fallback`` applies even when the field is present but invalid.

.. code-block:: python

    from flask_inputfilter.validators import IsIntegerValidator

    class RobustFilter(InputFilter):
        age = field(
            required=False,
            validators=[IsIntegerValidator()],
            fallback=0  # Use 0 if validation fails
        )

        priority = field(
            required=True,
            validators=[IsIntegerValidator()],
            fallback=1  # Use 1 if provided value is invalid
        )

filters
~~~~~~~

**Type**: ``list[BaseFilter]``
**Default**: ``[]``

List of filters to apply to the field value. Filters are applied in the order specified
and transform the input data before validation.

.. code-block:: python

    from flask_inputfilter.filters import StringTrimFilter, ToLowerFilter, ToIntegerFilter

    class FilteredInputFilter(InputFilter):
        username = field(
            required=True,
            filters=[StringTrimFilter(), ToLowerFilter()]
        )

        age = field(
            required=False,
            filters=[ToIntegerFilter()]
        )

**Common Filters**:

.. code-block:: python

    from flask_inputfilter.filters import (
        StringTrimFilter,      # Remove leading/trailing whitespace
        ToLowerFilter,         # Convert to lowercase
        ToUpperFilter,         # Convert to uppercase
        ToIntegerFilter,       # Convert to integer
        ToFloatFilter,         # Convert to float
        ToBooleanFilter,       # Convert to boolean
        ToNullFilter,          # Convert empty strings to None
        RemoveFilter,          # Remove specific characters
        ReplaceFilter,         # Replace characters/patterns
    )

    class ComprehensiveFilter(InputFilter):
        email = field(filters=[StringTrimFilter(), ToLowerFilter()])
        price = field(filters=[ToFloatFilter()])
        active = field(filters=[ToBooleanFilter()])

validators
~~~~~~~~~~

**Type**: ``list[BaseValidator]``
**Default**: ``[]``

List of validators to apply to the field value. Validators check the processed value
and raise validation errors if the value doesn't meet the criteria.

.. code-block:: python

    from flask_inputfilter.validators import (
        IsStringValidator, LengthValidator, EmailValidator, RegexValidator
    )

    class ValidatedFilter(InputFilter):
        username = field(
            required=True,
            validators=[
                IsStringValidator(),
                LengthValidator(min_length=3, max_length=20)
            ]
        )

        email = field(
            required=True,
            validators=[IsStringValidator(), EmailValidator()]
        )

**Common Validators**:

.. code-block:: python

    from flask_inputfilter.validators import (
        IsStringValidator,     # Must be a string
        IsIntegerValidator,    # Must be an integer
        IsFloatValidator,      # Must be a float
        IsBooleanValidator,    # Must be a boolean
        IsListValidator,       # Must be a list
        IsDictValidator,       # Must be a dictionary
        LengthValidator,       # String/list length validation
        RangeValidator,        # Numeric range validation
        EmailValidator,        # Email format validation
        UrlValidator,          # URL format validation
        RegexValidator,        # Custom regex validation
        InValidator,           # Value must be in allowed list
        NotInValidator,        # Value must not be in forbidden list
    )

**Validator Examples**:

.. code-block:: python

    class DetailedValidationFilter(InputFilter):
        # String validation with length constraints
        password = field(
            required=True,
            validators=[
                IsStringValidator(),
                LengthValidator(min_length=8, max_length=128)
            ]
        )

        # Numeric validation with range
        age = field(
            required=True,
            validators=[
                IsIntegerValidator(),
                RangeValidator(min_value=13, max_value=120)
            ]
        )

        # Choice validation
        status = field(
            required=True,
            validators=[
                IsStringValidator(),
                InValidator(['active', 'inactive', 'pending'])
            ]
        )

        # Custom regex validation
        phone = field(
            required=False,
            validators=[
                IsStringValidator(),
                RegexValidator(r'^\+?1?\d{9,15}$', message="Invalid phone number format")
            ]
        )

steps
~~~~~

**Type**: ``list``
**Default**: ``[]``

Defines a sequence of processing steps (filters and validators) that are applied in order.
This allows for fine-grained control over the processing pipeline.

.. code-block:: python

    from flask_inputfilter.filters import StringTrimFilter, ToIntegerFilter
    from flask_inputfilter.validators import IsStringValidator, IsIntegerValidator

    class SteppedFilter(InputFilter):
        numeric_input = field(
            required=True,
            steps=[
                StringTrimFilter(),          # Step 1: Remove whitespace
                IsStringValidator(),         # Step 2: Validate it's a string
                ToIntegerFilter(),           # Step 3: Convert to integer
                IsIntegerValidator(),        # Step 4: Validate it's an integer
                RangeValidator(min_value=0)  # Step 5: Validate range
            ]
        )

external_api
~~~~~~~~~~~~

**Type**: ``ExternalApiConfig``
**Default**: ``None``

Configuration for fetching field values from external APIs. Useful for data enrichment
or validation against external services.

.. code-block:: python

    from flask_inputfilter.models import ExternalApiConfig

    class ExternalDataFilter(InputFilter):
        user_id = field(required=True, validators=[IsIntegerValidator()])

        # Fetch user details from external API
        user_profile = field(
            required=False,
            external_api=ExternalApiConfig(
                url="https://api.example.com/users/{user_id}",
                method="GET",
                headers={"Authorization": "Bearer token"}
            )
        )

For detailed information, see :doc:`ExternalApi <external_api>`.

copy
~~~~

**Type**: ``str``
**Default**: ``None``

Copy the value from another field. The copied value can then be filtered and validated
independently.

.. code-block:: python

    class CopyFieldFilter(InputFilter):
        email = field(required=True, validators=[EmailValidator()])

        # Copy email value for confirmation
        email_confirmation = field(
            required=True,
            copy="email",
            validators=[EmailValidator()]
        )

        # Processing happens after copying
        normalized_email = field(
            required=False,
            copy="email",
            filters=[StringTrimFilter(), ToLowerFilter()]
        )

For detailed information, see :doc:`Copy <copy>`.

computed
~~~~~~~~

**Type**: ``Callable[[dict[str, Any]], Any]``
**Default**: ``None``

Define a read-only field that is automatically calculated from other fields.
The provided callable receives the current data dictionary and should return the
computed value.

Computed fields are:

- **Read-only**: Input values are ignored
- **Non-blocking**: Errors let the field stay on ``None`` and log a warning
- Evaluated **during validation**: Have access to all previously processed fields

.. code-block:: python

    class OrderInputFilter(InputFilter):
        quantity: int = field(required=True)
        price: float = field(required=True)

        # Computed field using lambda
        total: float = field(
            computed=lambda data: data['quantity'] * data['price']
        )

.. code-block:: python

    # Using named function for complex calculations
    def calculate_tax(data):
        subtotal = data.get('subtotal', 0)
        tax_rate = data.get('tax_rate', 0.19)
        return subtotal * tax_rate

    class InvoiceInputFilter(InputFilter):
        subtotal: float = field(required=True)
        tax_rate: float = field(default=0.19)

        tax: float = field(computed=calculate_tax)
        total: float = field(
            required=True,
            computed=lambda data: data['subtotal'] + data.get('tax', 0)
        )

Advanced Field Patterns
-----------------------

Multi-Type Fields
~~~~~~~~~~~~~~~~~

Fields that can accept multiple types:

.. code-block:: python

    from flask_inputfilter.validators import OrValidator

    class FlexibleTypeFilter(InputFilter):
        # Can be either string or integer
        identifier = field(
            required=True,
            validators=[
                OrValidator([
                    IsStringValidator(),
                    IsIntegerValidator()
                ])
            ]
        )

Custom Field Processing
~~~~~~~~~~~~~~~~~~~~~~~

Create reusable field configurations:

.. code-block:: python

    # Define reusable field types
    def email_field(required=True):
        return field(
            required=required,
            filters=[StringTrimFilter(), ToLowerFilter()],
            validators=[IsStringValidator(), EmailValidator()]
        )

    def username_field(min_length=3, max_length=20):
        return field(
            required=True,
            filters=[StringTrimFilter()],
            validators=[
                IsStringValidator(),
                LengthValidator(min_length=min_length, max_length=max_length),
                RegexValidator(r'^[a-zA-Z0-9_]+$', message="Only letters, numbers, and underscores allowed")
            ]
        )

    class UserFilter(InputFilter):
        username = username_field()
        email = email_field()
        backup_email = email_field(required=False)
