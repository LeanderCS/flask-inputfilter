Changelog
=========

All notable changes to this project will be documented in this file.

[0.6.2] - 2025-07-03
--------------------

Added
^^^^^
- Added IsImageValidator, ToBase64ImageFilter and ToImageFilter.


[0.6.1] - 2025-07-02
--------------------

Changed
^^^^^^^
- Fixed issue with ``__init__.py`` for compiled versions.


[0.6.0] - 2025-06-30
--------------------

Removed
^^^^^^^
- Removed deprecated camel case methods and properties.
- Removed deprecated subfolders.


[0.5.5] - 2025-06-30
--------------------

Changed
^^^^^^^
- Updated ``InputFilter`` to increase performance.
- Updated ``IsDataclassValidator`` to be more readable and maintainable.


[0.5.4] - 2025-05-24
--------------------

Added
^^^^^
- Added ``ArrayElementFilter`` to filter elements in an array against specific filter.

Changed
^^^^^^^
- Updated ``ArrayElementValidator`` to support validators directly.
- Updated ``IsDataclassValidator`` to also check against their types, including nested dataclasses, lists, and dictionaries.


[0.5.3] - 2025-04-28
--------------------

Changed
^^^^^^^
- Migrated methods from camel to snake case


[0.5.2] - 2025-04-27
--------------------

Changed
^^^^^^^
- Moved multiple internal methods to own ``FieldMixin``
  - ``applyFilters``
  - ``applySteps``
  - ``checkConditions``
  - ``checkForRequired``
  - ``validateField``


[0.5.1] - 2025-04-26
--------------------

Added
^^^^^
- Added .whl for musllinux_aarch64 to the release process.


[0.5.0] - 2025-04-26
--------------------

Changed
^^^^^^^
- Moved components to subfolders to improve readability and maintainability.
  The following components have been moved:
  - ``Condition`` => ``conditions``
  - ``Enum`` => ``enums``
  - ``Exception`` => ``exceptions``
  - ``Filter`` => ``filters``
  - ``Mixin`` => ``mixins``
  - ``Model`` => ``models``
  - ``Validator`` => ``validators``

  But the old import paths are still available for backward compatibility, but
  because the old path will be abandoned in the future, it is recommended
  to use the new paths.

- Renamed files into snake_case to follow the PEP8 standard.
  This requires a migration if you are importing the files directly.
  e.g. ``from flask_inputfilter.Filter import Base64ImageResizeFilter`` to
  ``from flask_inputfilter.filters.base64_image_resize_filter import Base64ImageResizeFilter``.

  If you are using the components through the module, you don't need to change anything.


[0.4.3a1] - 2025-04-26
----------------------

Added
^^^^^
- whl generation for linux too.


[0.4.2] - 2025-04-25
--------------------

Added
^^^^^
- whl generation for all major versions and envs.


[0.4.1] - 2025-04-24
--------------------

Changed
^^^^^^^
- Introduced first c++ vector in ``InputFilter`` to improve performance.
- Updated required ``cython`` version to 3.0 or higher for python 3.7 - 3.11.
- Moved static methods outside of pure InputFilter class.


[0.4.0] - 2025-04-20
--------------------

Added
^^^^^
- Added possibility to use ``cython`` for performance improvements.
  View :doc:`the guide <guides/compile>` for more information.


[0.4.0a2] - 2025-04-17
----------------------

Changed
^^^^^^^
- Added fallback for ``cython`` to use ``python`` if no c++ compiler is installed.
- super().__init__() is now **ONLY** optional, if you are using the cython version.


[0.4.0a1] - 2025-04-17
----------------------

Changed
^^^^^^^
- InputFilter now uses cython for performance improvements.
- Made super().__init__() call optional. You will only need to call it,
  if you are wanting to limit the allowed methods.


[0.3.1] - 2025-04-14
--------------------

Changed
^^^^^^^
- Updated error handling and changed broad ``Exception`` to specific errors.
- Smaller performance improvements


[0.3.0] - 2025-04-10
--------------------

Added
^^^^^
- ``IsDateTimeValidator``
- ``IsDateValidator``

Changed
^^^^^^^
- Updated ``IsTypedDictValidator` and ``IsDataclassValidator`` to require a specific model and
  checks if the input json is in the defined format.
- Introduced Mixins for parts of InputFilter

 - ``ConditionMixin``
 - ``DataMixin``
 - ``ErrorHandlingMixin``
 - ``ExternalApiMixin``
 - ``FieldMixin``
 - ``FilterMixin``
 - ``ModelMixin``
 - ``ValidationMixin``

Removed
^^^^^^^
- ``RemoveEmojisFilter``
- ``ToPascaleCaseFilter``
- ``SlugifyFilter``


[0.2.0] - 2025-04-07
--------------------

Added
^^^^^
- getErrorMessages

Changed
^^^^^^^
- Updated error handling: The first error for each field is now returned in a combined format,
  enabling more detailed and flexible error handling on the frontend. :doc:`Check it out <guides/frontend_validation>`
- Errors received through external_api request get logged.


[0.1.2] - 2025-03-29
--------------------

Added
^^^^^
- getConditions
- getGlobalFilters
- getGlobalValidators
- clear

Changed
^^^^^^^
- Fixed ``merge`` method to fit expected behavior.


[0.1.1] - 2025-03-29
--------------------

Changed
^^^^^^^
- Fixed unexpected message in error message of ``IsIntegerValidator``


[0.1.0] - 2025-03-26
--------------------

Added
^^^^^
- Multiple functions to allow a broader usage aside as decorator

 - getErrorMessage
 - getRawValue
 - getRawValues
 - getUnfilteredData
 - getValue
 - getValues
 - hasUnknown
 - isValid
 - merge
 - remove
 - replace
 - setData
 - setUnfilteredData

Removed
^^^^^^^
- IsMimeTypeValidator


[0.0.10] - 2025-03-06
---------------------

Added
^^^^^
- Added python 3.14 support.

Changed
^^^^^^^
- Use ``FieldModel`` for field definition. (Only internal change, no impact on usage)


[0.0.9.1] - 2025-02-09
----------------------

Changed
^^^^^^^
- Updated ``InputFilter`` to fix the issue with route params.


[0.0.9] - 2025-01-29
--------------------

Added
^^^^^
- New ``copy`` functionality to copy the value of another field. :doc:`Check it out <options/copy>`

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
- New ``condition`` functionality between fields. :doc:`Check it out <options/condition>`

Changed
^^^^^^^
- Switched ``external_api`` config from dict to class. :doc:`Check it out <options/external_api>`


[0.0.4] - 2025-01-09
--------------------

Added
^^^^^
- New external API functionality. :doc:`Check it out <options/external_api>`
