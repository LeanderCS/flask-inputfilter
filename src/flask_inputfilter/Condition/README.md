# Condition

The `Condition` module contains the conditions that can be used to validate the input data.

## Conditions

The `addCondition` method is used to add a condition between fields.

```python
from flask_inputfilter import InputFilter
from flask_inputfilter.Condition import ExactlyOneOfCondition
from flask_inputfilter.Filter import ToIntegerFilter
from flask_inputfilter.Validator import IsIntegerValidator

class TestInputFilter(InputFilter):
    def __init__(self):
        super().__init__()

        self.add(
            'id',
            required=True,
            filters=[ToIntegerFilter()],
            validators=[IsIntegerValidator()]
        )

        self.add(
            'name',
            required=True
        )

        self.addCondition(
            ExactlyOneOfCondition('id', 'name')
        )
```

## Available conditions

The following conditions are available in the `Condition` module:

1. [`CustomCondition`](CustomCondition.py) - A custom condition that can be used to validate the input data.
2. [`EqualCondition`](EqualCondition.py) - Validates that the input is equal to the given value.
3. [`ExactlyNOfCondition`](ExactlyNOfCondition.py) - Validates that exactly `n` of the given conditions are true.
4. [`ExactlyNOfMatchesCondition`](ExactlyNOfMatchesCondition.py) - Validates that exactly `n` of the given matches are true.
5. [`ExactlyOneOfCondition`](ExactlyOneOfCondition.py) - Validates that exactly one of the given conditions is true.
6. [`ExactlyOneOfMatchesCondition`](ExactlyOneOfMatchesCondition.py) - Validates that exactly one of the given matches is true.
7. [`IntegerBiggerThanCondition`](IntegerBiggerThanCondition.py) - Validates that the integer is bigger than the given value.
8. [`NOfCondition`](NOfCondition.py) - Validates that at least `n` of the given conditions are true.
9. [`NOfMatchesCondition`](NOfMatchesCondition.py) - Validates that at least `n` of the given matches are true.
10. [`NotEqualCondition`](NotEqualCondition.py) - Validates that the input is not equal to the given value.
11. [`OneOfCondition`](OneOfCondition.py) - Validates that at least one of the given conditions is true.
12. [`OneOfMatchesCondition`](OneOfMatchesCondition.py) - Validates that at least one of the given matches is true.
13. [`RequiredIfCondition`](RequiredIfCondition.py) - Validates that the input is required if the given condition is true.
14. [`StringLongerThanCondition`](StringLongerThanCondition.py) - Validates that the string is longer than the given value.
15. [`TemporalOrderCondition`](TemporalOrderCondition.py) - Validates that the input is a temporal value.
