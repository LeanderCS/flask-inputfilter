OpenAPI Generator
=================

Overview
--------

The OpenAPI generator allows you to automatically generate InputFilter classes from OpenAPI specification files. This is particularly useful when you have an existing OpenAPI specification and want to use flask-inputfilter for validation.

Installation
------------

The OpenAPI generator requires ``pyyaml`` for parsing YAML files. Install it as an generate dependency:

.. code-block:: bash

    pip install flask-inputfilter[generate]

Or install pyyaml separately:

.. code-block:: bash

    pip install pyyaml

Basic Usage
-----------

Command Line Interface (CLI)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The easiest way to generate InputFilter classes is using the CLI command:

Generate all schemas to a single file:

.. code-block:: bash

    flask-inputfilter generate openapi api.yaml --output filters.py

Generate all schemas to separate files in a directory:

.. code-block:: bash

    flask-inputfilter generate openapi api.yaml --output-dir filters

Python API
~~~~~~~~~~

Generating from OpenAPI File
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can also use the Python API directly:

.. code-block:: python

    from flask_inputfilter.generators.openapi import generate_from_openapi

    # Generate all schemas from OpenAPI file
    code = generate_from_openapi(
        openapi_file="api.yaml",
        output_file="generated_filters.py"
    )

Generating Specific Schema
^^^^^^^^^^^^^^^^^^^^^^^^^^

You can generate a specific schema by providing the schema name:

.. code-block:: python

    code = generate_from_openapi(
        openapi_file="api.yaml",
        schema_name="User",
        output_file="user_filter.py"
    )

Generating from String
^^^^^^^^^^^^^^^^^^^^^^

You can also generate from OpenAPI content as a string:

.. code-block:: python

    openapi_yaml = """
    openapi: 3.0.0
    info:
      title: Test API
      version: 1.0.0
    components:
      schemas:
        User:
          type: object
          required:
            - name
            - email
          properties:
            name:
              type: string
              minLength: 2
              maxLength: 50
            email:
              type: string
              format: email
    """

    code = generate_from_openapi(
        openapi_content=openapi_yaml,
        format="yaml"
    )

Example OpenAPI Schema
----------------------

Here's an example OpenAPI schema:

.. code-block:: yaml

    openapi: 3.0.0
    info:
      title: User API
      version: 1.0.0
    components:
      schemas:
        User:
          type: object
          required:
            - name
            - email
          properties:
            name:
              type: string
              minLength: 2
              maxLength: 50
            email:
              type: string
              format: email
            age:
              type: integer
              minimum: 18
              maximum: 120
            active:
              type: boolean
              default: true
            tags:
              type: array
              items:
                type: string

Generated Output
----------------

The generator will create the following InputFilter class:

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.declarative import field
    from flask_inputfilter.filters import ToIntegerFilter, ToBooleanFilter
    from flask_inputfilter.validators import (
        IsStringValidator,
        IsIntegerValidator,
        IsBooleanValidator,
        LengthValidator,
        RangeValidator,
        RegexValidator,
        IsArrayValidator,
        ArrayElementValidator,
    )

    class UserInputFilter(InputFilter):
        name: str = field(
            required=True,
            validators=[
                IsStringValidator(),
                LengthValidator(min_length=2, max_length=50),
            ],
        )

        email: str = field(
            required=True,
            validators=[
                IsStringValidator(),
                RegexValidator(
                    pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                ),
            ],
        )

        age: int = field(
            required=False,
            filters=[ToIntegerFilter()],
            validators=[
                IsIntegerValidator(),
                RangeValidator(min_value=18, max_value=120),
            ],
        )

        active: bool = field(
            required=False,
            default=True,
            filters=[ToBooleanFilter()],
            validators=[IsBooleanValidator()],
        )

        tags: list[str] = field(
            required=False,
            validators=[
                IsArrayValidator(),
                ArrayElementValidator(element_filter=[IsStringValidator()]),
            ],
        )

Supported OpenAPI Features
--------------------------

Type Mappings
~~~~~~~~~~~~~

The generator supports the following OpenAPI types:

- **string** → ``IsStringValidator()``
- **integer** → ``ToIntegerFilter()`` + ``IsIntegerValidator()``
- **number** → ``ToFloatFilter()`` + ``IsFloatValidator()``
- **boolean** → ``ToBooleanFilter()`` + ``IsBooleanValidator()``
- **array** → ``IsArrayValidator()`` + element validation

Format Support
~~~~~~~~~~~~~~

The following formats are supported:

- **email** → ``RegexValidator()`` with email pattern
- **date** → ``ToDateFilter()`` + ``IsDateValidator()``
- **date-time** → ``ToDateTimeFilter()`` + ``IsDateTimeValidator()``
- **uri** → ``IsUrlValidator()``
- **uuid** → ``IsUUIDValidator()``

Constraints
~~~~~~~~~~~

The following constraints are mapped:

- **minLength / maxLength** → ``LengthValidator()``
- **minimum / maximum** → ``RangeValidator()``
- **pattern** → ``RegexValidator()``
- **enum** → ``InArrayValidator()``
- **minItems / maxItems** → ``ArrayLengthValidator()``

Other Features
~~~~~~~~~~~~~~

- **required** → ``required=True`` in field definition
- **default** → ``default=...`` in field definition
- **nested objects** → Separate InputFilter classes with ``input_filter`` parameter
- **$ref references** → Resolved and generated as separate classes

Nested Objects
--------------

When your OpenAPI schema contains nested objects, the generator will create separate InputFilter classes:

.. code-block:: yaml

    components:
      schemas:
        User:
          type: object
          properties:
            name:
              type: string
            address:
              type: object
              properties:
                street:
                  type: string
                city:
                  type: string

This will generate:

.. code-block:: python

    class AddressInputFilter(InputFilter):
        street: str = field(required=False, validators=[IsStringValidator()])
        city: str = field(required=False, validators=[IsStringValidator()])

    class UserInputFilter(InputFilter):
        name: str = field(required=False, validators=[IsStringValidator()])
        address: dict = field(
            required=False,
            input_filter=AddressInputFilter,
        )

Arrays
------

Arrays are supported with element validation:

.. code-block:: yaml

    properties:
      tags:
        type: array
        items:
          type: string

Generated as:

.. code-block:: python

    tags: list[str] = field(
        required=False,
        validators=[
            IsArrayValidator(),
            ArrayElementValidator(element_filter=[IsStringValidator()]),
        ],
    )

Enums
-----

Enum values are mapped to ``InArrayValidator``:

.. code-block:: yaml

    properties:
      status:
        type: string
        enum:
          - active
          - inactive
          - pending

Generated as:

.. code-block:: python

    status: str = field(
        required=False,
        validators=[
            IsStringValidator(),
            InArrayValidator(haystack=["active", "inactive", "pending"]),
        ],
    )

Using Generated Filters
------------------------

After generating the InputFilter classes, you can use them in your Flask application:

.. code-block:: python

    from flask import Flask, g, jsonify
    from generated_filters import UserInputFilter

    app = Flask(__name__)

    @app.route('/users', methods=['POST'])
    @UserInputFilter.validate()
    def create_user():
        # Access validated data
        data = g.validated_data
        return jsonify(data), 201

The validated data will be available in ``g.validated_data`` after the decorator validates the request.
If validation fails, a 400 response with error messages will be returned automatically.

Generating from Endpoints
-------------------------

Besides ``components/schemas``, the generator can create one InputFilter per
endpoint (path/method combination). Path parameters, query parameters and the
JSON request body are merged into a single filter — matching how
``InputFilter.validate()`` merges route kwargs, query arguments and the JSON
body into one data dictionary:

.. code-block:: bash

    # Generate schema classes plus one InputFilter per endpoint
    flask-inputfilter generate openapi api.yaml --output filters.py --include-endpoints

    # Generate only endpoint InputFilters
    flask-inputfilter generate openapi api.yaml --output filters.py --endpoints-only

    # Restrict to a single endpoint
    flask-inputfilter generate openapi api.yaml --output filters.py \
        --endpoints-only --path /users --method post

Or programmatically:

.. code-block:: python

    from flask_inputfilter.generators.openapi import generate_from_openapi

    code = generate_from_openapi(
        openapi_file="api.yaml",
        include_endpoints=True,
    )

Naming and semantics:

- If the operation has an ``operationId`` (e.g. ``createUser``), the class is
  named after it: ``CreateUserInputFilter``. Otherwise the HTTP method and the
  path segments are used: ``POST /users/{id}/orders`` becomes
  ``PostUsersIdOrdersInputFilter``. Name collisions get a numeric suffix.
- Path parameters are always generated as ``required=True`` (as mandated by
  OpenAPI); query parameters follow their own ``required`` flag.
- If the request body is a direct ``$ref`` to a generated schema class, the
  endpoint filter is emitted as a subclass of that class and only adds the
  parameter fields. Inline body schemas are expanded into regular fields.
- On a name collision between a parameter and a body property, the body
  property wins and a warning comment is emitted into the generated code.
- Endpoint generation is only supported with ``--output`` (single file).

Exporting InputFilters to OpenAPI
---------------------------------

The reverse direction is also supported: existing InputFilter classes can be
exported as OpenAPI 3.0 schema objects — for example to generate API
documentation directly from your filters:

.. code-block:: python

    from flask_inputfilter.generators.openapi import (
        to_openapi_components,
        to_openapi_schema,
    )

    # Bare schema object for a single filter
    schema = to_openapi_schema(UserInputFilter)

    # components/schemas document, nested filters become $refs
    document = to_openapi_components(UserInputFilter, OrderInputFilter)

Or via the CLI:

.. code-block:: bash

    # Export a single InputFilter as JSON schema object
    flask-inputfilter export openapi myapp.filters:UserInputFilter --output user.json

    # Export all InputFilters of a module as components document (YAML)
    flask-inputfilter export openapi myapp.filters --all --format yaml --output schemas.yaml

The exporter maps filters and validators back to schema keywords:

.. list-table::
   :header-rows: 1

   * - InputFilter component
     - OpenAPI keyword
   * - ``ToIntegerFilter`` / ``IsIntegerValidator``
     - ``type: integer``
   * - ``ToFloatFilter`` / ``IsFloatValidator``
     - ``type: number``
   * - ``ToBooleanFilter`` / ``IsBooleanValidator``
     - ``type: boolean``
   * - ``IsStringValidator``
     - ``type: string``
   * - ``IsEmailValidator`` / ``IsUrlValidator`` / ``IsUUIDValidator``
     - ``format: email`` / ``uri`` / ``uuid``
   * - ``ToDateFilter`` / ``ToDateTimeFilter``
     - ``format: date`` / ``date-time``
   * - ``LengthValidator``
     - ``minLength`` / ``maxLength``
   * - ``RangeValidator``
     - ``minimum`` / ``maximum``
   * - ``ArrayLengthValidator``
     - ``minItems`` / ``maxItems``
   * - ``RegexValidator``
     - ``pattern`` (well-known patterns become ``format``)
   * - ``InArrayValidator`` / ``InEnumValidator``
     - ``enum``
   * - ``ArrayElementValidator``
     - ``type: array`` with ``items``
   * - ``field(input_filter=...)``
     - nested object schema or ``$ref``

Features without an OpenAPI equivalent degrade gracefully into ``x-``
extension keywords instead of failing (disable with
``include_extensions=False``):

.. list-table::
   :header-rows: 1

   * - InputFilter feature
     - Behavior
   * - Custom / unmapped validators and filters
     - listed in ``x-validators`` / ``x-filters``
   * - ``computed`` fields
     - excluded by default; included with ``x-computed: true`` when
       ``include_computed=True``
   * - ``copy``
     - ``x-copied-from``
   * - ``fallback``
     - ``x-fallback`` (if JSON-serializable)
   * - ``external_api``
     - ``x-external-api: true``
   * - conditions
     - object-level ``x-conditions`` list
   * - global validators
     - object-level ``x-global-validators`` list

CLI Options
-----------

The CLI command supports the following options:

- ``openapi`` - Path to OpenAPI YAML or JSON file (required)
- ``--schema`` - Generate specific schema only (optional)
- ``--output`` - Output file path for single file generation (required if --output-dir not specified)
- ``--output-dir`` - Output directory for separate file generation (required if --output not specified)
- ``--include-endpoints`` - Also generate one InputFilter per endpoint
- ``--endpoints-only`` - Generate only endpoint InputFilters
- ``--path`` / ``--method`` - Restrict endpoint generation

Examples:

.. code-block:: bash

    # Generate all schemas to one file
    flask-inputfilter generate openapi api.yaml --output filters.py

    # Generate all schemas to separate files
    flask-inputfilter generate openapi api.yaml --output-dir filters/

    # Generate specific schema
    flask-inputfilter generate openapi api.yaml --schema User --output user_filter.py

Limitations
-----------

Currently, the following OpenAPI features are not fully supported:

- ``allOf``, ``oneOf``, ``anyOf`` (not supported)
- ``additionalProperties``
- Non-JSON request bodies (only ``application/json`` is processed)
- Endpoint generation with ``--output-dir``

Documented degradation behaviour:

- Circular ``$ref`` references terminate with ``{"type": "object"}``
  during schema resolution instead of raising ``RecursionError``.
- Circular nested InputFilters terminate during export with
  ``{"type": "object", "x-circular-ref": "<Name>"}`` instead of recursing
  forever (when extensions are enabled).
- Arrays of objects (and ``$ref`` items) are emitted as
  ``ArrayElementValidator(element_filter=NestedInputFilter())``.
- Property names that are not valid Python identifiers (keywords,
  hyphens, leading digits, …) are skipped during code generation; a
  ``# WARNING:`` comment is emitted in the generated file.
- ``operationId`` values and path segments are sanitized into valid
  Python class name parts (non-alphanumeric characters become
  separators; leading digits are prefixed).

Future enhancements may add support for these features.
