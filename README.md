# flask-inputfilter

The `InputFilter` class is used to validate and filter input data in Flask applications.
It provides a modular way to clean and ensure that incoming data meets expected format and type requirements before being processed.

---

## Installation

```bash
pip install flask-inputfilter
```

---

## Quickstart

To use the `InputFilter` class, you need to create a new class that inherits from it and define the fields you want to validate and filter.
There are lots of different filters and validators available to use, and you can also create your own custom filters and validators.

### Definition

```python
from flask_inputfilter import InputFilter
from flask_inputfilter.Enum import RegexEnum
from flask_inputfilter.Filter import StringTrimFilter, ToIntegerFilter, ToNullFilter
from flask_inputfilter.Validator import IsIntegerValidator, RegexValidator 


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
            required=True,
            filters=[StringTrimFilter()],
            validators=[
                RegexValidator(
                    RegexEnum.POSTAL_CODE.value,
                    'The zipcode is not in the correct format.'
                )
            ]
        )
```

### Usage

To use the `InputFilter` class, you need to call the `validate` method on the class instance.
After calling the `validate` method, the validated data will be available in the `g.validatedData` object in the wanted format.
If the data is not valid, the `validate` method will return a 400 response with the error message.

```python
from flask import Flask, g
from your-path import UpdateZipcodeInputFilter

app = Flask(__name__)

@app.route('/update-zipcode', methods=['POST'])
@UpdateZipcodeInputFilter.validate()
def updateZipcode():
    data = g.validatedData

    # Do something with validatedData
    id = data.get('id')
    zipcode = data.get('zipcode')
```

---

## Options

The `add` method takes the following options:

- [`Required`](#required)
- [`Filter`](src/flask_inputfilter/Filter/README.md)
- [`Validator`](src/flask_inputfilter/Validator/README.md)
- [`Default`](#default)
- [`Fallback`](#fallback)
- [`ExternalApi`](EXTERNAL_API.md)

### Required

The `required` option is used to specify if the field is required or not.
If the field is required and not present in the input data, the `validate` method will return the `ValidationError` with an error message.

### Default

The `default` option is used to specify a default value to use if the field is not present in the input data.

### Fallback

The `fallback` option is used to specify a fallback value to use if something unexpected happens, for example if the field is required but no value where provides 
 or the validation fails.

This means that if the field is not required and no value is present, the fallback value will not be used.
In this case you have to use the `default` option.
