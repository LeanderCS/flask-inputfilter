Declarative API
===============

Overview
--------

The Declarative API is the modern, recommended way to define InputFilters in flask-inputfilter.
It uses Python decorators and class-level declarations to create clean, readable, and maintainable
input validation definitions.

Key Features
------------

- **Clean Syntax**: Define fields, conditions, and global components directly in class definition
- **Type Safety**: Integrates well with type hints and IDEs
- **Inheritance Support**: Full support for class inheritance and MRO
- **Model Integration**: Automatic serialization to dataclasses, Pydantic models, and more
- **Multiple Element Support**: Register multiple components at once for concise definitions

Core Components
---------------

The Declarative API consists of four main decorators:

+----------------------+--------------------------------------------+
| Decorator            | Purpose                                    |
+======================+============================================+
| ``field()``          | Define individual input fields             |
+----------------------+--------------------------------------------+
| ``condition()``      | Add cross-field validation conditions     |
+----------------------+--------------------------------------------+
| ``global_filter()``  | Add filters applied to all fields         |
+----------------------+--------------------------------------------+
| ``global_validator()``| Add validators applied to all fields      |
+----------------------+--------------------------------------------+
| ``model()``          | Associate with a model class              |
+----------------------+--------------------------------------------+

Quick Example
-------------

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.declarative import field, condition, global_filter, global_validator, model
    from flask_inputfilter.filters import StringTrimFilter, ToLowerFilter
    from flask_inputfilter.validators import IsStringValidator, LengthValidator, EmailValidator
    from flask_inputfilter.conditions import EqualCondition
    from dataclasses import dataclass

    @dataclass
    class User:
        username: str
        email: str
        password: str

    class UserRegistrationFilter(InputFilter):
        # Field definitions with individual configuration
        username = field(
            required=True,
            validators=[LengthValidator(min_length=3, max_length=20)]
        )

        email = field(
            required=True,
            validators=[EmailValidator()]
        )

        password = field(required=True, validators=[LengthValidator(min_length=8)])
        password_confirmation = field(required=True)

        # Global components - applied to all fields
        global_filter(StringTrimFilter(), ToLowerFilter())
        global_validator(IsStringValidator())

        # Cross-field validation
        condition(EqualCondition('password', 'password_confirmation'))

        # Model association
        model(User)

 Declarative API
----------------

.. code-block:: python

    class MyFilter(InputFilter):
        name = field(required=True, validators=[IsStringValidator()])
        email = field(required=True, validators=[EmailValidator()])

        global_filter(StringTrimFilter())
        condition(RequiredCondition('name'))

Inheritance and MRO
-------------------

The Declarative API fully supports Python's inheritance and Method Resolution Order (MRO):

.. code-block:: python

    class BaseUserFilter(InputFilter):
        # Base fields
        name = field(required=True, validators=[IsStringValidator()])

        # Base global components
        global_filter(StringTrimFilter())

    class ExtendedUserFilter(BaseUserFilter):
        # Additional fields
        email = field(required=True, validators=[EmailValidator()])
        age = field(required=False, validators=[IsIntegerValidator()])

        # Additional global components (inherited ones are preserved)
        global_validator(LengthValidator(min_length=1))

        # Conditions
        condition(RequiredCondition('email'))

Field Override
~~~~~~~~~~~~~~

You can override fields from parent classes:

.. code-block:: python

    class BaseFilter(InputFilter):
        name = field(required=False)  # Optional in base

    class StrictFilter(BaseFilter):
        name = field(required=True, validators=[LengthValidator(min_length=2)])  # Override

Multiple Element Registration
-----------------------------

You can register multiple components at once for cleaner definitions:

.. code-block:: python

    class CompactFilter(InputFilter):
        name = field(required=True)
        email = field(required=True)

        # Multiple global filters
        global_filter(StringTrimFilter(), ToLowerFilter(), RemoveExtraSpacesFilter())

        # Multiple global validators
        global_validator(IsStringValidator(), NotEmptyValidator())

        # Multiple conditions
        condition(
            RequiredCondition('name'),
            RequiredCondition('email'),
            EqualCondition('password', 'password_confirmation')
        )

Model Integration
-----------------

The Declarative API seamlessly integrates with various model types:

Dataclasses
~~~~~~~~~~~

.. code-block:: python

    from dataclasses import dataclass

    @dataclass
    class User:
        name: str
        email: str

    class UserFilter(InputFilter):
        name = field(required=True, validators=[IsStringValidator()])
        email = field(required=True, validators=[EmailValidator()])

        model(User)

    # Usage
    filter_instance = UserFilter()
    user = filter_instance.validate_data({'name': 'John', 'email': 'john@example.com'})
    # user is a User dataclass instance

Pydantic Models
~~~~~~~~~~~~~~~

.. code-block:: python

    from pydantic import BaseModel

    class User(BaseModel):
        name: str
        email: str

    class UserFilter(InputFilter):
        name = field(required=True, validators=[IsStringValidator()])
        email = field(required=True, validators=[EmailValidator()])

        model(User)

TypedDict
~~~~~~~~~

.. code-block:: python

    from typing import TypedDict

    class UserDict(TypedDict):
        name: str
        email: str

    class UserFilter(InputFilter):
        name = field(required=True, validators=[IsStringValidator()])
        email = field(required=True, validators=[EmailValidator()])

        model(UserDict)

Next Steps
----------

For detailed information about each component, see:

- :doc:`Field Decorator <field_decorator>` - Complete field configuration options
- :doc:`Global Decorators <global_decorators>` - Global filters, validators, and conditions
- :doc:`Conditions <condition>` - Cross-field validation conditions
- :doc:`Filters <filter>` - Available filters and custom filter creation
- :doc:`Validators <validator>` - Available validators and custom validator creation
