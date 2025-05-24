Filter
======

``Filters`` are used to filter the input data to a wanted format.

Overview
--------

Filters can be added into the ``add`` method for a specific field or as a global filter for all fields in ``add_global_filter``.

The global filters will be executed before the specific field filtering.

Example
-------

.. code-block:: python

    class TestInputFilter(InputFilter):
        def __init__(self):
            super().__init__()

            self.add(
                'username',
                required=True,
                filters=[StringTrimFilter()]
            )

            self.add(
                'name',
                required=True,
                filters=[StringTrimFilter()]
            )

            self.add_global_filter(ToLowerFilter())

Available Filters
-----------------

- `ArrayElementFilter <#flask_inputfilter.filters.ArrayElementFilter>`_
- `ArrayExplodeFilter <#flask_inputfilter.filters.ArrayExplodeFilter>`_
- `Base64ImageDownscaleFilter <#flask_inputfilter.filters.Base64ImageDownscaleFilter>`_
- `Base64ImageResizeFilter <#flask_inputfilter.filters.Base64ImageResizeFilter>`_
- `BlacklistFilter <#flask_inputfilter.filters.BlacklistFilter>`_
- `StringRemoveEmojisFilter <#flask_inputfilter.filters.StringRemoveEmojisFilter>`_
- `StringSlugifyFilter <#flask_inputfilter.filters.StringSlugifyFilter>`_
- `StringTrimFilter <#flask_inputfilter.filters.StringTrimFilter>`_
- `ToAlphaNumericFilter <#flask_inputfilter.filters.ToAlphaNumericFilter>`_
- `ToBooleanFilter <#flask_inputfilter.filters.ToBooleanFilter>`_
- `ToCamelCaseFilter <#flask_inputfilter.filters.ToCamelCaseFilter>`_
- `ToDataclassFilter <#flask_inputfilter.filters.ToDataclassFilter>`_
- `ToDateFilter <#flask_inputfilter.filters.ToDateFilter>`_
- `ToDateTimeFilter <#flask_inputfilter.filters.ToDateTimeFilter>`_
- `ToDigitsFilter <#flask_inputfilter.filters.ToDigitsFilter>`_
- `ToEnumFilter <#flask_inputfilter.filters.ToEnumFilter>`_
- `ToFloatFilter <#flask_inputfilter.filters.ToFloatFilter>`_
- `ToIntegerFilter <#flask_inputfilter.filters.ToIntegerFilter>`_
- `ToIsoFilter <#flask_inputfilter.filters.ToIsoFilter>`_
- `ToLowerFilter <#flask_inputfilter.filters.ToLowerFilter>`_
- `ToNormalizedUnicodeFilter <#flask_inputfilter.filters.ToNormalizedUnicodeFilter>`_
- `ToNullFilter <#flask_inputfilter.filters.ToNullFilter>`_
- `ToPascalCaseFilter <#flask_inputfilter.filters.ToPascalCaseFilter>`_
- `ToSnakeCaseFilter <#flask_inputfilter.filters.ToSnakeCaseFilter>`_
- `ToStringFilter <#flask_inputfilter.filters.ToStringFilter>`_
- `ToTypedDictFilter <#flask_inputfilter.filters.ToTypedDictFilter>`_
- `ToUpperFilter <#flask_inputfilter.filters.ToUpperFilter>`_
- `TruncateFilter <#flask_inputfilter.filters.TruncateFilter>`_
- `WhitelistFilter <#flask_inputfilter.filters.WhitelistFilter>`_
- `WhitespaceCollapseFilter <#flask_inputfilter.filters.WhitespaceCollapseFilter>`_

Base Filter
-----------

.. autoclass:: flask_inputfilter.filters.BaseFilter
   :members:
   :undoc-members:
   :show-inheritance:

Detailed Description
--------------------

.. automodule:: flask_inputfilter.filters
   :members:
   :undoc-members:
   :show-inheritance:
   :exclude-members: BaseFilter
