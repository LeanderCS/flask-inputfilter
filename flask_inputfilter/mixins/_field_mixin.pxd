cdef class FieldMixin:

    @staticmethod
    cdef object apply_filters(list filters, object value)
    @staticmethod
    cdef object validate_field(list validators, object fallback, object value)
    @staticmethod
    cdef object apply_steps(list steps, object fallback, object value)
    @staticmethod
    cdef void check_conditions(list conditions, dict validated_data) except *
    @staticmethod
    cdef object check_for_required(str field_name, bint required, object default, object fallback, object value)
