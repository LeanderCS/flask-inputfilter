Global Decorators
=================

Overview
--------

Global decorators apply filters, validators, and conditions to all fields in an InputFilter
or establish cross-field validation rules. They provide a convenient way to implement
common processing logic without repeating configuration for each field.

The global decorators are:

- ``global_filter()`` - Apply filters to all fields
- ``global_validator()`` - Apply validators to all fields
- ``condition()`` - Add cross-field validation conditions
- ``model()`` - Associate with a model class for serialization

All global decorators support multiple element registration for concise definitions.

global_filter()
---------------

Applies filters to all fields in the InputFilter before individual field filters are processed.

.. autofunction:: flask_inputfilter.declarative.global_filter.global_filter

Basic Usage
~~~~~~~~~~~

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.declarative import field, global_filter
    from flask_inputfilter.filters import StringTrimFilter, ToLowerFilter

    class TrimmedInputFilter(InputFilter):
        name = field(required=True)
        email = field(required=True)
        description = field(required=False)

        # Apply to all fields
        global_filter(StringTrimFilter())

Multiple Global Filters
~~~~~~~~~~~~~~~~~~~~~~~~

Register multiple filters in a single call:

.. code-block:: python

    class ProcessedInputFilter(InputFilter):
        username = field(required=True)
        email = field(required=True)
        bio = field(required=False)

        # Multiple filters applied to all fields
        global_filter(StringTrimFilter(), ToLowerFilter(), RemoveExtraSpacesFilter())

**Processing Order**: Global filters are applied first, then individual field filters.

.. code-block:: python

    class OrderDemoFilter(InputFilter):
        name = field(
            required=True,
            filters=[ToUpperFilter()]  # Applied after global filters
        )

        # Applied first to all fields
        global_filter(StringTrimFilter())

    # Input: "  john  " → StringTrimFilter() → "john" → ToUpperFilter() → "JOHN"

Inheritance
~~~~~~~~~~~

Global filters are inherited and preserved across class hierarchies:

.. code-block:: python

    class BaseFilter(InputFilter):
        global_filter(StringTrimFilter())

    class ExtendedFilter(BaseFilter):
        name = field(required=True)

        # Additional global filter (StringTrimFilter is preserved)
        global_filter(ToLowerFilter())

    # ExtendedFilter has both StringTrimFilter and ToLowerFilter

global_validator()
------------------

Applies validators to all fields in the InputFilter after filters have been processed.

.. autofunction:: flask_inputfilter.declarative.global_validator.global_validator

Basic Usage
~~~~~~~~~~~

.. code-block:: python

    from flask_inputfilter.validators import IsStringValidator, NotEmptyValidator

    class ValidatedInputFilter(InputFilter):
        name = field(required=True)
        email = field(required=True)
        description = field(required=False)

        # All fields must be strings and not empty
        global_validator(IsStringValidator())

Multiple Global Validators
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class StrictInputFilter(InputFilter):
        username = field(required=True)
        email = field(required=True)
        password = field(required=True)

        # Multiple validators applied to all fields
        global_validator(
            IsStringValidator(),
            NotEmptyValidator(),
            LengthValidator(min_length=1, max_length=255)
        )

Inheritance and Override
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class BaseValidatedFilter(InputFilter):
        global_validator(IsStringValidator())

    class StrictFilter(BaseValidatedFilter):
        name = field(required=True)

        # Additional validators (IsStringValidator is preserved)
        global_validator(LengthValidator(min_length=2))

Practical Examples
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Ensure all text fields are valid strings
    class TextOnlyFilter(InputFilter):
        global_validator(IsStringValidator(), NotEmptyValidator())

    # Length constraints for all fields
    class BoundedFilter(InputFilter):
        global_validator(LengthValidator(max_length=1000))

    # Security validation
    class SecureInputFilter(InputFilter):
        global_validator(
            NoScriptTagValidator(),
            NoSqlInjectionValidator(),
            NoXssValidator()
        )

condition()
-----------

Adds cross-field validation conditions that validate relationships between multiple fields.

.. autofunction:: flask_inputfilter.declarative.condition.condition

Basic Usage
~~~~~~~~~~~

.. code-block:: python

    from flask_inputfilter.conditions import EqualCondition

    class RegistrationFilter(InputFilter):
        password = field(required=True)
        password_confirmation = field(required=True)

        # Password confirmation validation
        condition(EqualCondition('password', 'password_confirmation'))

Multiple Conditions
~~~~~~~~~~~~~~~~~~~

Register multiple conditions in a single call:

.. code-block:: python

    from flask_inputfilter.conditions import (
        EqualCondition, AtLeastOneOfCondition, ExactlyOneOfCondition
    )

    class ComplexValidationFilter(InputFilter):
        password = field(required=True)
        password_confirmation = field(required=True)
        email = field(required=False)
        phone = field(required=False)
        address = field(required=False)

        # Multiple cross-field validations
        condition(
            EqualCondition('password', 'password_confirmation'),
            AtLeastOneOfCondition(['email', 'phone']),  # Need at least one contact method
            ExactlyOneOfCondition(['email', 'phone', 'address'])  # But only one primary contact
        )

model()
-------

Associates the InputFilter with a model class for automatic serialization.

.. autofunction:: flask_inputfilter.declarative.model.model

Basic Usage
~~~~~~~~~~~

.. code-block:: python

    from dataclasses import dataclass
    from flask_inputfilter.declarative import model

    @dataclass
    class User:
        username: str
        email: str

    class UserFilter(InputFilter):
        username = field(required=True, validators=[IsStringValidator()])
        email = field(required=True, validators=[EmailValidator()])

        model(User)

    # Usage
    filter_instance = UserFilter()
    user = filter_instance.validate_data({'username': 'john', 'email': 'john@example.com'})
    # user is a User dataclass instance

Supported Model Types
~~~~~~~~~~~~~~~~~~~~~

**Dataclasses**:

.. code-block:: python

    from dataclasses import dataclass

    @dataclass
    class Product:
        name: str
        price: float
        in_stock: bool = True

    class ProductFilter(InputFilter):
        name = field(required=True, validators=[IsStringValidator()])
        price = field(required=True, filters=[ToFloatFilter()])
        in_stock = field(required=False, filters=[ToBooleanFilter()], default=True)

        model(Product)

**Pydantic Models**:

.. code-block:: python

    from pydantic import BaseModel

    class User(BaseModel):
        username: str
        email: str
        age: int = None

    class UserFilter(InputFilter):
        username = field(required=True, validators=[IsStringValidator()])
        email = field(required=True, validators=[EmailValidator()])
        age = field(required=False, filters=[ToIntegerFilter()])

        model(User)

**TypedDict**:

.. code-block:: python

    from typing import TypedDict

    class UserDict(TypedDict):
        username: str
        email: str

    class UserFilter(InputFilter):
        username = field(required=True, validators=[IsStringValidator()])
        email = field(required=True, validators=[EmailValidator()])

        model(UserDict)

Field Filtering
~~~~~~~~~~~~~~~

The model decorator automatically filters out fields that don't exist in the model:

.. code-block:: python

    @dataclass
    class SimpleUser:
        name: str  # Only has name field

    class ExtendedUserFilter(InputFilter):
        name = field(required=True, validators=[IsStringValidator()])
        email = field(required=True, validators=[EmailValidator()])  # Extra field
        age = field(required=False, filters=[ToIntegerFilter()])     # Extra field

        model(SimpleUser)

    # Only 'name' will be passed to SimpleUser constructor
    # 'email' and 'age' are filtered out automatically

Inheritance and Advanced Usage
------------------------------

Combining Global Decorators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class FullFeaturedFilter(InputFilter):
        username = field(required=True)
        email = field(required=True)
        password = field(required=True)
        password_confirmation = field(required=True)
        phone = field(required=False)

        # Global processing
        global_filter(StringTrimFilter(), ToLowerFilter())
        global_validator(IsStringValidator(), NotEmptyValidator())

        # Cross-field validation
        condition(
            EqualCondition('password', 'password_confirmation'),
            AtLeastOneOfCondition(['email', 'phone'])
        )

        # Model association
        model(User)

Hierarchical Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class BaseUserFilter(InputFilter):
        # Base global configuration
        global_filter(StringTrimFilter())
        global_validator(IsStringValidator())

    class StandardUserFilter(BaseUserFilter):
        username = field(required=True)
        email = field(required=True)

        # Additional processing
        global_validator(NotEmptyValidator())

    class AdminUserFilter(StandardUserFilter):
        role = field(required=True, default="admin")
        permissions = field(required=False, default=[])

        # Admin-specific validation
        global_validator(SecurityValidator())
        condition(AdminPermissionCondition())
        # errors will contain both field-level and condition-level errors
