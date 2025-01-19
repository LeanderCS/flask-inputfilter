flask-inputfilter
==================================

The ``InputFilter`` class is used to validate and filter input data in Flask applications.
It provides a modular way to clean and ensure that incoming data meets expected format
and type requirements before being processed.

.. raw:: html

    <div style="border:1px solid #86989B;padding:1rem;border-radius:3px;background-color:#f7f7f7;">
        <p style="background-color:hsl(219.5, 84%, 90%);margin:-1rem -1rem 0.8rem -1rem;padding:0.3rem 1rem 0.3rem 2.5rem;position:relative;border-radius:3px 3px 0 0;">
            <span style="content:'';position:absolute;top:.25rem;left:.5rem;width:1.5rem;height:1.5rem;background-color:hsl(219.5, 84%, 50%);mask-image:url('data:image/svg+xml;charset=utf-8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M20.71 7.04c.39-.39.39-1.04 0-1.41l-2.34-2.34c-.37-.39-1.02-.39-1.41 0l-1.84 1.83 3.75 3.75M3 17.25V21h3.75L17.81 9.93l-3.75-3.75L3 17.25z"/></svg>');"></span>
            Tip
        </p>
        <p style="margin:0;">
            Thank you for using <code>flask-inputfilter</code>!<br>
            If you have any questions or suggestions, please feel free to open an issue on GitHub <a href="https://github.com/LeanderCS/flask-inputfilter">here</a>.<br>
            If you don't want to miss any updates, please star the repository.<br>
            This will help me to understand how many people are interested in this project.<br>
        </p>
    </div>

.. raw:: html

    <div style="border:1px solid #86989B;padding:1rem;border-radius:3px;background-color:#f7f7f7;">
        <p style="background-color:hsl(150, 36.7%, 90%);margin:-1rem -1rem 0.8rem -1rem;padding:0.3rem 1rem 0.3rem 2.5rem;position:relative;border-radius:3px 3px 0 0;">
            <span style="content:'';position:absolute;top:.25rem;left:.5rem;width:1.5rem;height:1.5rem;background-color:hsl(150, 36.7%, 50%);mask-image:url('data:image/svg+xml;charset=utf-8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M15.07 11.25l-.9.92C13.45 12.89 13 13.5 13 15h-2v-.5c0-1.11.45-2.11 1.17-2.83l1.24-1.26c.37-.36.59-.86.59-1.41a2 2 0 00-2-2 2 2 0 00-2 2H8a4 4 0 014-4 4 4 0 014 4 3.2 3.2 0 01-.93 2.25M13 19h-2v-2h2M12 2A10 10 0 002 12a10 10 0 0010 10 10 10 0 0010-10c0-5.53-4.5-10-10-10z"/></svg>');"></span>
            Hint
        </p>
        <p style="margin:0;">
            For information about the usage you can view the documentation
        </p>
    </div>

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

    .. image:: https://img.shields.io/pypi/dm/flask-inputfilter?style=flat-square&label=PyPI
        :target: https://pypi.org/project/flask-inputfilter/

Installation
============

.. code-block:: bash

    pip install flask-inputfilter

Quickstart
==========

To use the ``InputFilter`` class, create a new class that inherits from it and define the
fields you want to validate and filter.

There are numerous filters and validators available, but you can also create your `own <CreateOwn.md>`_.

Definition
----------

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


.. raw:: html

    <div style="border:1px solid #86989B;padding:1rem;border-radius:3px;background-color:#f7f7f7;">
        <p style="background-color:hsl(150, 36.7%, 90%);margin: -1rem -1rem 0.8rem -1rem;padding:0.3rem 1rem 0.3rem 2.5rem;position:relative;border-radius:3px 3px 0 0;">
            <span style="content:'';position:absolute;top:.25rem;left:.5rem;width:1.5rem;height:1.5rem;background-color:hsl(150,36.7%,50%);mask-image:url('data:image/svg+xml;charset=utf-8,<svg xmlns=&quot;http://www.w3.org/2000/svg&quot; viewBox=&quot;0 0 24 24&quot;><path d=&quot;M13 9h-2V7h2m0 10h-2v-6h2m-1-9A10 10 0 002 12a10 10 0 0010 10 10 10 0 0010-10A10 10 0 0012 2z&quot;/></svg>');"></span>
            Tip
        </p>
        <p style="margin:0;">
            For further instructions please view the documentary `Here <https://github.com/LeanderCS/flask-inputfilter.<br>

            For ideas, suggestions or questions, please open an issue on GitHub <a href="https://github.com/LeanderCS/flask-inputfilter">here</a>.
        </p>
    </div>
