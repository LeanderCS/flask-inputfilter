Frontend Validation
===================

Keeping frontend and backend validations synchronized can take a lot of time and
may lead to unexpected behavior if not maintained properly.

With ``flask_inputfilter`` you can easily implement an extra route to keep up with the validation and
use the same ``InputFilter`` definition both for the frontend and backend validation.


Example implementation
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from flask import Response, Flask

    app = Flask(__name__)

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
                        pattern=RegexEnum.POSTAL_CODE.value,
                        error_message='The zipcode is not in the correct format.'
                    )
                ]
            )

    @app.route('/form-update-zipcode', methods=['POST'])
    @UpdateZipcodeInputFilter.validate()
    def updateZipcode():
        return Response(status=200)

This basic implementation allows you to validate the form in the frontend through the route ``/form-update-zipcode``.
If the validation is successful, it returns an empty response with the status code 200.
If it fails, it returns an response with the status code 400 and the corresponding errors in json format.

If the validation for the zipcode fails, the response would be:

.. code-block:: python

    {
        "zipcode": "The zipcode is not in the correct format."
    }

Validation errors of conditions can be found in the ``_condition`` field.
