InputFilter
===========

Overview
--------

The ``InputFilter`` class is the core component of flask-inputfilter that provides data validation,
filtering, and serialization capabilities for Flask applications. It supports two different approaches
for defining input filters.

.. autoclass:: flask_inputfilter.input_filter.InputFilter
   :members:
   :undoc-members:
   :show-inheritance:

Defining InputFilters
---------------------

The declarative API uses Python decorators to define fields, conditions, and global filters/validators
directly in the class definition.

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.declarative import field, condition, global_filter, global_validator
    from flask_inputfilter.filters import StringTrimFilter
    from flask_inputfilter.validators import IsStringValidator, LengthValidator
    from flask_inputfilter.conditions import EqualCondition

    class UserRegistrationFilter(InputFilter):
        # Field definitions
        username = field(
            required=True,
            filters=[StringTrimFilter()],
            validators=[IsStringValidator(), LengthValidator(min_length=3, max_length=20)]
        )

        email = field(
            required=True,
            validators=[IsStringValidator()]
        )

        password = field(required=True)
        password_confirmation = field(required=True)

        # Global filters applied to all fields
        global_filter(StringTrimFilter())

        # Global validators applied to all fields
        global_validator(IsStringValidator())

        # Conditions for cross-field validation
        condition(EqualCondition('password', 'password_confirmation'))

For detailed information about the declarative API, see:

- :doc:`Declarative API Overview <declarative_api>`
- :doc:`Field Decorator <field_decorator>`
- :doc:`Global Decorators <global_decorators>`

Usage
-----

Using the Validate Decorator
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The most common way to use InputFilter is as a decorator on Flask routes:

.. code-block:: python

    from flask import Flask, g

    app = Flask(__name__)

    @app.route('/register', methods=['POST'])
    @UserRegistrationFilter.validate()
    def register():
        # Access validated data
        data = g.validated_data

        username = data['username']
        email = data['email']

        # Your registration logic here
        return {'message': 'User registered successfully'}

Manual Validation
~~~~~~~~~~~~~~~~~

You can also validate data manually:

.. code-block:: python

    filter_instance = UserRegistrationFilter()

    filter_instance.set_data({
        'username': 'john_doe',
        'email': 'john@example.com',
        'password': 'secret123',
        'password_confirmation': 'secret123'
    })

    if not filter_instance.is_valid():
        print("Wrong credentials")
        return

    print(f"Welcome {filter_instance.get_value('username')}!")

Model Serialization
~~~~~~~~~~~~~~~~~~~

InputFilter can automatically serialize validated data to model instances:

.. code-block:: python

    from dataclasses import dataclass
    from flask_inputfilter.declarative import model

    @dataclass
    class User:
        username: str
        email: str

    class UserFilter(InputFilter):
        username = field(required=True, validators=[IsStringValidator()])
        email = field(required=True, validators=[IsStringValidator()])

        # Associate with model
        model(User)

    filter_instance = UserFilter()
    filter_instance.set_data({
        'username': 'john_doe',
        'email': 'john@example.com'
    })

    if filter_instance.is_valid():
        # Access validated data and create model instance
        user_instance = User(
            username=filter_instance.get_value('username'),
            email=filter_instance.get_value('email')
        )

        # user_instance is now a User object
        assert isinstance(user_instance, User)
        assert user_instance.username == 'john_doe'

Key Methods
-----------

validate()
~~~~~~~~~~

Class method that returns a decorator for Flask routes. Automatically validates request data
and stores the result in ``g.validated_data``.

.. code-block:: python

    @app.route('/api/users', methods=['POST'])
    @UserFilter.validate()
    def create_user():
        data = g.validated_data
        # Use validated data

set_data(data)
~~~~~~~~~~~~~~

Instance method that sets the input data to be validated.

.. code-block:: python

    filter_instance = UserFilter()
    filter_instance.set_data({'username': 'john'})

is_valid()
~~~~~~~~~~

Instance method that validates the current data and returns ``True`` if valid, ``False`` otherwise.

.. code-block:: python

    if filter_instance.is_valid():
        # Data is valid, proceed with processing
        username = filter_instance.get_value('username')

get_value(field_name)
~~~~~~~~~~~~~~~~~~~~~

Instance method that returns the validated value for a specific field.

.. code-block:: python

    username = filter_instance.get_value('username')
    email = filter_instance.get_value('email')

Error Handling
--------------

Flask-inputfilter provides error information when validation fails. You can access validation errors
through the filter instance:

.. code-block:: python

    filter_instance = UserFilter()
    filter_instance.set_data({'username': ''})  # Empty username

    if not filter_instance.is_valid():
        errors = filter_instance.get_errors()
        # errors = {'username': 'This field is required'}

When using the decorator, validation errors automatically return a 400 response with
the error details in JSON format.

Best Practices
--------------

1. **Organize Complex Filters**: Break down complex filters into base classes using inheritance
2. **Model Integration**: Use model serialization for type-safe data handling
3. **Global Components**: Use global filters/validators for common processing (e.g., trimming strings)

.. code-block:: python

    class BaseFilter(InputFilter):
        # Common global filters and validators
        global_filter(StringTrimFilter())
        global_validator(IsStringValidator())

    class UserFilter(BaseFilter):
        username = field(
            required=True,
            validators=[
                LengthValidator(
                    min_length=3,
                    max_length=20,
                    message="Username must be between 3 and 20 characters"
                )
            ]
        )
