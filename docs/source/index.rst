flask-inputfilter documentation
===============================

Overview
--------

Flask-InputFilter is a comprehensive input validation and filtering library for Flask applications. It provides a declarative way to define validation rules, data transformation filters, and business logic conditions for your API endpoints.

Key Features:
- **Declarative syntax**: Define validation rules using Python type hints and decorators
- **Comprehensive filtering**: Transform input data with built-in or custom filters
- **Rich validation**: Validate data with extensive built-in validators or create your own
- **Business conditions**: Enforce complex inter-field relationships and business rules
- **External API integration**: Fetch and validate data from external services
- **Model deserialization**: Convert validated data into custom model objects
- **Frontend integration**: Share validation logic between backend and frontend

..  toctree::
    :maxdepth: 1

    options/index
    guides/index
    changelog
    contributing
    development

Getting Started
---------------

Core Concepts
~~~~~~~~~~~~~

Before diving into code examples, let's understand the three main components:

**Filters**: Transform input data to a desired format (e.g., trim strings, convert to integers)
**Validators**: Ensure data meets specific criteria (e.g., is a valid email, within a range)
**Conditions**: Enforce relationships between multiple fields (e.g., exactly one field must be present)

Basic Workflow
~~~~~~~~~~~~~~

1. **Define**: Create an InputFilter class with field definitions
2. **Apply**: Use as a decorator or call validation methods directly
3. **Access**: Retrieve validated and filtered data from `g.validated_data`

Available functions:
--------------------

- :doc:`InputFilter <options/inputfilter>`
- :doc:`Conditions <options/condition>`
- :doc:`Filter <options/filter>`
- :doc:`Validator <options/validator>`
- :doc:`Creating your own Conditions, Filters and Validators <guides/create_own_components>`
- :doc:`ExternalApi <options/external_api>`

.. tip::

    Thank you for using `flask-inputfilter`!

    If you have any questions or suggestions, please feel free to open an issue on `GitHub <https://github.com/LeanderCS/flask-inputfilter>`_.
    If you don't want to miss any updates, please star the repository.
    This will help me to understand how many people are interested in this project.

.. note::

    If you like the project, please consider giving it a star on `GitHub <https://github.com/LeanderCS/flask-inputfilter>`_.

Installation
------------

.. code-block:: bash

    pip install flask-inputfilter

Quickstart
----------

To use the `InputFilter` class, create a new class that inherits from it and define the
fields you want to validate and filter.

There are numerous filters and validators available, but you can also create your :doc:`own <guides/create_own_components>`.

Step 1: Define Your InputFilter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.declarative import field
    from flask_inputfilter.conditions import ExactlyOneOfCondition
    from flask_inputfilter.enums import RegexEnum
    from flask_inputfilter.filters import StringTrimFilter, ToIntegerFilter, ToNullFilter
    from flask_inputfilter.validators import IsIntegerValidator, IsStringValidator, RegexValidator

    class UpdateZipcodeInputFilter(InputFilter):
        # Required integer field with filtering and validation
        id: int = field(
            required=True,
            filters=[ToIntegerFilter(), ToNullFilter()],
            validators=[IsIntegerValidator()]
        )

        # Optional string field with regex validation
        zipcode: str = field(
            filters=[StringTrimFilter()],
            validators=[
                RegexValidator(
                    RegexEnum.POSTAL_CODE.value,
                    'The zipcode is not in the correct format.'
                )
            ]
        )

        # Optional string field
        city: str = field(
            filters=[StringTrimFilter()],
            validators=[IsStringValidator()]
        )

        # Business rule: either zipcode OR city must be provided, but not both
        _conditions = [ExactlyOneOfCondition(['zipcode', 'city'])]

Step 2: Use in Your Flask Route
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The most common way is to use the `@validate()` decorator:

.. code-block:: python

    from flask import Flask, g, jsonify

    app = Flask(__name__)

    @app.route('/update-zipcode', methods=['POST'])
    @UpdateZipcodeInputFilter.validate()
    def update_zipcode():
        # Access validated and filtered data
        data = g.validated_data

        # All data is guaranteed to be valid at this point
        user_id = data.get('id')        # Always an integer
        zipcode = data.get('zipcode')   # Trimmed string or None
        city = data.get('city')         # Trimmed string or None

        # Your business logic here
        return jsonify({"success": True, "user_id": user_id})

Step 3: Handle Validation Errors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If validation fails, flask-inputfilter automatically returns a 400 response with error details:

.. code-block:: json

    {
        "id": "This field is required.",
        "zipcode": "The zipcode is not in the correct format.",
        "_condition": "Exactly one of the following fields must be present: zipcode, city"
    }

Alternative: Manual Validation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can also validate data manually without using the decorator:

.. code-block:: python

    @app.route('/manual-validation', methods=['POST'])
    def manual_validation():
        input_filter = UpdateZipcodeInputFilter()
        input_filter.set_data(request.get_json())

        if input_filter.is_valid():
            validated_data = input_filter.get_data()
            return jsonify({"success": True, "data": validated_data})
        else:
            errors = input_filter.get_errors()
            return jsonify({"success": False, "errors": errors}), 400
