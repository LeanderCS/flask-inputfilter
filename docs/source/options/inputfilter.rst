InputFilter
===========

Overview
--------

.. autoclass:: flask_inputfilter.input_filter.InputFilter
   :members:
   :undoc-members:
   :show-inheritance:

Configuration
-------------

The ``add`` method supports several options:

- `Name`_
- `Required`_
- `Filters`_
- `Validators`_
- `Default`_
- `Fallback`_
- `Steps`_
- `ExternalApi`_
- `Copy`_

Name
~~~~

The ``name`` option specifies the name of the field.
This is the key that will be used to access the field value in the validated data.

Required
~~~~~~~~

The ``required`` option specifies whether the field must be included in the input data.
If the field is missing, a ``ValidationError`` will be raised with an appropriate error message.

Filters
~~~~~~~

The ``filters`` option allows you to specify one or more filters to apply to the field value.
Filters are applied in the order they are defined.

For more information view the :doc:`Filter <filter>` documentation.

Validators
~~~~~~~~~~

The ``validators`` option allows you to specify one or more validators to apply to the field value.
Validators are applied in the order they are defined.

For more information view the :doc:`Validator <validator>` documentation.

Default
~~~~~~~

The ``default`` option allows you to specify a default value to use if the field is not
present in the input data.

Fallback
~~~~~~~~

The ``fallback`` option specifies a value to use if validation fails or required data
is missing. Note that if the field is optional and absent, ``fallback`` will not apply;
use ``default`` in such cases.

Steps
~~~~~

The ``steps`` option allows you to specify a list of different filters and validator to apply to the field value.
It respects the order of the list.

ExternalApi
~~~~~~~~~~~

The ``external_api`` option allows you to specify an external API to call for the field value.
The API call is made when the field is validated, and the response is used as the field value.

For more information view the :doc:`ExternalApi <external_api>` documentation.

Copy
~~~~

The ``copy`` option allows you to copy the value of another field.
The copied value can be filtered and validated, due to the coping being executed first.

For more information view the :doc:`Copy <copy>` documentation.


Examples
--------

Least config


Full config
