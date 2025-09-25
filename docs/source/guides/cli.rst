CLI Code Generation
==================

Flask InputFilter includes a powerful command-line interface (CLI) for generating InputFilter classes from JSON Schema files. This feature significantly speeds up development by automatically creating validation code from API specifications or data schemas.

Installation
------------

To use the CLI features, install Flask InputFilter with the ``cli`` extra::

    pip install flask-inputfilter[cli]

This installs the following additional dependencies:

- ``click>=8.0`` - Command-line interface framework
- ``jinja2>=3.0`` - Template engine for code generation
- ``jsonschema>=4.0`` - JSON Schema validation library

Quick Start
-----------

Generate an InputFilter class from a JSON Schema file::

    fif generate --schema user_schema.json --class UserInputFilter --out user_filter.py

This command:

1. Reads the JSON Schema from ``user_schema.json``
2. Generates a ``UserInputFilter`` class with appropriate validators and filters
3. Saves the result to ``user_filter.py``

Example Schema and Generated Code
---------------------------------

Given this JSON Schema (``user_schema.json``):

.. code-block:: json

    {
      "$schema": "https://json-schema.org/draft/2020-12/schema",
      "title": "User",
      "description": "User registration data",
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "description": "User's full name",
          "minLength": 2,
          "maxLength": 100
        },
        "email": {
          "type": "string",
          "description": "User's email address",
          "format": "email"
        },
        "age": {
          "type": "integer",
          "description": "User's age",
          "minimum": 18,
          "maximum": 120
        }
      },
      "required": ["name", "email"],
      "additionalProperties": false
    }

The CLI generates this Python code:

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.declarative import field
    from flask_inputfilter.filters import StringTrimFilter
    from flask_inputfilter.validators import (
        CustomJsonValidator, IsIntegerValidator, IsStringValidator,
        LengthValidator, RangeValidator, RegexValidator
    )
    from flask_inputfilter.enums import RegexEnum


    class UserInputFilter(InputFilter):
        """User
        User registration data"""

        # User's full name
        name = field(required=True, filters=[StringTrimFilter()], validators=[IsStringValidator(), LengthValidator(min_length=2, max_length=100)])

        # User's email address
        email = field(required=True, filters=[StringTrimFilter()], validators=[RegexValidator(RegexEnum.EMAIL.value, 'Invalid email format.')])

        # User's age
        age = field(validators=[IsIntegerValidator(), RangeValidator(min_value=18, max_value=120)])

        _global_validators = [CustomJsonValidator({'additionalProperties': False})]

Command Reference
-----------------

generate
~~~~~~~~

Generate InputFilter classes from JSON Schema files.

**Syntax:**

.. code-block:: bash

    fif generate [OPTIONS]

**Required Options:**

``--schema PATH``
    Path to the JSON Schema file

``--class NAME``
    Name of the generated InputFilter class

**Optional Options:**

``--out PATH``
    Output file path. Use ``-`` for stdout (default)

``--base-class NAME``
    Base class name (default: ``InputFilter``)

``--base-module MODULE``
    Module to import base class from (default: ``flask_inputfilter``)

``--field-import MODULE``
    Module to import the ``field`` function from

``--field-name NAME``
    Name of the field builder function (default: ``field``)

``--strict``
    Fail if schema properties cannot be mapped to validators

``--docstring/--no-docstring``
    Include schema title and description as class docstring (default: enabled)

``--template PATH``
    Path to custom Jinja2 template file

**Examples:**

Basic usage::

    fif generate --schema user.json --class UserInputFilter

Save to file::

    fif generate --schema user.json --class UserInputFilter --out filters/user.py

Use strict validation::

    fif generate --schema user.json --class UserInputFilter --strict

Custom base class::

    fif generate --schema user.json --class UserInputFilter --base-class CustomFilter --base-module myapp.base

help
~~~~

Show help information for CLI commands.

**Syntax:**

.. code-block:: bash

    fif help [COMMAND]

**Arguments:**

``COMMAND`` (optional)
    Show help for a specific command. If omitted, shows general help.

**Description:**

The ``help`` command provides comprehensive help information for the Flask InputFilter CLI. When called without arguments, it displays an organized overview of all available commands grouped by category. When called with a specific command name, it shows detailed help for that command.

**Examples:**

General help::

    fif help

Help for specific command::

    fif help generate

**Features:**

- **Organized by categories**: Commands are grouped into logical sections (Code Generation, Utilities, etc.)
- **Practical examples**: Shows common usage patterns
- **Command discovery**: Lists all available commands with brief descriptions
- **Error handling**: Provides helpful feedback for unknown commands
- **Multiple access methods**: Works alongside standard ``--help`` flags

The help system is designed to be both comprehensive for new users and quick for experienced users who need specific command details.

Supported JSON Schema Features
------------------------------

Data Types
~~~~~~~~~~~

+-------------+----------------------+-------------------+
| Schema Type | Generated Validator  | Generated Filter  |
+=============+======================+===================+
| ``string``  | ``IsStringValidator``| ``StringTrimFilter`` |
+-------------+----------------------+-------------------+
| ``integer`` | ``IsIntegerValidator``| None             |
+-------------+----------------------+-------------------+
| ``number``  | ``IsFloatValidator`` | ``ToFloatFilter`` |
+-------------+----------------------+-------------------+
| ``boolean`` | ``IsBooleanValidator``| None             |
+-------------+----------------------+-------------------+
| ``array``   | ``IsArrayValidator`` | None             |
+-------------+----------------------+-------------------+

String Formats
~~~~~~~~~~~~~~

+---------------+----------------------------------+
| Format        | Generated Validator              |
+===============+==================================+
| ``email``     | ``RegexValidator(RegexEnum.EMAIL.value)`` |
+---------------+----------------------------------+
| ``uri``       | ``RegexValidator(RegexEnum.URL.value)``   |
+---------------+----------------------------------+
| ``uuid``      | ``IsUUIDValidator``              |
+---------------+----------------------------------+
| ``date``      | ``IsDateValidator``              |
+---------------+----------------------------------+
| ``date-time`` | ``IsDateTimeValidator``          |
+---------------+----------------------------------+
| ``ipv4``      | ``RegexValidator(RegexEnum.IPV4.value)``  |
+---------------+----------------------------------+
| ``ipv6``      | ``RegexValidator(RegexEnum.IPV6.value)``  |
+---------------+----------------------------------+

Constraints
~~~~~~~~~~~

+---------------------------+----------------------------------------+
| JSON Schema Constraint    | Generated Validator                    |
+===========================+========================================+
| ``minLength``/``maxLength`` | ``LengthValidator(min_length=X, max_length=Y)`` |
+---------------------------+----------------------------------------+
| ``minimum``/``maximum``   | ``RangeValidator(min_value=X, max_value=Y)``     |
+---------------------------+----------------------------------------+
| ``minItems``/``maxItems`` | ``ArrayLengthValidator(min_length=X, max_length=Y)`` |
+---------------------------+----------------------------------------+
| ``pattern``               | ``RegexValidator(r'pattern', 'Error message')``     |
+---------------------------+----------------------------------------+
| ``enum``                  | ``InArrayValidator([...])``            |
+---------------------------+----------------------------------------+

Schema-Level Features
~~~~~~~~~~~~~~~~~~~~

+----------------------------+----------------------------------------------+
| JSON Schema Feature        | Generated Code                               |
+============================+==============================================+
| ``required``               | ``field(required=True, ...)``               |
+----------------------------+----------------------------------------------+
| ``default``                | ``field(default=value, ...)``               |
+----------------------------+----------------------------------------------+
| ``description``            | Python comment above field definition       |
+----------------------------+----------------------------------------------+
| ``additionalProperties: false`` | ``_global_validators = [CustomJsonValidator(...)]`` |
+----------------------------+----------------------------------------------+

Integration with Flask Applications
-----------------------------------

Generated InputFilter classes work seamlessly with Flask routes:

.. code-block:: python

    from flask import Flask, g, jsonify
    from .filters.user_filter import UserInputFilter

    app = Flask(__name__)

    @app.route('/users', methods=['POST'])
    @UserInputFilter.validate()
    def create_user():
        data = g.validated_data

        # All data is validated according to the JSON Schema
        name = data['name']      # Required, 2-100 chars
        email = data['email']    # Required, valid email
        age = data.get('age')    # Optional, 18-120 if provided

        # Create user in database...
        return jsonify({'status': 'created'})

Advanced Usage
--------------

Custom Templates
~~~~~~~~~~~~~~~~

You can provide your own Jinja2 template for code generation:

.. code-block:: bash

    fif generate --schema user.json --class UserFilter --template my_template.j2

The template receives these context variables:

- ``base_module``, ``base_class`` - Import information
- ``class_name`` - Generated class name
- ``schema_title``, ``schema_description`` - From JSON Schema
- ``fields`` - List of field definitions with validators and filters
- ``import_filters``, ``import_validators``, ``import_enums`` - Required imports
- ``global_validators`` - Schema-level validators

CI/CD Integration
~~~~~~~~~~~~~~~~~

The CLI is ideal for automated code generation in CI/CD pipelines:

.. code-block:: yaml

    # GitHub Actions example
    - name: Generate InputFilter classes
      run: |
        for schema in schemas/*.json; do
          class_name=$(basename "$schema" .json | sed 's/.*/\u&/')InputFilter
          fif generate --schema "$schema" --class "$class_name" --out "src/filters/"
        done

Working with OpenAPI Specifications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

While the CLI currently supports JSON Schema directly, you can extract schemas from OpenAPI specifications:

.. code-block:: bash

    # Extract user schema from OpenAPI spec
    yq eval '.components.schemas.User' openapi.yaml > user_schema.json

    # Generate InputFilter
    fif generate --schema user_schema.json --class UserInputFilter

Best Practices
--------------

Schema Organization
~~~~~~~~~~~~~~~~~~~

- Keep JSON schemas in a dedicated directory (e.g., ``schemas/``)
- Use descriptive filenames that match your model names
- Include meaningful ``title`` and ``description`` fields
- Set ``additionalProperties: false`` for strict validation

Code Generation
~~~~~~~~~~~~~~~

- Use consistent naming conventions for generated classes (e.g., ``ModelNameInputFilter``)
- Generate filters into a dedicated module (e.g., ``filters/`` or ``validation/``)
- Consider using ``--strict`` mode in CI/CD to catch schema issues early
- Version control both schemas and generated code for traceability

Error Handling
~~~~~~~~~~~~~~

- Use descriptive error messages in your schemas
- Test generated validators with valid and invalid data
- Consider custom error messages for business-specific validation rules

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**"No such command 'generate'"**

Ensure you installed with the CLI extra::

    pip install flask-inputfilter[cli]

**"Invalid JSON Schema" errors**

Use the ``--strict`` flag for detailed validation feedback::

    fif generate --schema user.json --class UserFilter --strict

**Import errors in generated code**

Verify that your flask-inputfilter version supports all generated validators and filters.

**Unexpected validator parameters**

This indicates a version mismatch. Ensure you're using a compatible flask-inputfilter version.

Getting Help
~~~~~~~~~~~~

For command-specific help::

    fif --help
    fif generate --help

For issues and feature requests, visit the `GitHub repository <https://github.com/LeanderCS/flask-inputfilter/issues>`_.