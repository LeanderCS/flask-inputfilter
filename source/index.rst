flask-inputfilter documentation
===============================

Overview
--------

..  toctree::
    :maxdepth: 1

    options/index
    guides/index
    changelog
    contributing
    development

Available functions:
--------------------

- :doc:`Creating your own Conditions, Filters and Validators <guides/create_own>`
- :doc:`Conditions <options/condition>`
- :doc:`Filter <options/filter>`
- :doc:`Validator <options/validator>`
- :doc:`ExternalApi <options/external_api>`

Installation
------------

.. code-block:: bash

    pip install flask-inputfilter

Quickstart
----------

To use the `InputFilter` class, create a new class that inherits from it and define the
fields you want to validate and filter.

There are numerous filters and validators available, but you can also create your [`own`](CreateOwn.md).

Definition
^^^^^^^^^^

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Condition import ExactlyOneOfCondition
    from flask_inputfilter.Enum import RegexEnum
    from flask_inputfilter.Filter import StringTrimFilter, ToIntegerFilter, ToNullFilter
    from flask_inputfilter.Validator import IsIntegerValidator, IsStringValidator, RegexValidator

    class UpdateZipcodeInputFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add(
                'id',
                required=True,
                filters=[ToIntegerFilter(), ToNullFilter()],
                validators=[
                    IsIntegerValidator()
                ]
            )

            self.add(
                'zipcode',
                filters=[StringTrimFilter()],
                validators=[
                    RegexValidator(
                        RegexEnum.POSTAL_CODE.value,
                        'The zipcode is not in the correct format.'
                    )
                ]
            )

            self.add(
                'city',
                filters=[StringTrimFilter()],
                validators=[
                    IsStringValidator()
                ]
            )

            self.addCondition(
                ExactlyOneOfCondition(['zipcode', 'city'])
            )

Usage
^^^^^

To use the `InputFilter` class, call the `validate` method on the class instance.
After calling `validate`, the validated data will be available in `g.validated_data`.
If the data is invalid, a 400 response with an error message will be returned.

.. code-block:: python

    from flask import Flask, g
    from your-path import UpdateZipcodeInputFilter

    app = Flask(__name__)

    @app.route('/update-zipcode', methods=['POST'])
    @UpdateZipcodeInputFilter.validate()
    def updateZipcode():
        data = g.validated_data

        # Do something with validated data
        id = data.get('id')
        zipcode = data.get('zipcode')
