# flask-inputfilter

The `InputFilter` class is used to validate and filter input data in Flask applications.
It provides a modular way to clean and ensure that incoming data meets expected format and type requirements before being processed.

## Installation

```bash
pip install flask-inputfilter
```

## Usage

To use the `InputFilter` class, you need to create a new class that inherits from it and define the fields you want to validate and filter.
There are lots of different filters and validators available to use, and you can also create your own custom filters and validators.

### Definition

```python
from flask_inputfilter import InputFilter
from flask_inputfilter.Enum import RegexEnum
from flask_inputfilter.Filters import ToIntFilter, ToNullFilter, StringTrimFilter
from flask_inputfilter.Validators import RegexValidator

class UpdateZipcodeInputFilter(InputFilter):
    def __init__(self):

        super().__init__()

        self.add(
            'id',
            required=True,
            filters=[ToIntFilter(), ToNullFilter()]
        )

        self.add(
            'zipcode',
            required=True,
            filters=[StringTrimFilter()],
            validators=[
                RegexValidator(
                    RegexEnum.POSTAL_CODE.value,
                    'The email is not in the format of an email.'
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

app = Flask(__name__)

@app.route('/update-zipcode', methods=['POST'])
@UpdateZipcodeInputFilter.validate()
def updateZipcode():
    data = g.validatedData

    # Do something with validatedData
    id = data.get('id')
    zipcode = data.get('zipcode')
```

