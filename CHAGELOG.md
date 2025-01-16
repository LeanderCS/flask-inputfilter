# Changelog

All notable changes to this project will be documented in this file.


# [0.0.7.1] - 2025-01-16

## Changed

- Updated setup.py to fix the issue with the missing subfolders.


# [0.0.7] - 2025-01-14

## Added

- Workflow to run tests on all supported python versions. [Check it out](.github/workflows/test_env.yaml)
- Added more test coverage for validators and filters.
- Added tracking of coverage in tests. [Check it out](https://coveralls.io/github/LeanderCS/flask-inputfilter)
- New functionality for global filters and validators in InputFilters.
- New functionality to define custom supported methods.

### Validator

- New `NotInArrayValidator` to check if a value is not in a list. [Check it out](flask_inputfilter/Validator/NotInArrayValidator.py)
- New `NotValidator` to invert the result of another validator. [Check it out](flask_inputfilter/Validator/NotValidator.py)


# [0.0.6] - 2025-01-12

## Added

- New date validators and filters.

## Removed

- Dropped support for Python 3.6.


# [0.0.5] - 2025-01-12

## Added

- New condition functionality between fields. [Check it out](flask_inputfilter/Condition/README.md)

## Changed

- Switched external_api config from dict to class. [Check it out](flask_inputfilter/Model/ExternalApiConfig.py)


# [0.0.4] - 2025-01-09

## Added

- New external api functionality. [Check it out](EXTERNAL_API.md)
