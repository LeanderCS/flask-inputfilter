import unittest

from flask_inputfilter.generators.openapi import generate_from_openapi
from flask_inputfilter.generators.openapi.endpoint_generator import (
    EndpointCodeGenerator,
)
from flask_inputfilter.generators.openapi.parser import (
    EndpointSpec,
    OpenAPIParser,
)

OPENAPI_SPEC = {
    "openapi": "3.0.0",
    "info": {"title": "Test API", "version": "1.0.0"},
    "paths": {
        "/users": {
            "post": {
                "operationId": "createUser",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/User"}
                        }
                    }
                },
            },
            "get": {
                "parameters": [
                    {
                        "name": "limit",
                        "in": "query",
                        "required": False,
                        "schema": {"type": "integer", "minimum": 1},
                    }
                ]
            },
        },
        "/users/{id}/orders": {
            "parameters": [
                {
                    "name": "id",
                    "in": "path",
                    "required": True,
                    "schema": {"type": "integer"},
                }
            ],
            "post": {
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "item": {"type": "string"},
                                    "amount": {
                                        "type": "integer",
                                        "minimum": 1,
                                    },
                                },
                                "required": ["item"],
                            }
                        }
                    }
                }
            },
        },
    },
    "components": {
        "schemas": {
            "User": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "minLength": 1},
                    "email": {"type": "string", "format": "email"},
                },
                "required": ["name"],
            }
        }
    },
}


class TestExtractEndpoints(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = OpenAPIParser(openapi_content=OPENAPI_SPEC)

    def test_extracts_all_endpoints(self) -> None:
        endpoints = self.parser.extract_endpoints()
        self.assertEqual(len(endpoints), 3)

        keys = {(e.path, e.method) for e in endpoints}
        self.assertEqual(
            keys,
            {
                ("/users", "post"),
                ("/users", "get"),
                ("/users/{id}/orders", "post"),
            },
        )

    def test_operation_id_captured(self) -> None:
        endpoints = {
            (e.path, e.method): e for e in self.parser.extract_endpoints()
        }
        self.assertEqual(
            endpoints[("/users", "post")].operation_id, "createUser"
        )
        self.assertIsNone(endpoints[("/users", "get")].operation_id)

    def test_path_level_parameters_merged(self) -> None:
        endpoints = {
            (e.path, e.method): e for e in self.parser.extract_endpoints()
        }
        parameters = endpoints[("/users/{id}/orders", "post")].parameters
        self.assertEqual(len(parameters), 1)
        self.assertEqual(parameters[0]["name"], "id")

    def test_request_body_schema_keeps_ref(self) -> None:
        endpoints = {
            (e.path, e.method): e for e in self.parser.extract_endpoints()
        }
        body = endpoints[("/users", "post")].request_body_schema
        self.assertEqual(body, {"$ref": "#/components/schemas/User"})


class TestEndpointClassNaming(unittest.TestCase):
    def setUp(self) -> None:
        parser = OpenAPIParser(openapi_content=OPENAPI_SPEC)
        self.generator = EndpointCodeGenerator(parser=parser)

    def test_operation_id_naming(self) -> None:
        endpoint = EndpointSpec(
            path="/users", method="post", operation_id="createUser"
        )
        self.assertEqual(
            self.generator.class_name_for(endpoint), "CreateUserInputFilter"
        )

    def test_fallback_naming_from_path(self) -> None:
        endpoint = EndpointSpec(path="/users/{id}/orders", method="post")
        self.assertEqual(
            self.generator.class_name_for(endpoint),
            "PostUsersIdOrdersInputFilter",
        )

    def test_collision_gets_suffix(self) -> None:
        endpoint = EndpointSpec(
            path="/users", method="post", operation_id="createUser"
        )
        first = self.generator.class_name_for(endpoint)
        second = self.generator.class_name_for(endpoint)
        self.assertEqual(first, "CreateUserInputFilter")
        self.assertEqual(second, "CreateUser2InputFilter")

    def test_operation_id_with_dots_is_valid_identifier(self) -> None:
        endpoint = EndpointSpec(
            path="/users", method="post", operation_id="create.user"
        )
        class_name = self.generator.class_name_for(endpoint)
        self.assertEqual(class_name, "CreateUserInputFilter")
        self.assertTrue(class_name.isidentifier())

    def test_digit_leading_operation_id_is_valid_identifier(self) -> None:
        endpoint = EndpointSpec(
            path="/users", method="post", operation_id="123create"
        )
        class_name = self.generator.class_name_for(endpoint)
        self.assertEqual(class_name, "N123createInputFilter")
        self.assertTrue(class_name.isidentifier())


class TestEndpointCodeGeneration(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = OpenAPIParser(openapi_content=OPENAPI_SPEC)
        self.generator = EndpointCodeGenerator(parser=self.parser)

    def _endpoint(self, path: str, method: str) -> EndpointSpec:
        return next(
            e
            for e in self.parser.extract_endpoints()
            if e.path == path and e.method == method
        )

    def test_ref_body_becomes_subclass_of_component(self) -> None:
        code = self.generator.generate_endpoint_class(
            self._endpoint("/users", "post"), {"UserInputFilter"}
        )
        self.assertIn(
            "class CreateUserInputFilter(UserInputFilter):", code
        )

    def test_ref_body_inlined_without_component(self) -> None:
        code = self.generator.generate_endpoint_class(
            self._endpoint("/users", "post"), set()
        )
        self.assertIn("class CreateUserInputFilter(InputFilter):", code)
        self.assertIn("name: str = field(", code)
        self.assertIn("email: str = field(", code)

    def test_path_param_is_required(self) -> None:
        code = self.generator.generate_endpoint_class(
            self._endpoint("/users/{id}/orders", "post"), set()
        )
        self.assertIn("class PostUsersIdOrdersInputFilter", code)
        self.assertIn("item: str = field(", code)
        self.assertIn("id: int = field(", code)

        # The path parameter must be required.
        id_block = code.split("id: int = field(")[1]
        self.assertIn("required=True", id_block)

    def test_query_param_type_mapping(self) -> None:
        code = self.generator.generate_endpoint_class(
            self._endpoint("/users", "get"), set()
        )
        self.assertIn("limit: int = field(", code)
        self.assertIn("ToIntegerFilter()", code)


class TestGenerateFromOpenapiEndpoints(unittest.TestCase):
    def test_include_endpoints(self) -> None:
        import json

        code = generate_from_openapi(
            openapi_content=json.dumps(OPENAPI_SPEC),
            format="json",
            include_endpoints=True,
        )

        # Components come before endpoint classes.
        self.assertIn("class UserInputFilter(InputFilter):", code)
        self.assertIn(
            "class CreateUserInputFilter(UserInputFilter):", code
        )
        self.assertLess(
            code.index("class UserInputFilter"),
            code.index("class CreateUserInputFilter"),
        )

        self._assert_code_executes(code)

    def test_endpoints_only(self) -> None:
        import json

        code = generate_from_openapi(
            openapi_content=json.dumps(OPENAPI_SPEC),
            format="json",
            endpoints_only=True,
        )

        self.assertNotIn("class UserInputFilter(InputFilter):", code)
        self.assertIn("class CreateUserInputFilter(InputFilter):", code)

        self._assert_code_executes(code)

    def test_path_and_method_filter(self) -> None:
        import json

        code = generate_from_openapi(
            openapi_content=json.dumps(OPENAPI_SPEC),
            format="json",
            endpoints_only=True,
            path="/users",
            method="GET",
        )

        self.assertIn("class GetUsersInputFilter(InputFilter):", code)
        self.assertNotIn("CreateUserInputFilter", code)

    def _assert_code_executes(self, code: str) -> None:
        """Generated code must compile, exec and validate sample data."""
        namespace: dict = {}
        exec(compile(code, "<generated>", "exec"), namespace)  # noqa: S102

        create_user = namespace["CreateUserInputFilter"]()
        validated = create_user.validate_data(
            {"name": "John", "email": "john@example.com"}
        )
        self.assertEqual(validated["name"], "John")

        from flask_inputfilter.exceptions import ValidationError

        with self.assertRaises(ValidationError):
            namespace["CreateUserInputFilter"]().validate_data(
                {"email": "john@example.com"}
            )


if __name__ == "__main__":
    unittest.main()
