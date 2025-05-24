Deserialization
===============

Deserialization in Flask-InputFilter allows you to convert validated data 
into custom model objects or maintain it as a dictionary. This feature is 
particularly useful when you want to work with strongly-typed objects in 
your application.

Overview
--------

The deserialization process is handled through two main methods:

- ``set_model()``: Sets the model class to be used for deserialization
- ``serialize()``: Converts the validated data into an instance of the 
  specified model class or returns the raw data as a dictionary

Configuration
-------------

The ``validate()`` method will automatically deserialize the validated data 
into an instance of the model class, if there is a model class set.

.. code-block:: python

    from dataclasses import dataclass


    @dataclass
    class User:
        username: str
        email: str


    class UserInputFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.set_model(User)

Examples
--------

Usage with Flask Routes
^^^^^^^^^^^^^^^^^^^^^^^

You can also use deserialization in your Flask routes:

.. code-block:: python

    from flask import Flask, jsonify, g


    class User:
        def __init__(self, username: str):
            self.username = username


    class MyInputFilter(InputFilter):
        def __init__(self):
            super().__init__(methods=["GET"])
            self.add("username")
            self.set_model(User)


    app = Flask(__name__)

    @app.route("/test", methods=["GET"])
    @MyInputFilter.validate()
    def test_route():
        # g.validated_data will contain the deserialized User instance

        validated_data: User = g.validated_data

Usage outside of Flask Routes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can also use deserialization outside of Flask routes:

.. code-block:: python

    from flask import Flask, jsonify, g


    class User:
        def __init__(self, username: str):
            self.username = username


    class MyInputFilter(InputFilter):
        def __init__(self):
            super().__init__(methods=["GET"])
            self.add("username")
            self.set_model(User)

    app = Flask(__name__)

    @app.route("/test", methods=["GET"])
    def test_route():
        input_filter = MyInputFilter()
        input_filter.set_data({"username": "test user"})

        if not input_filter.is_valid():
            return jsonify({"error": "Invalid data"}), 400

        validated_data: User = input_filter.serialize()
