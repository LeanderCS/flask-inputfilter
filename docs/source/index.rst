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

Definition
^^^^^^^^^^

.. code-block:: python

    class UpdateZipcodeInputFilter(InputFilter):
        id: int = field(
            required=True,
            filters=[ToIntegerFilter(), ToNullFilter()],
            validators=[IsIntegerValidator()]
        )

        zipcode: str = field(
            filters=[StringTrimFilter()],
            validators=[
                RegexValidator(
                    RegexEnum.POSTAL_CODE,
                    'The zipcode is not in the correct format.'
                )
            ]
        )

        city: str = field(
            filters=[StringTrimFilter()],
            validators=[IsStringValidator()]
        )

        condition(ExactlyOneOfCondition(['zipcode', 'city']))

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
        city = data.get('city')
