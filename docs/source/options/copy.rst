Copy functionality
==================

Overview
--------

The copy functionality is configured via the ``copy`` parameter in the ``add`` method.
This parameter accepts a string with the name the value should be copied from.

.. note::

    The copy functionality runs **before** all filters and validators have been executed.
    This means the copied data can be validated and/or filtered.

Example
-------

Basic Copy Integration

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Filter import SlugifyFilter

    class MyInputFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add(
                "username"
            )

            self.add(
                "escapedUsername",
                copy="username"
                filters=[SlugifyFilter()]
            )

    # Example usage
    # Body: {"username": "Very Important User"}

    @app.route("/test", methods=["GET"])
    @MyInputFilter.validate()
    def test_route():
        validated_data = g.validated_data

        # Cotains the same value as username but escaped eg. "very-important-user"
        print(validated_data["escapedUsername"])


The coping can also be used as a chain.

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.Filter import SlugifyFilter, ToUpperFilter, ToLowerFilter

    class MyInputFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add(
                "username"
            )

            self.add(
                "escapedUsername",
                copy="username"
                filters=[SlugifyFilter()]
            )

            self.add(
                "upperEscapedUsername",
                copy="escapedUsername"
                filters=[ToUpperFilter()]
            )

            self.add(
                "lowerEscapedUsername",
                copy="escapedUsername"
                filters=[ToLowerFilter()]
            )
