"""Tests for MutuallyExclusiveCondition."""

import pytest

from flask_inputfilter.conditions import MutuallyExclusiveCondition


class TestMutuallyExclusiveCondition:
    """Test cases for MutuallyExclusiveCondition."""
    
    def test_single_group_present(self):
        """Test that single group present passes validation."""
        condition = MutuallyExclusiveCondition([
            ['username', 'password'],
            ['api_key'],
            ['oauth_token']
        ])
        
        # Only username/password group
        assert condition.check({'username': 'user', 'password': 'pass'}) is True
        
        # Only api_key group
        assert condition.check({'api_key': 'key123'}) is True
        
        # Only oauth_token group
        assert condition.check({'oauth_token': 'token456'}) is True
    
    def test_multiple_groups_present(self):
        """Test that multiple groups present fails validation."""
        condition = MutuallyExclusiveCondition([
            ['username', 'password'],
            ['api_key']
        ])
        
        # Both groups present - should fail
        assert condition.check({
            'username': 'user',
            'password': 'pass',
            'api_key': 'key123'
        }) is False
    
    def test_no_groups_present(self):
        """Test behavior when no groups are present."""
        # Default: require one group
        condition_require = MutuallyExclusiveCondition(
            [['username', 'password'], ['api_key']],
            require_one=True,
            allow_none=False
        )
        assert condition_require.check({}) is False
        assert condition_require.check({'other_field': 'value'}) is False
        
        # Allow none
        condition_allow_none = MutuallyExclusiveCondition(
            [['username', 'password'], ['api_key']],
            require_one=False,
            allow_none=True
        )
        assert condition_allow_none.check({}) is True
        assert condition_allow_none.check({'other_field': 'value'}) is True
    
    def test_partial_group_present(self):
        """Test when only part of a group is present."""
        condition = MutuallyExclusiveCondition([
            ['username', 'password'],
            ['api_key']
        ])
        
        # Only username (partial group) - counts as group present
        assert condition.check({'username': 'user'}) is True
        
        # Only password (partial group) - counts as group present
        assert condition.check({'password': 'pass'}) is True
    
    def test_empty_string_handling(self):
        """Test that empty strings are handled correctly."""
        condition = MutuallyExclusiveCondition([
            ['username', 'password'],
            ['api_key']
        ])
        
        # Empty strings should not count as present
        assert condition.check({
            'username': '',
            'password': '',
            'api_key': 'valid_key'
        }) is True
        
        # Non-empty username with empty password
        assert condition.check({
            'username': 'user',
            'password': ''
        }) is True
    
    def test_none_value_handling(self):
        """Test that None values are handled correctly."""
        condition = MutuallyExclusiveCondition([
            ['field1', 'field2'],
            ['field3']
        ])
        
        # None values should not count as present
        assert condition.check({
            'field1': None,
            'field2': None,
            'field3': 'value'
        }) is True
        
        # Mixed None and values
        assert condition.check({
            'field1': 'value',
            'field2': None,
            'field3': None
        }) is True
    
    def test_custom_error_message(self):
        """Test custom error messages."""
        condition = MutuallyExclusiveCondition(
            [['username', 'password'], ['api_key']],
            custom_message="Please use either username/password OR API key, not both"
        )
        
        message = condition.get_error_message({
            'username': 'user',
            'password': 'pass',
            'api_key': 'key'
        })
        assert message == "Please use either username/password OR API key, not both"
    
    def test_error_message_generation(self):
        """Test automatic error message generation."""
        condition = MutuallyExclusiveCondition([
            ['username', 'password'],
            ['api_key'],
            ['oauth_token']
        ])
        
        # Multiple groups present
        message = condition.get_error_message({
            'username': 'user',
            'api_key': 'key'
        })
        assert "mutually exclusive" in message.lower()
        assert "Group" in message
        
        # No groups present (when required)
        condition_required = MutuallyExclusiveCondition(
            [['username', 'password'], ['api_key']],
            require_one=True
        )
        message = condition_required.get_error_message({})
        assert "at least one group" in message.lower()
    
    def test_complex_groups(self):
        """Test with complex group configurations."""
        condition = MutuallyExclusiveCondition([
            ['email', 'email_password', 'email_2fa'],
            ['phone', 'phone_code'],
            ['oauth_provider', 'oauth_token', 'oauth_refresh']
        ])
        
        # First group only
        assert condition.check({
            'email': 'user@example.com',
            'email_password': 'pass',
            'email_2fa': '123456'
        }) is True
        
        # Second group only
        assert condition.check({
            'phone': '+1234567890',
            'phone_code': '1234'
        }) is True
        
        # Mix of first and third group - should fail
        assert condition.check({
            'email': 'user@example.com',
            'oauth_provider': 'google',
            'oauth_token': 'token'
        }) is False
    
    def test_non_dict_input(self):
        """Test handling of non-dictionary input."""
        condition = MutuallyExclusiveCondition([['field1'], ['field2']])
        
        # Non-dict input should return False
        assert condition.check(None) is False
        assert condition.check([]) is False
        assert condition.check("string") is False
        assert condition.check(123) is False
    
    def test_single_field_groups(self):
        """Test with single-field groups."""
        condition = MutuallyExclusiveCondition([
            ['method1'],
            ['method2'],
            ['method3']
        ])
        
        # Only one method
        assert condition.check({'method1': 'value'}) is True
        assert condition.check({'method2': 'value'}) is True
        
        # Multiple methods - should fail
        assert condition.check({
            'method1': 'value1',
            'method2': 'value2'
        }) is False
    
    def test_edge_cases(self):
        """Test edge cases."""
        # Empty groups list
        condition_empty = MutuallyExclusiveCondition([])
        assert condition_empty.check({}) is True
        
        # Single group
        condition_single = MutuallyExclusiveCondition([['field1', 'field2']])
        assert condition_single.check({'field1': 'value'}) is True
        assert condition_single.check({}) is False  # If require_one=True
        
        # Groups with overlapping field names (shouldn't happen but test anyway)
        condition_overlap = MutuallyExclusiveCondition([
            ['field1', 'field2'],
            ['field2', 'field3']  # field2 in both groups
        ])
        # If field2 is present, both groups are considered present
        assert condition_overlap.check({'field2': 'value'}) is False