import datetime
import unittest
from enum import Enum

from flask_inputfilter import InputFilter
from flask_inputfilter.conditions import ExactlyOneOfCondition
from flask_inputfilter.declarative import condition, field
from flask_inputfilter.enums import RegexEnum
from flask_inputfilter.filters import (
    StringTrimFilter,
    ToDateFilter,
    ToIntegerFilter,
)
from flask_inputfilter.generators.openapi import (
    to_openapi_components,
    to_openapi_schema,
)
from flask_inputfilter.validators import (
    ArrayElementValidator,
    ArrayLengthValidator,
    InArrayValidator,
    InEnumValidator,
    IsEmailValidator,
    IsIntegerValidator,
    IsStringValidator,
    LengthValidator,
    RangeValidator,
    RegexValidator,
)


class ColorEnum(Enum):
    RED = "red"
    GREEN = "green"


class TestSchemaExporterBasics(unittest.TestCase):
    def test_types_required_and_constraints(self) -> None:
        class UserInputFilter(InputFilter):
            name: str = field(
                required=True,
                validators=[
                    IsStringValidator(),
                    LengthValidator(min_length=1, max_length=50),
                ],
            )
            age: int = field(
                filters=[ToIntegerFilter()],
                validators=[
                    IsIntegerValidator(),
                    RangeValidator(min_value=0, max_value=120),
                ],
            )

        schema = to_openapi_schema(UserInputFilter)

        self.assertEqual(schema["type"], "object")
        self.assertEqual(schema["required"], ["name"])
        self.assertEqual(
            schema["properties"]["name"],
            {"type": "string", "minLength": 1, "maxLength": 50},
        )
        self.assertEqual(
            schema["properties"]["age"],
            {"type": "integer", "minimum": 0, "maximum": 120},
        )

    def test_format_detection_from_validator_and_pattern(self) -> None:
        class ContactInputFilter(InputFilter):
            email: str = field(validators=[IsEmailValidator()])
            other_email: str = field(
                validators=[RegexValidator(RegexEnum.EMAIL)]
            )
            code: str = field(validators=[RegexValidator(r"^[A-Z]{3}$")])

        schema = to_openapi_schema(ContactInputFilter)

        self.assertEqual(
            schema["properties"]["email"],
            {"type": "string", "format": "email"},
        )
        self.assertEqual(
            schema["properties"]["other_email"],
            {"type": "string", "format": "email"},
        )
        self.assertEqual(
            schema["properties"]["code"],
            {"type": "string", "pattern": "^[A-Z]{3}$"},
        )

    def test_enum_exports(self) -> None:
        class MyFilter(InputFilter):
            status: str = field(
                validators=[InArrayValidator(["active", "inactive"])]
            )
            color: str = field(validators=[InEnumValidator(ColorEnum)])

        schema = to_openapi_schema(MyFilter)

        self.assertEqual(
            schema["properties"]["status"]["enum"], ["active", "inactive"]
        )
        self.assertEqual(
            schema["properties"]["color"]["enum"], ["red", "green"]
        )

    def test_in_enum_exports_member_values_not_names(self) -> None:
        class StatusEnum(Enum):
            ACTIVE = "is_active"
            INACTIVE = "is_inactive"

        class MyFilter(InputFilter):
            status: str = field(validators=[InEnumValidator(StatusEnum)])

        schema = to_openapi_schema(MyFilter)
        self.assertEqual(
            schema["properties"]["status"]["enum"],
            ["is_active", "is_inactive"],
        )

    def test_array_with_element_validator(self) -> None:
        class MyFilter(InputFilter):
            tags: list = field(
                validators=[
                    ArrayElementValidator(element_filter=IsStringValidator()),
                    ArrayLengthValidator(min_length=1, max_length=5),
                ]
            )

        schema = to_openapi_schema(MyFilter)

        self.assertEqual(
            schema["properties"]["tags"],
            {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1,
                "maxItems": 5,
            },
        )

    def test_type_falls_back_to_annotation(self) -> None:
        class MyFilter(InputFilter):
            note: str = field(filters=[StringTrimFilter()])

        schema = to_openapi_schema(MyFilter)
        self.assertEqual(schema["properties"]["note"]["type"], "string")

    def test_default_serialization(self) -> None:
        class MyFilter(InputFilter):
            page: int = field(default=1, validators=[IsIntegerValidator()])
            since: datetime.date = field(
                default=datetime.date(2024, 1, 1), filters=[ToDateFilter()]
            )

        schema = to_openapi_schema(MyFilter)
        self.assertEqual(schema["properties"]["page"]["default"], 1)
        self.assertEqual(
            schema["properties"]["since"]["default"], "2024-01-01"
        )


class TestSchemaExporterNested(unittest.TestCase):
    def test_nested_inlined_in_bare_export(self) -> None:
        class AddressInputFilter(InputFilter):
            zipcode: str = field(required=True,
                                 validators=[IsStringValidator()])

        class UserInputFilter(InputFilter):
            address: dict = field(input_filter=AddressInputFilter)

        schema = to_openapi_schema(UserInputFilter)

        self.assertEqual(
            schema["properties"]["address"],
            {
                "type": "object",
                "properties": {"zipcode": {"type": "string"}},
                "required": ["zipcode"],
            },
        )

    def test_nested_referenced_in_components_export(self) -> None:
        class AddressInputFilter(InputFilter):
            zipcode: str = field(validators=[IsStringValidator()])

        class UserInputFilter(InputFilter):
            address: dict = field(input_filter=AddressInputFilter)

        document = to_openapi_components(UserInputFilter)
        schemas = document["components"]["schemas"]

        self.assertIn("User", schemas)
        self.assertIn("Address", schemas)
        self.assertEqual(
            schemas["User"]["properties"]["address"],
            {"$ref": "#/components/schemas/Address"},
        )


class TestSchemaExporterDegradation(unittest.TestCase):
    def test_unknown_validator_becomes_extension(self) -> None:
        from flask_inputfilter.validators import IsPortValidator

        class MyFilter(InputFilter):
            port: int = field(
                validators=[IsIntegerValidator(), IsPortValidator()]
            )

        schema = to_openapi_schema(MyFilter)
        self.assertEqual(schema["properties"]["port"]["type"], "integer")
        self.assertEqual(
            schema["properties"]["port"]["x-validators"],
            ["IsPortValidator"],
        )

    def test_computed_excluded_by_default(self) -> None:
        class MyFilter(InputFilter):
            name: str = field(validators=[IsStringValidator()])
            display: str = field(computed=lambda data: data["name"].upper())

        schema = to_openapi_schema(MyFilter)
        self.assertNotIn("display", schema["properties"])

        schema = to_openapi_schema(MyFilter, include_computed=True)
        self.assertTrue(schema["properties"]["display"]["x-computed"])

    def test_copy_and_conditions_become_extensions(self) -> None:
        class MyFilter(InputFilter):
            zipcode: str = field(validators=[IsStringValidator()])
            city: str = field(validators=[IsStringValidator()])
            zip_copy: str = field(copy="zipcode")

            condition(ExactlyOneOfCondition(["zipcode", "city"]))

        schema = to_openapi_schema(MyFilter)
        self.assertEqual(
            schema["properties"]["zip_copy"]["x-copied-from"], "zipcode"
        )
        self.assertEqual(len(schema["x-conditions"]), 1)
        self.assertIn("ExactlyOneOfCondition", schema["x-conditions"][0])

    def test_extensions_can_be_disabled(self) -> None:
        from flask_inputfilter.validators import IsPortValidator

        class MyFilter(InputFilter):
            port: int = field(validators=[IsPortValidator()])

        schema = to_openapi_schema(MyFilter, include_extensions=False)
        self.assertNotIn("x-validators", schema["properties"]["port"])


class TestRoundTrip(unittest.TestCase):
    def test_generated_code_exports_back_to_schema(self) -> None:
        import json

        from flask_inputfilter.generators.openapi import (
            generate_from_openapi,
        )

        spec = {
            "openapi": "3.0.0",
            "info": {"title": "t", "version": "1"},
            "components": {
                "schemas": {
                    "User": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "minLength": 2,
                                "maxLength": 30,
                            },
                            "email": {"type": "string", "format": "email"},
                            "age": {"type": "integer", "minimum": 0},
                            "role": {
                                "type": "string",
                                "enum": ["admin", "user"],
                            },
                        },
                        "required": ["name", "email"],
                    }
                }
            },
        }

        code = generate_from_openapi(
            openapi_content=json.dumps(spec), format="json"
        )
        namespace: dict = {}
        exec(compile(code, "<generated>", "exec"), namespace)  # noqa: S102

        schema = to_openapi_schema(namespace["UserInputFilter"])

        properties = schema["properties"]
        self.assertEqual(sorted(schema["required"]), ["email", "name"])
        self.assertEqual(properties["name"]["type"], "string")
        self.assertEqual(properties["name"]["minLength"], 2)
        self.assertEqual(properties["name"]["maxLength"], 30)
        self.assertEqual(properties["email"]["format"], "email")
        self.assertEqual(properties["age"]["type"], "integer")
        self.assertEqual(properties["age"]["minimum"], 0)
        self.assertEqual(properties["role"]["enum"], ["admin", "user"])


if __name__ == "__main__":
    unittest.main()


class TestSchemaExporterCycles(unittest.TestCase):
    def _tree_node_class(self):
        class TreeNode(InputFilter):
            name: str = field(validators=[IsStringValidator()])

            def __init__(self):
                super().__init__()
                import warnings

                with warnings.catch_warnings():
                    warnings.simplefilter("ignore", DeprecationWarning)
                    self.add("child")
                self.fields["child"].input_filter = TreeNode

        return TreeNode

    def test_self_referential_filter_in_components(self):
        TreeNode = self._tree_node_class()  # noqa: N806
        document = to_openapi_components(TreeNode)
        schemas = document["components"]["schemas"]
        self.assertEqual(
            schemas["TreeNode"]["properties"]["child"],
            {"$ref": "#/components/schemas/TreeNode"},
        )

    def test_self_referential_filter_in_bare_export(self):
        """Bare export inlines nested filters; a cycle must terminate
        with an x-circular-ref marker instead of RecursionError
        (regression)."""
        TreeNode = self._tree_node_class()  # noqa: N806
        schema = to_openapi_schema(TreeNode)
        self.assertEqual(
            schema["properties"]["child"],
            {"type": "object", "x-circular-ref": "TreeNode"},
        )

    def test_inline_nested_cycle_terminates(self):
        TreeNode = self._tree_node_class()  # noqa: N806
        document = to_openapi_components(TreeNode, inline_nested=True)
        schema = document["components"]["schemas"]["TreeNode"]
        self.assertIn("child", schema["properties"])
