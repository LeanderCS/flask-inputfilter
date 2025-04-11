from typing import Any, Dict

from typing_extensions import final

from flask_inputfilter.Mixin import BaseMixin


class DataMixin(BaseMixin):
    @final
    def setData(self, data: Dict[str, Any]) -> None:
        """
        Filters and sets the provided data into the object's internal
        storage, ensuring that only the specified fields are considered and
        their values are processed through defined filters.

        Parameters:
            data:
                The input dictionary containing key-value pairs where keys
                represent field names and values represent the associated
                data to be filtered and stored.
        """
        filtered_data = {}
        for field_name, field_value in data.items():
            if field_name in self._fields:
                filtered_data[field_name] = self._FilterMixin__applyFilters(
                    filters=self._fields[field_name].filters,
                    value=field_value,
                )
            else:
                filtered_data[field_name] = field_value

        self._data = filtered_data

    @final
    def getValue(self, name: str) -> Any:
        """
        This method retrieves a value associated with the provided name. It
        searches for the value based on the given identifier and returns the
        corresponding result. If no value is found, it typically returns a
        default or fallback output. The method aims to provide flexibility in
        retrieving data without explicitly specifying the details of the
        underlying implementation.

        Args:
            name: A string that represents the identifier for which the
                 corresponding value is being retrieved. It is used to perform
                 the lookup.

        Returns:
            Any: The retrieved value associated with the given name. The
                 specific type of this value is dependent on the
                 implementation and the data being accessed.
        """
        return self._validated_data.get(name)

    @final
    def getValues(self) -> Dict[str, Any]:
        """
        Retrieves a dictionary of key-value pairs from the current object.
        This method provides access to the internal state or configuration of
        the object in a dictionary format, where keys are strings and values
        can be of various types depending on the object's design.

        Returns:
            Dict[str, Any]: A dictionary containing string keys and their
                            corresponding values of any data type.
        """
        return self._validated_data

    @final
    def getRawValue(self, name: str) -> Any:
        """
        Fetches the raw value associated with the provided key.

        This method is used to retrieve the underlying value linked to the
        given key without applying any transformations or validations. It
        directly fetches the raw stored value and is typically used in
        scenarios where the raw data is needed for processing or debugging
        purposes.

        Args:
            name: The name of the key whose raw value is to be retrieved.

        Returns:
            Any: The raw value associated with the provided key.
        """
        return self._data.get(name) if name in self._data else None

    @final
    def getRawValues(self) -> Dict[str, Any]:
        """
        Retrieves raw values from a given source and returns them as a
        dictionary.

        This method is used to fetch and return unprocessed or raw data in
        the form of a dictionary where the keys are strings, representing
        the identifiers, and the values are of any data type.

        Returns:
            Dict[str, Any]: A dictionary containing the raw values retrieved.
               The keys are strings representing the identifiers, and the
               values can be of any type, depending on the source
               being accessed.
        """
        if not self._fields:
            return {}

        return {
            field: self._data[field]
            for field in self._fields
            if field in self._data
        }

    @final
    def getUnfilteredData(self) -> Dict[str, Any]:
        """
        Fetches unfiltered data from the data source.

        This method retrieves data without any filtering, processing, or
        manipulations applied. It is intended to provide raw data that has
        not been altered since being retrieved from its source. The usage
        of this method should be limited to scenarios where unprocessed data
        is required, as it does not perform any validations or checks.

        Returns:
            Dict[str, Any]: The unfiltered, raw data retrieved from the
                 data source. The return type may vary based on the
                 specific implementation of the data source.
        """
        return self._data

    @final
    def setUnfilteredData(self, data: Dict[str, Any]) -> None:
        """
        Sets unfiltered data for the current instance. This method assigns a
        given dictionary of data to the instance for further processing. It
        updates the internal state using the provided data.

        Parameters:
            data: A dictionary containing the unfiltered
                data to be associated with the instance.
        """
        self._data = data

    @final
    def hasUnknown(self) -> bool:
        """
        Checks whether any values in the current data do not have
        corresponding configurations in the defined fields.

        Returns:
            bool: True if there are any unknown fields; False otherwise.
        """
        if not self._data and self._fields:
            return True
        return any(
            field_name not in self._fields.keys()
            for field_name in self._data.keys()
        )
