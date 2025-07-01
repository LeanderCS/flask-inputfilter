cdef class FieldMixin:

    @staticmethod
    cdef object apply_filters(list filters1, list filters2, object value)
    @staticmethod
    cdef object validate_field(list validators1, list validators2, object fallback, object value)
    @staticmethod
    cdef object apply_steps(list steps, object fallback, object value)
    @staticmethod
    cdef void check_conditions(list conditions, dict validated_data) except *
    @staticmethod
    cdef object check_for_required(str field_name, object field_info, object value)
    @staticmethod
    cdef tuple validate_fields(
            dict fields,
            dict data,
            list global_filters,
            list global_validators
    )
    @staticmethod
    cdef object get_field_value(str field_name, object field_info, dict data, dict validated_data)
