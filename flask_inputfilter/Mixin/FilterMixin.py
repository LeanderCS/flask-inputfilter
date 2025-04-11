from typing import Any, List

from typing_extensions import final

from flask_inputfilter.Filter import BaseFilter
from flask_inputfilter.Mixin import BaseMixin


class FilterMixin(BaseMixin):
    @final
    def addGlobalFilter(self, filter: BaseFilter) -> None:
        """
        Add a global filter to be applied to all fields.

        Args:
            filter: The filter to add.
        """
        self._global_filters.append(filter)

    @final
    def getGlobalFilters(self) -> List[BaseFilter]:
        """
        Retrieve all global filters associated with this InputFilter instance.

        This method returns a list of BaseFilter instances that have been
        added as global filters. These filters are applied universally to
        all fields during data processing.

        Returns:
            List[BaseFilter]: A list of global filters.
        """
        return self._global_filters

    def __applyFilters(self, filters: List[BaseFilter], value: Any) -> Any:
        """
        Apply filters to the field value.
        """
        if value is None:
            return value

        for filter_ in self._global_filters + filters:
            value = filter_.apply(value)

        return value
