Changelog
=========

All notable changes to this project will be documented in this file.

[0.0.9] - 2025-01-29
--------------------

Added
^^^^^
- New ``copy`` functionality to copy the value of another field. `Check it out <options/copy>`_

Filter
""""""
- New ``ToDataclassFilter`` to convert a dictionary to a dataclass.
- New ``ToTypedDictFilter`` to convert a dictionary to a TypedDict.

Validator
"""""""""
- New ``CustomJsonValidator`` to check if a value is the format of a specific json.
- New ``IsDataclassValidator`` to check if a value is a dataclass.
- New ``IsTypedDictValidator`` to check if a value is a TypedDict.

Changed
^^^^^^^
- Moved external API call before the filter and validation process.
  Before, filters and validators the the external API field where useless,
  because the value of the field where replaced by the API result.
- Updated ``SlugifyFilter`` to remove accents and other special characters.


[0.0.8] - 2025-01-20
--------------------

Added
^^^^^
- New functionality to define steps for a field to have more control over the
  order of the validation and filtering process.
- Documentary

Filter
""""""
- New ``Base64ImageDownscaleFilter`` to reduce the size of an image.
- New ``Base64ImageResizeFilter`` to reduce the file size of an image.

Validator
"""""""""
- New ``IsHorizontalImageValidator`` to check if an image is horizontal.
- New ``IsVerticalImageValidator`` to check if an image is vertical.

Changed
^^^^^^^
- Added ``UnicodeFormEnum`` to show possible config values for ``ToNormalizedUnicodeFilter``.
  Old config is still supported, but will be removed in a later version.


[0.0.7.1] - 2025-01-16
----------------------

Changed
^^^^^^^
- Updated ``setup.py`` to fix the issue with the missing subfolders.


[0.0.7] - 2025-01-14
--------------------

Added
^^^^^
- Workflow to run tests on all supported Python versions.
- Added more test coverage for validators and filters.
- Added tracking of coverage in tests. `Check it out <https://coveralls.io/github/LeanderCS/flask-inputfilter>`_
- New functionality for global filters and validators in ``InputFilters``.
- New functionality to define custom supported methods.

Validator
"""""""""
- New ``NotInArrayValidator`` to check if a value is not in a list.
- New ``NotValidator`` to invert the result of another validator.


[0.0.6] - 2025-01-12
--------------------

Added
^^^^^
- New date validators and filters.

Removed
^^^^^^^
- Dropped support for Python 3.6.


[0.0.5] - 2025-01-12
--------------------

Added
^^^^^
- New ``condition`` functionality between fields. `Check it out <options/condition>`_

Changed
^^^^^^^
- Switched ``external_api`` config from dict to class. `Check it out <options/external_api#Configuration>`_


[0.0.4] - 2025-01-09
--------------------

Added
^^^^^
- New external API functionality. `Check it out <options/external_api>`_
