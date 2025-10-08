# flask-inputfilter


[![](https://img.shields.io/pypi/v/flask-inputfilter?style=flat-square&label=version)](https://pypi.org/project/flask-inputfilter/)
[![](https://img.shields.io/pypi/pyversions/flask-inputfilter)](https://pypi.org/project/flask-inputfilter/)
[![](https://img.shields.io/github/license/LeanderCS/flask-inputfilter)](https://github.com/LeanderCS/flask-inputfilter/blob/main/LICENSE)
[![](https://img.shields.io/github/actions/workflow/status/LeanderCS/flask-inputfilter/test.yaml?branch=main&style=flat-square&label=tests)](https://github.com/LeanderCS/flask-inputfilter/actions)
[![](https://img.shields.io/coveralls/LeanderCS/flask-inputfilter/main.svg?style=flat-square&label=coverage)](https://coveralls.io/r/LeanderCS/flask-inputfilter)
[![](https://static.pepy.tech/badge/flask-inputfilter/month)](https://pypi.org/project/flask-inputfilter/)
[![](https://static.pepy.tech/badge/flask-inputfilter)](https://pypi.org/project/flask-inputfilter/)

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=LeanderCS_flask-inputfilter&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=LeanderCS_flask-inputfilter)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=LeanderCS_flask-inputfilter&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=LeanderCS_flask-inputfilter)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=LeanderCS_flask-inputfilter&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=LeanderCS_flask-inputfilter)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=LeanderCS_flask-inputfilter&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=LeanderCS_flask-inputfilter)<br/>
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=LeanderCS_flask-inputfilter&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=LeanderCS_flask-inputfilter)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=LeanderCS_flask-inputfilter&metric=bugs)](https://sonarcloud.io/summary/new_code?id=LeanderCS_flask-inputfilter)
[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=LeanderCS_flask-inputfilter&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=LeanderCS_flask-inputfilter)
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=LeanderCS_flask-inputfilter&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=LeanderCS_flask-inputfilter)


## Description

This library is a Flask extension that provides a simple way to validate and filter input data.
It allows you to define a set of rules for each field in your input data, including filters and validators.
The library also supports conditions that can be used to enforce complex validation rules.
It is designed to be straightforward to use and flexible, allowing you to create custom filters and validators as needed.


## Quickstart

To use the `InputFilter` class, create a new class that inherits from it and define the
fields you want to validate and filter.

There are many filters and validators available, but you can also create your [own](https://leandercs.github.io/flask-inputfilter/guides/create_own_components.html).


## Installation

Using [pip](https://pip.pypa.io/en/stable/getting-started/):
```bash
  pip install flask-inputfilter
```

Using [UV](https://docs.astral.sh/uv/):  
```shell
  uv add flask-inputfilter
```

Using [Poetry](https://python-poetry.org/docs/): 
```shell
  poetry add flask-inputfilter
```

There are plenty of wheels for all major environments and all supported python versions.
But if you happen to use an environment where there is no wheel prebuilt, you can use either 
the python implementation or you can install ``flask-inputfilter`` with the dependencies needed 
for compilation by appending ``[compile]`` to the installation commands above.

_**Note:**_ If you do decide to recompile PQA binaries, you will need to install platform-specific `C/C++` build 
tools like [Visual Studio](https://visualstudio.microsoft.com/), [Xcode](https://developer.apple.com/xcode/) or 
[GNU Make](https://www.gnu.org/software/make/) _(non-exhaustive list)_.

A more detailed guide can be found [in the docs](https://leandercs.github.io/flask-inputfilter/guides/compile.html).


### Definition

```python
from flask_inputfilter import InputFilter
from flask_inputfilter.declarative import condition, field
from flask_inputfilter.conditions import ExactlyOneOfCondition
from flask_inputfilter.enums import RegexEnum
from flask_inputfilter.filters import StringTrimFilter, ToIntegerFilter, ToNullFilter
from flask_inputfilter.validators import IsIntegerValidator, IsStringValidator, RegexValidator

class UpdateZipcodeInputFilter(InputFilter):
    
    id: int = field(
        required=True,
        filters=[ToIntegerFilter(), ToNullFilter()],
        validators=[
            IsIntegerValidator()
        ]
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
        validators=[
            IsStringValidator()
        ]
    )

    condition(
        ExactlyOneOfCondition(['zipcode', 'city'])
    )
```


### Usage

To use the `InputFilter` class, call the `validate` method on the class instance.
After calling `validate`, the validated data will be available in `g.validated_data`.
If the data is invalid, a 400 response with an error message will be returned.

```python
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
```


## See also

For further instructions please view the [documentary](https://leandercs.github.io/flask-inputfilter).

For ideas, suggestions or questions, please open an issue on [GitHub](https://github.com/LeanderCS/flask-inputfilter).