# Condition

The `Condition` module contains the conditions that can be used to validate the input data.

## Conditions

The `addCondition` method is used to add a condition between fields.

```python

from flask_inputfilter import InputFilter
from flask_inputfilter.Condition import OneOfCondition
from flask_inputfilter.Filter import StringTrimFilter
from flask_inputfilter.Validator import IsStringValidator


class TestInputFilter(InputFilter):
    def __init__(self):
        super().__init__()

        self.add(
            'username',
            filters=[StringTrimFilter()],
            validators=[IsStringValidator()]
        )

        self.add(
            'name',
            filters=[StringTrimFilter()],
            validators=[IsStringValidator()]
        )

        self.addCondition(
            OneOfCondition(['id', 'name'])
        )

```

## Available conditions

The following conditions are available in the `Condition` module:

1. [`ArrayLengthEqualCondition`](ArrayLengthEqualCondition.py) - Validates that the length of the array is equal to the given value.
2. [`ArrayLongerThanCondition`](ArrayLongerThanCondition.py) - Validates that the length of the array is longer than the given value.
3. [`CustomCondition`](CustomCondition.py) - A custom condition that can be used to validate the input data.
4. [`EqualCondition`](EqualCondition.py) - Validates that the input is equal to the given value.
5. [`ExactlyNOfCondition`](ExactlyNOfCondition.py) - Validates that exactly `n` of the given conditions are true.
6. [`ExactlyNOfMatchesCondition`](ExactlyNOfMatchesCondition.py) - Validates that exactly `n` of the given matches are true.
7. [`ExactlyOneOfCondition`](ExactlyOneOfCondition.py) - Validates that exactly one of the given conditions is true.
8. [`ExactlyOneOfMatchesCondition`](ExactlyOneOfMatchesCondition.py) - Validates that exactly one of the given matches is true.
9. [`IntegerBiggerThanCondition`](IntegerBiggerThanCondition.py) - Validates that the integer is bigger than the given value.
10. [`NOfCondition`](NOfCondition.py) - Validates that at least `n` of the given conditions are true.
11. [`NOfMatchesCondition`](NOfMatchesCondition.py) - Validates that at least `n` of the given matches are true.
12. [`NotEqualCondition`](NotEqualCondition.py) - Validates that the input is not equal to the given value.
13. [`OneOfCondition`](OneOfCondition.py) - Validates that at least one of the given conditions is true.
14. [`OneOfMatchesCondition`](OneOfMatchesCondition.py) - Validates that at least one of the given matches is true.
15. [`RequiredIfCondition`](RequiredIfCondition.py) - Validates that the input is required if the given field has a specific value.
16. [`StringLongerThanCondition`](StringLongerThanCondition.py) - Validates that the string is longer than the given value.
17. [`TemporalOrderCondition`](TemporalOrderCondition.py) - Validates that the input is in correct temporal order.
