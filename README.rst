flask-inputfilter
=================

The ``InputFilter`` class is used to validate and filter input data in Flask applications.
It provides a modular way to clean and ensure that incoming data meets expected format
and type requirements before being processed.

Thank you for using ``flask-inputfilter``!
==========================================

If you have any questions or suggestions, please feel free to open an issue on `GitHub <https://github.com/LeanderCS/flask-inputfilter>`__.

If you don't want to miss any updates, please star the repository.
This will help me to understand how many people are interested in this project.

For information about the usage you can view the `documentation <https://leandercs.github.io/flask-inputfilter>`__.

:Test Status:

    .. image:: https://img.shields.io/github/actions/workflow/status/LeanderCS/flask-inputfilter/test.yaml?branch=main&style=flat-square&label=Github%20Actions
        :target: https://github.com/LeanderCS/flask-inputfilter/actions
    .. image:: https://img.shields.io/coveralls/LeanderCS/flask-inputfilter/main.svg?style=flat-square&label=Coverage
        :target: https://coveralls.io/r/LeanderCS/flask-inputfilter

:Version Info:

    .. image:: https://img.shields.io/pypi/v/flask-inputfilter?style=flat-square&label=PyPI
        :target: https://pypi.org/project/flask-inputfilter/

:Compatibility:

    .. image:: https://img.shields.io/pypi/pyversions/flask-inputfilter?style=flat-square&label=PyPI
        :target: https://pypi.org/project/flask-inputfilter/

:Downloads:

    .. image:: https://static.pepy.tech/badge/flask-inputfilter/month
        :target: https://pypi.org/project/flask-inputfilter/
    .. image:: https://static.pepy.tech/badge/flask-inputfilter
        :target: https://pypi.org/project/flask-inputfilter/

Installation
============

.. code-block:: bash

    pip install flask-inputfilter

Quickstart
==========

To use the ``InputFilter`` class, create a new class that inherits from it and define the
fields you want to validate and filter.

There are numerous filters and validators available, but you can also create your `own <https://leandercs.github.io/flask-inputfilter/guides/create_own.html>`__.

Definition
----------

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.conditions import ExactlyOneOfCondition
    from flask_inputfilter.enums import RegexEnum
    from flask_inputfilter.filters import StringTrimFilter, ToIntegerFilter, ToNullFilter
    from flask_inputfilter.validators import IsIntegerValidator, IsStringValidator, RegexValidator

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
-----

To use the ``InputFilter`` class, call the ``validate`` method on the class instance.
After calling ``validate``, the validated data will be available in ``g.validated_data``.
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


See also
========

For further instructions please view the `documentary <https://leandercs.github.io/flask-inputfilter>`__.

For ideas, suggestions or questions, please open an issue on `GitHub <https://github.com/LeanderCS/flask-inputfilter>`__.

