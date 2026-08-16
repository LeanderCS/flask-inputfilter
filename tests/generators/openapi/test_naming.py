import unittest

from flask_inputfilter.generators.openapi.naming import (
    to_input_filter_class_name,
    to_pascal_case,
)


class TestNaming(unittest.TestCase):
    def test_to_pascal_case_preserves_inner_case(self) -> None:
        self.assertEqual(to_pascal_case("createUser"), "CreateUser")
        self.assertEqual(to_pascal_case("create.user"), "CreateUser")

    def test_to_pascal_case_normalize(self) -> None:
        self.assertEqual(
            to_pascal_case("user-profile", normalize=True), "UserProfile"
        )

    def test_digit_leading_prefix(self) -> None:
        self.assertEqual(to_pascal_case("123foo"), "N123foo")
        self.assertEqual(
            to_input_filter_class_name("123foo"), "N123fooInputFilter"
        )

    def test_input_filter_class_name(self) -> None:
        self.assertEqual(
            to_input_filter_class_name("shipping_address"),
            "ShippingAddressInputFilter",
        )


if __name__ == "__main__":
    unittest.main()
