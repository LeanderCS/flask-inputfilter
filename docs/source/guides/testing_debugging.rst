Testing & Debugging
===================

This guide covers testing strategies, debugging techniques, and troubleshooting methods for flask-inputfilter implementations.

Unit Testing InputFilters
-------------------------

Basic Test Setup
~~~~~~~~~~~~~~~

Setting up tests for your InputFilter classes:

.. code-block:: python

    import pytest
    from flask import Flask, g
    from flask_inputfilter import InputFilter
    from flask_inputfilter.declarative import field
    from flask_inputfilter.filters import StringTrimFilter, ToIntegerFilter
    from flask_inputfilter.validators import IsEmailValidator, RangeValidator
    from flask_inputfilter.conditions import ExactlyOneOfCondition

    class UserRegistrationFilter(InputFilter):
        username: str = field(
            required=True,
            filters=[StringTrimFilter()],
            validators=[LengthValidator(min_length=3, max_length=20)]
        )

        email: str = field(
            required=True,
            filters=[StringTrimFilter()],
            validators=[IsEmailValidator()]
        )

        age: int = field(
            required=False,
            filters=[ToIntegerFilter()],
            validators=[RangeValidator(min_value=13, max_value=120)]
        )

        phone: str = field(required=False)

        _conditions = [
            ExactlyOneOfCondition(['email', 'phone'])
        ]

Testing Valid Input
~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class TestUserRegistrationFilter:
        def test_valid_input_with_email(self):
            """Test successful validation with email"""
            filter_instance = UserRegistrationFilter()
            valid_data = {
                'username': 'testuser',
                'email': 'test@example.com',
                'age': 25
            }

            filter_instance.set_data(valid_data)
            assert filter_instance.is_valid()

            validated_data = filter_instance.get_data()
            assert validated_data['username'] == 'testuser'
            assert validated_data['email'] == 'test@example.com'
            assert validated_data['age'] == 25

        def test_valid_input_with_phone(self):
            """Test successful validation with phone instead of email"""
            filter_instance = UserRegistrationFilter()
            valid_data = {
                'username': 'testuser',
                'phone': '+1234567890'
            }

            filter_instance.set_data(valid_data)
            assert filter_instance.is_valid()

        def test_filters_applied_correctly(self):
            """Test that filters are applied during validation"""
            filter_instance = UserRegistrationFilter()
            data_with_whitespace = {
                'username': '  testuser  ',
                'email': '  test@example.com  '
            }

            filter_instance.set_data(data_with_whitespace)
            assert filter_instance.is_valid()

            validated_data = filter_instance.get_data()
            # StringTrimFilter should remove whitespace
            assert validated_data['username'] == 'testuser'
            assert validated_data['email'] == 'test@example.com'

Testing Invalid Input
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    class TestUserRegistrationFilterErrors:
        def test_missing_required_fields(self):
            """Test validation fails when required fields are missing"""
            filter_instance = UserRegistrationFilter()
            filter_instance.set_data({})

            assert not filter_instance.is_valid()
            errors = filter_instance.get_errors()

            assert 'username' in errors
            assert 'required' in errors['username'].lower()

        def test_invalid_email_format(self):
            """Test validation fails for invalid email"""
            filter_instance = UserRegistrationFilter()
            filter_instance.set_data({
                'username': 'testuser',
                'email': 'invalid-email'
            })

            assert not filter_instance.is_valid()
            errors = filter_instance.get_errors()
            assert 'email' in errors

        def test_username_too_short(self):
            """Test validation fails for short username"""
            filter_instance = UserRegistrationFilter()
            filter_instance.set_data({
                'username': 'ab',  # Too short
                'email': 'test@example.com'
            })

            assert not filter_instance.is_valid()
            errors = filter_instance.get_errors()
            assert 'username' in errors

        def test_age_out_of_range(self):
            """Test validation fails for age outside valid range"""
            filter_instance = UserRegistrationFilter()
            filter_instance.set_data({
                'username': 'testuser',
                'email': 'test@example.com',
                'age': 150  # Too old
            })

            assert not filter_instance.is_valid()
            errors = filter_instance.get_errors()
            assert 'age' in errors

        def test_condition_validation_failure(self):
            """Test validation fails when conditions are not met"""
            filter_instance = UserRegistrationFilter()
            filter_instance.set_data({
                'username': 'testuser',
                # Neither email nor phone provided
            })

            assert not filter_instance.is_valid()
            errors = filter_instance.get_errors()
            assert '_condition' in errors

        def test_both_email_and_phone_provided(self):
            """Test ExactlyOneOf condition fails when both fields present"""
            filter_instance = UserRegistrationFilter()
            filter_instance.set_data({
                'username': 'testuser',
                'email': 'test@example.com',
                'phone': '+1234567890'  # Both email and phone
            })

            assert not filter_instance.is_valid()
            errors = filter_instance.get_errors()
            assert '_condition' in errors

Testing Edge Cases
~~~~~~~~~~~~~~~~~

.. code-block:: python

    class TestEdgeCases:
        def test_empty_string_handling(self):
            """Test how empty strings are handled"""
            filter_instance = UserRegistrationFilter()
            filter_instance.set_data({
                'username': '',
                'email': 'test@example.com'
            })

            assert not filter_instance.is_valid()
            errors = filter_instance.get_errors()
            assert 'username' in errors

        def test_none_value_handling(self):
            """Test how None values are handled"""
            filter_instance = UserRegistrationFilter()
            filter_instance.set_data({
                'username': 'testuser',
                'email': 'test@example.com',
                'age': None
            })

            # Should be valid as age is optional and None should be filtered
            assert filter_instance.is_valid()

        def test_type_conversion(self):
            """Test automatic type conversion by filters"""
            filter_instance = UserRegistrationFilter()
            filter_instance.set_data({
                'username': 'testuser',
                'email': 'test@example.com',
                'age': '25'  # String that should convert to int
            })

            assert filter_instance.is_valid()
            validated_data = filter_instance.get_data()
            assert isinstance(validated_data['age'], int)
            assert validated_data['age'] == 25

        def test_unicode_handling(self):
            """Test Unicode character handling"""
            filter_instance = UserRegistrationFilter()
            filter_instance.set_data({
                'username': 'tëstüser',
                'email': 'tëst@exämple.com'
            })

            # Should handle Unicode properly
            result = filter_instance.is_valid()
            if not result:
                errors = filter_instance.get_errors()
                print(f"Unicode test errors: {errors}")

        @pytest.mark.parametrize("invalid_username", [
            "ab",          # Too short
            "a" * 21,      # Too long
            "test user",   # Contains space (if regex validator added)
            "123",         # Only numbers (if regex validator added)
            "",            # Empty
        ])
        def test_invalid_usernames(self, invalid_username):
            """Parameterized test for various invalid usernames"""
            filter_instance = UserRegistrationFilter()
            filter_instance.set_data({
                'username': invalid_username,
                'email': 'test@example.com'
            })

            assert not filter_instance.is_valid()
            errors = filter_instance.get_errors()
            assert 'username' in errors

Integration Testing with Flask
------------------------------

Testing with Flask Routes
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import json
    import pytest
    from flask import Flask, g, jsonify

    def create_app():
        app = Flask(__name__)

        @app.route('/register', methods=['POST'])
        @UserRegistrationFilter.validate()
        def register():
            data = g.validated_data
            # Simulate user creation
            return jsonify({"success": True, "user_id": 123})

        return app

    @pytest.fixture
    def client():
        app = create_app()
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    class TestFlaskIntegration:
        def test_successful_registration(self, client):
            """Test successful user registration through API"""
            response = client.post('/register',
                json={
                    'username': 'testuser',
                    'email': 'test@example.com',
                    'age': 25
                }
            )

            assert response.status_code == 200
            data = response.get_json()
            assert data['success'] is True
            assert 'user_id' in data

        def test_validation_error_response(self, client):
            """Test API returns 400 for validation errors"""
            response = client.post('/register',
                json={
                    'username': 'ab',  # Too short
                    'email': 'invalid-email'
                }
            )

            assert response.status_code == 400
            data = response.get_json()
            assert 'username' in data
            assert 'email' in data

        def test_missing_data_handling(self, client):
            """Test API handles missing request data gracefully"""
            response = client.post('/register')  # No JSON data

            assert response.status_code == 400

        def test_malformed_json(self, client):
            """Test API handles malformed JSON"""
            response = client.post('/register',
                data='{"invalid": json}',
                content_type='application/json'
            )

            assert response.status_code == 400

Testing External API Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from unittest.mock import patch, Mock

    class ExternalApiFilter(InputFilter):
        user_id: int = field(required=True)

        user_status: str = field(
            external_api={
                "url": "https://api.example.com/users/{{user_id}}/status",
                "method": "GET",
                "data_key": "status"
            }
        )

    class TestExternalApiIntegration:
        @patch('requests.get')
        def test_successful_api_call(self, mock_get):
            """Test successful external API integration"""
            # Mock successful API response
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"status": "active"}
            mock_get.return_value = mock_response

            filter_instance = ExternalApiFilter()
            filter_instance.set_data({'user_id': 123})

            assert filter_instance.is_valid()
            validated_data = filter_instance.get_data()
            assert validated_data['user_status'] == 'active'

        @patch('requests.get')
        def test_api_error_handling(self, mock_get):
            """Test handling of API errors"""
            # Mock failed API response
            mock_response = Mock()
            mock_response.status_code = 404
            mock_get.return_value = mock_response

            filter_instance = ExternalApiFilter()
            filter_instance.set_data({'user_id': 123})

            assert not filter_instance.is_valid()
            errors = filter_instance.get_errors()
            assert 'user_status' in errors

Debugging Techniques
--------------------

Debug Mode and Logging
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import logging
    from flask_inputfilter import InputFilter

    # Enable debug logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    class DebugInputFilter(InputFilter):
        def __init__(self, debug=False):
            super().__init__()
            self.debug = debug

        def set_data(self, data):
            if self.debug:
                logger.debug(f"Input data: {data}")
            return super().set_data(data)

        def is_valid(self):
            result = super().is_valid()
            if self.debug:
                if not result:
                    errors = self.get_errors()
                    logger.debug(f"Validation failed with errors: {errors}")
                else:
                    logger.debug("Validation passed")
            return result

    # Usage
    filter_instance = DebugInputFilter(debug=True)

Step-by-Step Validation Tracing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def trace_validation_process(filter_class, input_data):
        """Debug helper to trace validation step-by-step"""
        print(f"\\n=== Tracing validation for {filter_class.__name__} ===")
        print(f"Input data: {input_data}")

        filter_instance = filter_class()
        filter_instance.set_data(input_data)

        # Get field definitions
        fields = filter_instance._get_fields()
        print(f"\\nDefined fields: {list(fields.keys())}")

        # Trace each field
        for field_name, field_config in fields.items():
            field_value = input_data.get(field_name)
            print(f"\\n--- Processing field '{field_name}' ---")
            print(f"  Input value: {field_value}")
            print(f"  Required: {field_config.get('required', False)}")

            # Apply filters
            if field_config.get('filters'):
                print(f"  Filters: {[f.__class__.__name__ for f in field_config['filters']]}")
                filtered_value = filter_instance._apply_filters(field_name, field_value)
                print(f"  After filters: {filtered_value}")
            else:
                filtered_value = field_value
                print("  No filters applied")

            # Apply validators
            if field_config.get('validators'):
                print(f"  Validators: {[v.__class__.__name__ for v in field_config['validators']]}")
                try:
                    filter_instance._validate_field(field_name, filtered_value)
                    print("  ✓ Validation passed")
                except Exception as e:
                    print(f"  ✗ Validation failed: {e}")
            else:
                print("  No validators defined")

        # Check conditions
        print(f"\\n--- Checking conditions ---")
        conditions = getattr(filter_instance, '_conditions', [])
        if conditions:
            print(f"Conditions: {[c.__class__.__name__ for c in conditions]}")
            try:
                filter_instance._validate_conditions()
                print("✓ All conditions passed")
            except Exception as e:
                print(f"✗ Condition failed: {e}")
        else:
            print("No conditions defined")

        # Final result
        is_valid = filter_instance.is_valid()
        print(f"\\n=== Final Result: {'VALID' if is_valid else 'INVALID'} ===")
        if not is_valid:
            print(f"Errors: {filter_instance.get_errors()}")

    # Usage
    trace_validation_process(UserRegistrationFilter, {
        'username': '  testuser  ',
        'email': 'invalid-email'
    })

Interactive Debugging with IPython
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # In your test or development environment
    from IPython import embed

    class InteractiveDebugFilter(InputFilter):
        def is_valid(self):
            result = super().is_valid()
            if not result:
                print("Validation failed. Starting interactive debugger...")
                print(f"Errors: {self.get_errors()}")
                print(f"Data: {self.get_data()}")
                embed()  # Start interactive shell
            return result

Performance Testing
-------------------

Load Testing Validation
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import time
    import statistics
    from concurrent.futures import ThreadPoolExecutor

    def performance_test_filter(filter_class, test_data_list, iterations=1000):
        """Test filter performance with multiple data sets"""

        def single_validation(data):
            start_time = time.perf_counter()
            filter_instance = filter_class()
            filter_instance.set_data(data)
            result = filter_instance.is_valid()
            end_time = time.perf_counter()
            return end_time - start_time, result

        # Sequential testing
        sequential_times = []
        for _ in range(iterations):
            for data in test_data_list:
                exec_time, _ = single_validation(data)
                sequential_times.append(exec_time)

        # Concurrent testing
        with ThreadPoolExecutor(max_workers=10) as executor:
            concurrent_times = []
            futures = []

            for _ in range(iterations):
                for data in test_data_list:
                    future = executor.submit(single_validation, data)
                    futures.append(future)

            for future in futures:
                exec_time, _ = future.result()
                concurrent_times.append(exec_time)

        print(f"Performance Test Results for {filter_class.__name__}:")
        print(f"Sequential - Avg: {statistics.mean(sequential_times):.6f}s, "
              f"Min: {min(sequential_times):.6f}s, "
              f"Max: {max(sequential_times):.6f}s")
        print(f"Concurrent - Avg: {statistics.mean(concurrent_times):.6f}s, "
              f"Min: {min(concurrent_times):.6f}s, "
              f"Max: {max(concurrent_times):.6f}s")

    # Usage
    test_data = [
        {'username': 'user1', 'email': 'user1@example.com'},
        {'username': 'user2', 'email': 'user2@example.com'},
        {'username': 'user3', 'email': 'user3@example.com'},
    ]

    performance_test_filter(UserRegistrationFilter, test_data)

Memory Usage Testing
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import psutil
    import os

    def memory_test_filter(filter_class, test_data, iterations=10000):
        """Test memory usage of filter validation"""
        process = psutil.Process(os.getpid())

        # Get initial memory usage
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Run many validations
        for _ in range(iterations):
            filter_instance = filter_class()
            filter_instance.set_data(test_data)
            filter_instance.is_valid()

        # Get final memory usage
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory

        print(f"Memory Test for {filter_class.__name__}:")
        print(f"Initial memory: {initial_memory:.2f} MB")
        print(f"Final memory: {final_memory:.2f} MB")
        print(f"Memory increase: {memory_increase:.2f} MB")
        print(f"Memory per validation: {(memory_increase / iterations) * 1024:.2f} KB")

Troubleshooting Common Issues
----------------------------

Filter Order Problems
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Problem: Filters applied in wrong order
    class ProblematicFilter(InputFilter):
        value: str = field(
            filters=[
                ToIntegerFilter(),  # This should be last
                StringTrimFilter()  # This should be first
            ]
        )

    # Solution: Correct filter order
    class CorrectedFilter(InputFilter):
        value: str = field(
            filters=[
                StringTrimFilter(),  # First: clean string
                ToIntegerFilter()    # Then: convert to integer
            ]
        )

Type Conversion Issues
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def debug_type_conversion():
        """Debug helper for type conversion issues"""

        class TypeTestFilter(InputFilter):
            number: int = field(
                filters=[ToIntegerFilter()],
                validators=[IsIntegerValidator()]
            )

        test_cases = [
            "123",      # Valid string number
            " 123 ",    # String with whitespace
            "123.45",   # Float as string
            "abc",      # Non-numeric string
            123,        # Already integer
            None,       # None value
            "",         # Empty string
        ]

        for test_value in test_cases:
            print(f"\\nTesting value: {repr(test_value)} (type: {type(test_value).__name__})")

            filter_instance = TypeTestFilter()
            filter_instance.set_data({'number': test_value})

            is_valid = filter_instance.is_valid()
            if is_valid:
                result = filter_instance.get_data()['number']
                print(f"  ✓ Valid - Result: {repr(result)} (type: {type(result).__name__})")
            else:
                errors = filter_instance.get_errors()
                print(f"  ✗ Invalid - Error: {errors.get('number', 'Unknown error')}")

Condition Logic Debugging
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    def debug_conditions(filter_class, test_data):
        """Debug condition evaluation"""
        filter_instance = filter_class()
        filter_instance.set_data(test_data)

        conditions = getattr(filter_instance, '_conditions', [])
        if not conditions:
            print("No conditions defined")
            return

        print(f"Testing {len(conditions)} conditions with data: {test_data}")

        for i, condition in enumerate(conditions):
            try:
                result = condition.check(test_data)
                print(f"Condition {i+1} ({condition.__class__.__name__}): {'✓ PASS' if result else '✗ FAIL'}")
            except Exception as e:
                print(f"Condition {i+1} ({condition.__class__.__name__}): ERROR - {e}")

    # Usage
    debug_conditions(UserRegistrationFilter, {
        'username': 'testuser',
        'email': 'test@example.com',
        'phone': '+1234567890'  # Both email and phone (should fail ExactlyOneOf)
    })

Best Practices for Testing
--------------------------

Test Organization
~~~~~~~~~~~~~~~~

.. code-block:: python

    # Organize tests by functionality
    class TestUserRegistrationFilter:
        """Main test class for user registration validation"""

        class TestValidInputs:
            """Test cases for valid inputs"""
            def test_minimum_valid_data(self): pass
            def test_complete_valid_data(self): pass

        class TestInvalidInputs:
            """Test cases for invalid inputs"""
            def test_missing_required_fields(self): pass
            def test_invalid_field_formats(self): pass

        class TestFilters:
            """Test filter behavior"""
            def test_string_trimming(self): pass
            def test_type_conversion(self): pass

        class TestValidators:
            """Test validator behavior"""
            def test_email_validation(self): pass
            def test_range_validation(self): pass

        class TestConditions:
            """Test condition logic"""
            def test_exactly_one_of_condition(self): pass

Test Data Management
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Use fixtures for reusable test data
    @pytest.fixture
    def valid_user_data():
        return {
            'username': 'testuser',
            'email': 'test@example.com',
            'age': 25
        }

    @pytest.fixture
    def invalid_user_data():
        return {
            'username': 'ab',  # Too short
            'email': 'invalid-email',
            'age': 150  # Too old
        }

    # Use parameterized tests for multiple scenarios
    @pytest.mark.parametrize("username,expected_valid", [
        ("validuser", True),
        ("ab", False),           # Too short
        ("a" * 21, False),       # Too long
        ("", False),             # Empty
        ("valid-user_123", True), # With allowed special chars
    ])
    def test_username_validation(self, username, expected_valid):
        filter_instance = UserRegistrationFilter()
        filter_instance.set_data({
            'username': username,
            'email': 'test@example.com'
        })

        assert filter_instance.is_valid() == expected_valid

Continuous Integration Testing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    # Example GitHub Actions workflow
    name: Test InputFilters

    on: [push, pull_request]

    jobs:
      test:
        runs-on: ubuntu-latest
        strategy:
          matrix:
            python-version: [3.8, 3.9, "3.10", "3.11"]

        steps:
        - uses: actions/checkout@v2
        - name: Set up Python ${{ matrix.python-version }}
          uses: actions/setup-python@v2
          with:
            python-version: ${{ matrix.python-version }}
        - name: Install dependencies
          run: |
            pip install flask-inputfilter pytest
        - name: Run tests
          run: |
            pytest tests/ -v --tb=short
        - name: Run performance tests
          run: |
            pytest tests/performance/ -v

Remember to:

1. **Test both success and failure cases**
2. **Use meaningful test names that describe what's being tested**
3. **Test edge cases and boundary conditions**
4. **Mock external dependencies**
5. **Test error messages for clarity**
6. **Include performance and memory tests for critical paths**
7. **Use debugging tools when validation behaves unexpectedly**
8. **Document known issues and their workarounds**