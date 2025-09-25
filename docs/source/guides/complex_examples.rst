Complex Examples
================

This guide provides comprehensive examples for advanced flask-inputfilter usage patterns.

Nested Data Structures
-----------------------

Working with nested objects and arrays:

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.declarative import field
    from flask_inputfilter.filters import ToDataclassFilter, ArrayElementFilter
    from flask_inputfilter.validators import IsArrayValidator, IsDataclassValidator
    from dataclasses import dataclass
    from typing import List

    @dataclass
    class Address:
        street: str
        city: str
        postal_code: str

    @dataclass
    class ContactInfo:
        email: str
        phone: str

    class UserRegistrationFilter(InputFilter):
        # Basic user info
        username: str = field(
            required=True,
            filters=[StringTrimFilter()],
            validators=[LengthValidator(min_length=3, max_length=50)]
        )

        # Nested address object
        address: Address = field(
            required=True,
            filters=[ToDataclassFilter(Address)],
            validators=[IsDataclassValidator(Address)]
        )

        # Array of contact methods
        contacts: List[ContactInfo] = field(
            required=False,
            filters=[
                ArrayElementFilter(ToDataclassFilter(ContactInfo))
            ],
            validators=[
                IsArrayValidator(),
                ArrayLengthValidator(min_length=1, max_length=5)
            ],
            default=[]
        )

        # Tags as simple string array
        tags: List[str] = field(
            required=False,
            filters=[ArrayElementFilter(StringTrimFilter())],
            validators=[
                IsArrayValidator(),
                ArrayElementValidator(IsStringValidator())
            ],
            default=[]
        )

Multi-Step Validation
---------------------

Complex validation with multiple processing steps:

.. code-block:: python

    class PaymentProcessingFilter(InputFilter):
        # Credit card processing with multiple validation steps
        card_number: str = field(
            required=True,
            steps=[
                {
                    "filters": [StringTrimFilter(), ToDigitsFilter()],
                    "validators": [IsStringValidator()]
                },
                {
                    "filters": [],
                    "validators": [
                        LengthValidator(min_length=13, max_length=19),
                        CustomValidator(luhn_check)  # Custom Luhn algorithm
                    ]
                }
            ]
        )

        # Amount with currency conversion
        amount: float = field(
            required=True,
            steps=[
                {
                    "filters": [ToFloatFilter()],
                    "validators": [IsFloatValidator()]
                },
                {
                    "external_api": {
                        "url": "https://api.exchange.com/convert",
                        "method": "POST",
                        "params": {
                            "from": "{{currency}}",
                            "to": "USD",
                            "amount": "{{amount}}"
                        },
                        "data_key": "converted_amount"
                    }
                }
            ]
        )

        currency: str = field(
            required=True,
            filters=[ToUpperFilter()],
            validators=[InArrayValidator(['USD', 'EUR', 'GBP', 'JPY'])]
        )

External API Integration
------------------------

Complex external API workflows:

.. code-block:: python

    class UserVerificationFilter(InputFilter):
        email: str = field(
            required=True,
            filters=[StringTrimFilter(), ToLowerFilter()],
            validators=[IsEmailValidator()]
        )

        # Verify email exists and get user ID
        user_id: int = field(
            external_api={
                "url": "https://api.userservice.com/verify-email",
                "method": "POST",
                "data": {"email": "{{email}}"},
                "data_key": "user_id",
                "api_key": "your-api-key"
            },
            validators=[IsIntegerValidator()]
        )

        # Get user permissions based on user_id
        permissions: list = field(
            external_api={
                "url": "https://api.userservice.com/users/{{user_id}}/permissions",
                "method": "GET",
                "data_key": "permissions",
                "api_key": "your-api-key"
            },
            validators=[IsArrayValidator()],
            fallback=[]
        )

        # Conditional field based on permissions
        admin_notes: str = field(
            required=False,
            filters=[StringTrimFilter()],
            validators=[IsStringValidator()]
        )

        _conditions = [
            RequiredIfCondition(
                field='admin_notes',
                condition=lambda data: 'admin' in data.get('permissions', [])
            )
        ]

Complex Business Rules
----------------------

Advanced condition combinations:

.. code-block:: python

    from flask_inputfilter.conditions import (
        ExactlyOneOfCondition,
        RequiredIfCondition,
        CustomCondition
    )

    class OrderProcessingFilter(InputFilter):
        # Order type affects required fields
        order_type: str = field(
            required=True,
            validators=[InEnumValidator(OrderTypeEnum)]
        )

        # Shipping info (required for physical orders)
        shipping_address: dict = field(
            required=False,
            filters=[ToTypedDictFilter(AddressDict)],
            validators=[IsTypedDictValidator(AddressDict)]
        )

        # Digital delivery (required for digital orders)
        email: str = field(
            required=False,
            filters=[StringTrimFilter(), ToLowerFilter()],
            validators=[IsEmailValidator()]
        )

        # Payment method
        payment_method: str = field(
            required=True,
            validators=[InArrayValidator(['credit_card', 'paypal', 'bank_transfer'])]
        )

        # Credit card fields (conditional)
        card_number: str = field(required=False)
        card_expiry: str = field(required=False)
        card_cvv: str = field(required=False)

        # PayPal email (conditional)
        paypal_email: str = field(
            required=False,
            validators=[IsEmailValidator()]
        )

        # Bank details (conditional)
        bank_account: str = field(required=False)
        routing_number: str = field(required=False)

        # Complex business rules
        _conditions = [
            # Shipping required for physical orders
            RequiredIfCondition(
                field='shipping_address',
                condition=lambda data: data.get('order_type') == 'physical'
            ),

            # Email required for digital orders
            RequiredIfCondition(
                field='email',
                condition=lambda data: data.get('order_type') == 'digital'
            ),

            # Credit card fields required together
            CustomCondition(
                lambda data: (
                    data.get('payment_method') != 'credit_card' or
                    all(field in data and data[field] for field in
                        ['card_number', 'card_expiry', 'card_cvv'])
                ),
                "Credit card payment requires card number, expiry, and CVV"
            ),

            # PayPal email required for PayPal payment
            RequiredIfCondition(
                field='paypal_email',
                condition=lambda data: data.get('payment_method') == 'paypal'
            ),

            # Bank details required together for bank transfer
            CustomCondition(
                lambda data: (
                    data.get('payment_method') != 'bank_transfer' or
                    all(field in data and data[field] for field in
                        ['bank_account', 'routing_number'])
                ),
                "Bank transfer requires account and routing numbers"
            )
        ]

File Upload Validation
----------------------

Handling file uploads with validation:

.. code-block:: python

    class FileUploadFilter(InputFilter):
        # File metadata
        filename: str = field(
            required=True,
            filters=[StringTrimFilter()],
            validators=[
                RegexValidator(r'^[\w\-. ]+$', 'Invalid filename characters'),
                LengthValidator(max_length=255)
            ]
        )

        # File content as base64
        file_content: str = field(
            required=True,
            validators=[
                IsBase64ImageValidator(),
                IsBase64ImageCorrectSizeValidator(max_width=1920, max_height=1080)
            ],
            filters=[
                Base64ImageResizeFilter(max_width=800, max_height=600),
                Base64ImageDownscaleFilter(quality=85)
            ]
        )

        # File type validation
        file_type: str = field(
            required=True,
            filters=[ToLowerFilter()],
            validators=[InArrayValidator(['jpg', 'jpeg', 'png', 'gif', 'webp'])]
        )

        # Optional metadata
        alt_text: str = field(
            required=False,
            filters=[StringTrimFilter()],
            validators=[LengthValidator(max_length=500)]
        )

        tags: List[str] = field(
            required=False,
            filters=[ArrayElementFilter(StringTrimFilter())],
            validators=[
                IsArrayValidator(),
                ArrayLengthValidator(max_length=10)
            ],
            default=[]
        )

        # Ensure file type matches content
        _conditions = [
            CustomCondition(
                lambda data: validate_file_type_matches_content(
                    data.get('file_content'),
                    data.get('file_type')
                ),
                "File type does not match file content"
            )
        ]

API Pagination and Search
-------------------------

Common patterns for API endpoints:

.. code-block:: python

    class SearchFilter(InputFilter):
        # Search query
        q: str = field(
            required=False,
            filters=[StringTrimFilter()],
            validators=[LengthValidator(min_length=1, max_length=200)],
            default=""
        )

        # Pagination
        page: int = field(
            required=False,
            filters=[ToIntegerFilter()],
            validators=[RangeValidator(min_value=1, max_value=1000)],
            default=1
        )

        limit: int = field(
            required=False,
            filters=[ToIntegerFilter()],
            validators=[RangeValidator(min_value=1, max_value=100)],
            default=20
        )

        # Sorting
        sort_by: str = field(
            required=False,
            validators=[InArrayValidator(['name', 'date', 'popularity', 'price'])],
            default='name'
        )

        sort_order: str = field(
            required=False,
            filters=[ToLowerFilter()],
            validators=[InArrayValidator(['asc', 'desc'])],
            default='asc'
        )

        # Filters
        category: str = field(
            required=False,
            validators=[IsStringValidator()]
        )

        price_min: float = field(
            required=False,
            filters=[ToFloatFilter()],
            validators=[IsFloatValidator(), RangeValidator(min_value=0)]
        )

        price_max: float = field(
            required=False,
            filters=[ToFloatFilter()],
            validators=[IsFloatValidator(), RangeValidator(min_value=0)]
        )

        # Date range
        date_from: datetime = field(
            required=False,
            filters=[ToDateTimeFilter()],
            validators=[IsDateTimeValidator()]
        )

        date_to: datetime = field(
            required=False,
            filters=[ToDateTimeFilter()],
            validators=[IsDateTimeValidator()]
        )

        # Ensure price and date ranges are valid
        _conditions = [
            CustomCondition(
                lambda data: (
                    not all([data.get('price_min'), data.get('price_max')]) or
                    data.get('price_min') <= data.get('price_max')
                ),
                "Minimum price cannot be greater than maximum price"
            ),
            CustomCondition(
                lambda data: (
                    not all([data.get('date_from'), data.get('date_to')]) or
                    data.get('date_from') <= data.get('date_to')
                ),
                "Start date cannot be after end date"
            )
        ]

Model Deserialization
--------------------

Converting validated data to custom objects:

.. code-block:: python

    from dataclasses import dataclass
    from typing import Optional, List

    @dataclass
    class User:
        id: int
        username: str
        email: str
        profile: Optional['UserProfile'] = None
        settings: Optional['UserSettings'] = None

    @dataclass
    class UserProfile:
        first_name: str
        last_name: str
        bio: Optional[str] = None
        avatar_url: Optional[str] = None

    @dataclass
    class UserSettings:
        theme: str = "light"
        notifications_enabled: bool = True
        language: str = "en"

    class CreateUserFilter(InputFilter):
        username: str = field(
            required=True,
            filters=[StringTrimFilter()],
            validators=[
                LengthValidator(min_length=3, max_length=50),
                RegexValidator(r'^[a-zA-Z0-9_]+$', 'Username must be alphanumeric')
            ]
        )

        email: str = field(
            required=True,
            filters=[StringTrimFilter(), ToLowerFilter()],
            validators=[IsEmailValidator()]
        )

        # Nested profile data
        profile: UserProfile = field(
            required=False,
            filters=[ToDataclassFilter(UserProfile)],
            validators=[IsDataclassValidator(UserProfile)]
        )

        # Nested settings with defaults
        settings: UserSettings = field(
            required=False,
            filters=[ToDataclassFilter(UserSettings)],
            validators=[IsDataclassValidator(UserSettings)],
            default_factory=lambda: UserSettings()  # Default settings
        )

        # Set the model for automatic deserialization
        _model = User

    # Usage
    @app.route('/users', methods=['POST'])
    @CreateUserFilter.validate()
    def create_user():
        # g.validated_data is now a User instance
        user: User = g.validated_data

        # Access nested data safely
        full_name = f"{user.profile.first_name} {user.profile.last_name}" if user.profile else user.username

        return jsonify({
            "success": True,
            "user_id": user.id,
            "display_name": full_name,
            "theme": user.settings.theme if user.settings else "light"
        })