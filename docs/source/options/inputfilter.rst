InputFilter
===========

Overview
--------

.. autoclass:: flask_inputfilter.input_filter.InputFilter
   :members:
   :undoc-members:
   :show-inheritance:

Configuration
-------------

The ``field`` decorator supports several options:

- `Required`_
- `Filters`_
- `Validators`_
- `Default`_
- `Fallback`_
- `Steps`_
- `ExternalApi`_
- `Copy`_

Required
~~~~~~~~

The ``required`` option specifies whether the field must be included in the input data.
If the field is missing, a ``ValidationError`` will be raised with an appropriate error message.

Filters
~~~~~~~

The ``filters`` option allows you to specify one or more filters to apply to the field value.
Filters are applied in the order they are defined.

For more information view the :doc:`Filter <filter>` documentation.

Validators
~~~~~~~~~~

The ``validators`` option allows you to specify one or more validators to apply to the field value.
Validators are applied in the order they are defined.

For more information view the :doc:`Validator <validator>` documentation.

Default
~~~~~~~

The ``default`` option allows you to specify a default value to use if the field is not
present in the input data.

Fallback
~~~~~~~~

The ``fallback`` option specifies a value to use if validation fails or required data
is missing. Note that if the field is optional and absent, ``fallback`` will not apply;
use ``default`` in such cases.

Steps
~~~~~

The ``steps`` option allows you to specify a list of different filters and validator to apply to the field value.
It respects the order of the list.

ExternalApi
~~~~~~~~~~~

The ``external_api`` option allows you to specify an external API to call for the field value.
The API call is made when the field is validated, and the response is used as the field value.

For more information view the :doc:`ExternalApi <external_api>` documentation.

Copy
~~~~

The ``copy`` option allows you to copy the value of another field.
The copied value can be filtered and validated, due to the coping being executed first.

For more information view the :doc:`Copy <copy>` documentation.


Examples
--------

Least config
~~~~~~~~~~~~

Here's a minimal example with just basic field definitions:

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.declarative import field

    class SimpleInputFilter(InputFilter):
        name: str = field()
        age: int = field()
        email: str = field()

Full config
~~~~~~~~~~~

Here's a comprehensive example using all available field options:

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.declarative import field
    from flask_inputfilter.conditions import ExactlyOneOfCondition
    from flask_inputfilter.filters import StringTrimFilter, ToIntegerFilter
    from flask_inputfilter.validators import IsIntegerValidator, RegexValidator
    from flask_inputfilter.enums import RegexEnum

    class AdvancedInputFilter(InputFilter):
        # Required field with filters and validators
        user_id: int = field(
            required=True,
            filters=[ToIntegerFilter()],
            validators=[IsIntegerValidator()],
            fallback=0
        )

        # Optional field with default value
        username: str = field(
            required=False,
            default="anonymous",
            filters=[StringTrimFilter()],
            validators=[RegexValidator(r'^[a-zA-Z0-9_]+$', 'Username must be alphanumeric')]
        )

        # Field with external API integration
        profile_data: dict = field(
            external_api={
                "url": "https://api.example.com/profile/{{user_id}}",
                "method": "GET",
                "data_key": "profile"
            },
            fallback={}
        )

        # Field with copy from another field
        display_name: str = field(
            copy="username",
            filters=[StringTrimFilter()]
        )

        # Field with multiple validation steps
        score: int = field(
            steps=[
                {
                    "filters": [ToIntegerFilter()],
                    "validators": [IsIntegerValidator()]
                }
            ]
        )

        # Conditions to enforce business rules
        _conditions = [
            ExactlyOneOfCondition(['username', 'profile_data'])
        ]

Usage Examples
~~~~~~~~~~~~~~

Basic usage with Flask route:

.. code-block:: python

    from flask import Flask, g, jsonify

    app = Flask(__name__)

    @app.route('/user', methods=['POST'])
    @AdvancedInputFilter.validate()
    def create_user():
        data = g.validated_data

        # All data is now validated and filtered
        user_id = data.get('user_id')
        username = data.get('username')
        profile_data = data.get('profile_data')

        return jsonify({"success": True, "user_id": user_id})

Manual validation without decorator:

.. code-block:: python

    def process_data(raw_data):
        input_filter = AdvancedInputFilter()
        input_filter.set_data(raw_data)

        if input_filter.is_valid():
            validated_data = input_filter.get_data()
            return {"success": True, "data": validated_data}
        else:
            return {"success": False, "errors": input_filter.get_errors()}
