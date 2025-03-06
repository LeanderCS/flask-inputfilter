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
- :doc:`Creating your own Conditions, Filters and Validators <guides/create_own>`
- :doc:`ExternalApi <options/external_api>`


.. raw:: html

    <div style="border:1px solid #86989B;padding:1rem;border-radius:3px;margin-top:40px;">
        <p style="background-color:hsl(219.5, 84%, 90%);margin:-1rem -1rem 0.8rem -1rem;padding:0.3rem 1rem 0.3rem 2.5rem;position:relative;border-radius:3px 3px 0 0;">
            <span style="content:'';position:absolute;top:.25rem;left:.5rem;width:1.5rem;height:1.5rem;background-color:hsl(219.5, 84%, 50%);mask-image:url('data:image/svg+xml;charset=utf-8,<svg xmlns=&quot;http://www.w3.org/2000/svg&quot; viewBox=&quot;0 0 24 24&quot;><path d=&quot;M20.71 7.04c.39-.39.39-1.04 0-1.41l-2.34-2.34c-.37-.39-1.02-.39-1.41 0l-1.84 1.83 3.75 3.75M3 17.25V21h3.75L17.81 9.93l-3.75-3.75L3 17.25z&quot;/></svg>');"></span>
            Tip
        </p>
        <p style="margin:0;">
            Thank you for using <code>flask-inputfilter</code>!<br>
            If you have any questions or suggestions, please feel free to open an issue on <a href="https://github.com/LeanderCS/flask-inputfilter">GitHub</a>.<br>
            If you don't want to miss any updates, please star the repository.<br>
            This will help me to understand how many people are interested in this project.<br>
        </p>
    </div>

Installation
------------

.. code-block:: bash

    pip install flask-inputfilter

Quickstart
----------

To use the `InputFilter` class, create a new class that inherits from it and define the
fields you want to validate and filter.

There are numerous filters and validators available, but you can also create your :doc:`own <guides/create_own>`.

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
