Cookbook & Recipes
==================

This cookbook contains ready-to-use recipes for common validation scenarios. Each recipe includes complete working examples that you can copy and adapt to your needs.

User Authentication & Registration
----------------------------------

User Registration
~~~~~~~~~~~~~~~~~

Complete user registration with password confirmation and terms acceptance:

.. code-block:: python

    from flask_inputfilter import InputFilter
    from flask_inputfilter.declarative import field
    from flask_inputfilter.conditions import EqualCondition
    from flask_inputfilter.filters import StringTrimFilter, ToLowerFilter
    from flask_inputfilter.validators import (
        IsEmailValidator, LengthValidator, RegexValidator, IsBooleanValidator
    )

    class UserRegistrationFilter(InputFilter):
        username: str = field(
            required=True,
            filters=[StringTrimFilter()],
            validators=[
                LengthValidator(min_length=3, max_length=30),
                RegexValidator(
                    pattern=r'^[a-zA-Z0-9_]+$',
                    error_message="Username can only contain letters, numbers, and underscores"
                )
            ]
        )

        email: str = field(
            required=True,
            filters=[StringTrimFilter(), ToLowerFilter()],
            validators=[IsEmailValidator()]
        )

        password: str = field(
            required=True,
            validators=[
                LengthValidator(
                    min_length=8,
                    error_message="Password must be at least 8 characters long"
                ),
                RegexValidator(
                    pattern=r'(?=.*[A-Z])',
                    error_message="Password must contain at least one uppercase letter"
                ),
                RegexValidator(
                    pattern=r'(?=.*[a-z])',
                    error_message="Password must contain at least one lowercase letter"
                ),
                RegexValidator(
                    pattern=r'(?=.*[0-9])',
                    error_message="Password must contain at least one number"
                )
            ]
        )

        password_confirmation: str = field(
            required=True,
            validators=[IsStringValidator()]
        )

        terms_accepted: bool = field(
            required=True,
            validators=[
                IsBooleanValidator(),
                CustomValidator(
                    lambda value: value is True,
                    error_message="You must accept the terms and conditions"
                )
            ]
        )

        newsletter_signup: bool = field(
            required=False,
            default=False,
            validators=[IsBooleanValidator()]
        )

        _conditions = [
            EqualCondition(
                'password',
                'password_confirmation',
                error_message="Password confirmation must match password"
            )
        ]

Login with Email or Username
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Allow users to login with either email or username:

.. code-block:: python

    from flask_inputfilter.conditions import ExactlyOneOfCondition, CustomCondition

    class LoginFilter(InputFilter):
        email: str = field(
            required=False,
            filters=[StringTrimFilter(), ToLowerFilter()],
            validators=[IsEmailValidator()]
        )

        username: str = field(
            required=False,
            filters=[StringTrimFilter()],
            validators=[
                LengthValidator(min_length=3, max_length=30),
                RegexValidator(r'^[a-zA-Z0-9_]+$')
            ]
        )

        password: str = field(
            required=True,
            validators=[LengthValidator(min_length=1)]
        )

        remember_me: bool = field(
            required=False,
            default=False,
            validators=[IsBooleanValidator()]
        )

        _conditions = [
            ExactlyOneOfCondition(
                fields=['email', 'username'],
                error_message="Please provide either email or username"
            )
        ]

E-commerce & Shopping
--------------------

Product Creation
~~~~~~~~~~~~~~~

Complete product creation with categories, pricing, and inventory:

.. code-block:: python

    from decimal import Decimal
    from flask_inputfilter.filters import ToFloatFilter, ArrayElementFilter
    from flask_inputfilter.validators import (
        IsFloatValidator, RangeValidator, IsArrayValidator, InArrayValidator
    )

    class ProductFilter(InputFilter):
        name: str = field(
            required=True,
            filters=[StringTrimFilter()],
            validators=[
                LengthValidator(min_length=3, max_length=200),
                RegexValidator(
                    pattern=r'^[a-zA-Z0-9\s\-_.,()]+$',
                    error_message="Product name contains invalid characters"
                )
            ]
        )

        description: str = field(
            required=True,
            filters=[StringTrimFilter()],
            validators=[
                LengthValidator(min_length=10, max_length=2000)
            ]
        )

        price: float = field(
            required=True,
            filters=[ToFloatFilter()],
            validators=[
                IsFloatValidator(),
                RangeValidator(min_value=0.01, max_value=999999.99)
            ]
        )

        compare_at_price: float = field(
            required=False,
            filters=[ToFloatFilter()],
            validators=[
                IsFloatValidator(),
                RangeValidator(min_value=0.01, max_value=999999.99)
            ]
        )

        category: str = field(
            required=True,
            validators=[
                InArrayValidator([
                    'electronics', 'clothing', 'books', 'home',
                    'sports', 'beauty', 'toys', 'automotive'
                ])
            ]
        )

        tags: list = field(
            required=False,
            filters=[ArrayElementFilter(StringTrimFilter())],
            validators=[
                IsArrayValidator(),
                ArrayLengthValidator(max_length=20)
            ],
            default=[]
        )

        sku: str = field(
            required=True,
            filters=[StringTrimFilter(), ToUpperFilter()],
            validators=[
                RegexValidator(
                    pattern=r'^[A-Z0-9\-_]+$',
                    error_message="SKU can only contain uppercase letters, numbers, hyphens, and underscores"
                ),
                LengthValidator(min_length=3, max_length=50)
            ]
        )

        inventory_quantity: int = field(
            required=True,
            filters=[ToIntegerFilter()],
            validators=[
                IsIntegerValidator(),
                RangeValidator(min_value=0, max_value=999999)
            ]
        )

        weight: float = field(
            required=False,
            filters=[ToFloatFilter()],
            validators=[
                IsFloatValidator(),
                RangeValidator(min_value=0.01, max_value=999.99)
            ]
        )

        _conditions = [
            CustomCondition(
                lambda data: (
                    not data.get('compare_at_price') or
                    data.get('compare_at_price') > data.get('price', 0)
                ),
                error_message="Compare at price must be higher than regular price"
            )
        ]

Shopping Cart Operations
~~~~~~~~~~~~~~~~~~~~~~~

Add/update items in shopping cart with quantity validation:

.. code-block:: python

    class CartItemFilter(InputFilter):
        product_id: int = field(
            required=True,
            filters=[ToIntegerFilter()],
            validators=[
                IsIntegerValidator(),
                RangeValidator(min_value=1)
            ]
        )

        quantity: int = field(
            required=True,
            filters=[ToIntegerFilter()],
            validators=[
                IsIntegerValidator(),
                RangeValidator(
                    min_value=1,
                    max_value=99,
                    error_message="Quantity must be between 1 and 99"
                )
            ]
        )

        size: str = field(
            required=False,
            validators=[
                InArrayValidator(['XS', 'S', 'M', 'L', 'XL', 'XXL'])
            ]
        )

        color: str = field(
            required=False,
            filters=[StringTrimFilter()],
            validators=[
                RegexValidator(
                    pattern=r'^[a-zA-Z\s]+$',
                    error_message="Color must contain only letters and spaces"
                )
            ]
        )

        # Verify product exists and has sufficient inventory
        available_quantity: int = field(
            external_api={
                "url": "https://api.inventory.com/products/{{product_id}}/quantity",
                "method": "GET",
                "data_key": "available_quantity"
            },
            validators=[IsIntegerValidator()]
        )

        _conditions = [
            CustomCondition(
                lambda data: data.get('quantity', 0) <= data.get('available_quantity', 0),
                error_message="Requested quantity exceeds available inventory"
            )
        ]

File Upload & Media
------------------

Image Upload with Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Handle image uploads with size, format, and content validation:

.. code-block:: python

    from flask_inputfilter.validators import (
        IsBase64ImageValidator,
        IsBase64ImageCorrectSizeValidator
    )
    from flask_inputfilter.filters import (
        Base64ImageResizeFilter,
        Base64ImageDownscaleFilter
    )

    class ImageUploadFilter(InputFilter):
        image: str = field(
            required=True,
            validators=[
                IsBase64ImageValidator(
                    allowed_formats=['jpeg', 'jpg', 'png', 'webp'],
                    error_message="Image must be in JPEG, PNG, or WebP format"
                ),
                IsBase64ImageCorrectSizeValidator(
                    min_width=100,
                    min_height=100,
                    max_width=4000,
                    max_height=4000,
                    error_message="Image dimensions must be between 100x100 and 4000x4000 pixels"
                )
            ],
            filters=[
                Base64ImageResizeFilter(max_width=1920, max_height=1080),
                Base64ImageDownscaleFilter(quality=85)
            ]
        )

        title: str = field(
            required=False,
            filters=[StringTrimFilter()],
            validators=[LengthValidator(max_length=200)],
            default=""
        )

        alt_text: str = field(
            required=True,
            filters=[StringTrimFilter()],
            validators=[
                LengthValidator(
                    min_length=5,
                    max_length=500,
                    error_message="Alt text is required for accessibility (5-500 characters)"
                )
            ]
        )

        is_public: bool = field(
            required=False,
            default=True,
            validators=[IsBooleanValidator()]
        )

File Metadata Validation
~~~~~~~~~~~~~~~~~~~~~~~~

Validate file metadata for document uploads:

.. code-block:: python

    class FileMetadataFilter(InputFilter):
        filename: str = field(
            required=True,
            filters=[StringTrimFilter()],
            validators=[
                RegexValidator(
                    pattern=r'^[\w\-. ]+\.(pdf|doc|docx|txt|rtf)$',
                    error_message="File must have a valid name and be a PDF, DOC, DOCX, TXT, or RTF file"
                ),
                LengthValidator(max_length=255)
            ]
        )

        file_size: int = field(
            required=True,
            filters=[ToIntegerFilter()],
            validators=[
                IsIntegerValidator(),
                RangeValidator(
                    min_value=1,
                    max_value=10485760,  # 10MB in bytes
                    error_message="File size must be between 1 byte and 10MB"
                )
            ]
        )

        mime_type: str = field(
            required=True,
            validators=[
                InArrayValidator([
                    'application/pdf',
                    'application/msword',
                    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                    'text/plain',
                    'text/rtf'
                ])
            ]
        )

        tags: list = field(
            required=False,
            filters=[ArrayElementFilter(StringTrimFilter())],
            validators=[
                IsArrayValidator(),
                ArrayLengthValidator(max_length=10),
                ArrayElementValidator(LengthValidator(min_length=2, max_length=30))
            ],
            default=[]
        )

API & Search Operations
----------------------

Search and Filtering
~~~~~~~~~~~~~~~~~~~~

Comprehensive search with filtering, pagination, and sorting:

.. code-block:: python

    from datetime import datetime
    from flask_inputfilter.filters import ToDateTimeFilter

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
            validators=[
                IsIntegerValidator(),
                RangeValidator(min_value=1, max_value=1000)
            ],
            default=1
        )

        per_page: int = field(
            required=False,
            filters=[ToIntegerFilter()],
            validators=[
                IsIntegerValidator(),
                RangeValidator(min_value=1, max_value=100)
            ],
            default=20
        )

        # Sorting
        sort_by: str = field(
            required=False,
            validators=[
                InArrayValidator([
                    'created_at', 'updated_at', 'name', 'price',
                    'popularity', 'rating', 'title'
                ])
            ],
            default='created_at'
        )

        sort_direction: str = field(
            required=False,
            filters=[ToLowerFilter()],
            validators=[InArrayValidator(['asc', 'desc'])],
            default='desc'
        )

        # Filters
        category: str = field(
            required=False,
            validators=[IsStringValidator()]
        )

        status: str = field(
            required=False,
            validators=[
                InArrayValidator(['active', 'inactive', 'pending', 'archived'])
            ]
        )

        # Price range
        price_min: float = field(
            required=False,
            filters=[ToFloatFilter()],
            validators=[
                IsFloatValidator(),
                RangeValidator(min_value=0)
            ]
        )

        price_max: float = field(
            required=False,
            filters=[ToFloatFilter()],
            validators=[
                IsFloatValidator(),
                RangeValidator(min_value=0)
            ]
        )

        # Date range
        created_after: datetime = field(
            required=False,
            filters=[ToDateTimeFilter()],
            validators=[IsDateTimeValidator()]
        )

        created_before: datetime = field(
            required=False,
            filters=[ToDateTimeFilter()],
            validators=[IsDateTimeValidator()]
        )

        # Location-based search
        latitude: float = field(
            required=False,
            filters=[ToFloatFilter()],
            validators=[
                IsFloatValidator(),
                RangeValidator(min_value=-90, max_value=90)
            ]
        )

        longitude: float = field(
            required=False,
            filters=[ToFloatFilter()],
            validators=[
                IsFloatValidator(),
                RangeValidator(min_value=-180, max_value=180)
            ]
        )

        radius: float = field(
            required=False,
            filters=[ToFloatFilter()],
            validators=[
                IsFloatValidator(),
                RangeValidator(min_value=0.1, max_value=1000)  # km
            ],
            default=10.0
        )

        _conditions = [
            # Price range validation
            CustomCondition(
                lambda data: (
                    not all([data.get('price_min'), data.get('price_max')]) or
                    data.get('price_min') <= data.get('price_max')
                ),
                error_message="Minimum price cannot be greater than maximum price"
            ),

            # Date range validation
            CustomCondition(
                lambda data: (
                    not all([data.get('created_after'), data.get('created_before')]) or
                    data.get('created_after') <= data.get('created_before')
                ),
                error_message="Start date cannot be after end date"
            ),

            # Location search requires both coordinates
            CustomCondition(
                lambda data: (
                    not any([data.get('latitude'), data.get('longitude')]) or
                    all([data.get('latitude'), data.get('longitude')])
                ),
                error_message="Both latitude and longitude are required for location-based search"
            )
        ]

API Rate Limiting
~~~~~~~~~~~~~~~~

Handle API rate limiting parameters:

.. code-block:: python

    class RateLimitedRequestFilter(InputFilter):
        # Client identification
        client_id: str = field(
            required=True,
            filters=[StringTrimFilter()],
            validators=[
                RegexValidator(
                    pattern=r'^[a-zA-Z0-9\-_]+$',
                    error_message="Client ID must be alphanumeric with hyphens and underscores only"
                ),
                LengthValidator(min_length=8, max_length=64)
            ]
        )

        # Request signature for security
        signature: str = field(
            required=True,
            validators=[
                RegexValidator(
                    pattern=r'^[a-fA-F0-9]{64}$',
                    error_message="Signature must be a 64-character hexadecimal string"
                )
            ]
        )

        # Timestamp to prevent replay attacks
        timestamp: int = field(
            required=True,
            filters=[ToIntegerFilter()],
            validators=[
                IsIntegerValidator(),
                CustomValidator(
                    lambda value: abs(int(datetime.now().timestamp()) - value) <= 300,
                    error_message="Request timestamp must be within 5 minutes of current time"
                )
            ]
        )

        # Request priority
        priority: str = field(
            required=False,
            validators=[InArrayValidator(['low', 'normal', 'high'])],
            default='normal'
        )

Content Management
-----------------

Blog Post Creation
~~~~~~~~~~~~~~~~~

Complete blog post validation with SEO fields:

.. code-block:: python

    class BlogPostFilter(InputFilter):
        title: str = field(
            required=True,
            filters=[StringTrimFilter()],
            validators=[
                LengthValidator(
                    min_length=10,
                    max_length=200,
                    error_message="Title must be between 10 and 200 characters"
                )
            ]
        )

        slug: str = field(
            required=False,
            filters=[
                StringTrimFilter(),
                ToLowerFilter(),
                StringSlugifyFilter()
            ],
            validators=[
                RegexValidator(
                    pattern=r'^[a-z0-9\-]+$',
                    error_message="Slug can only contain lowercase letters, numbers, and hyphens"
                ),
                LengthValidator(min_length=3, max_length=200)
            ]
        )

        content: str = field(
            required=True,
            filters=[StringTrimFilter()],
            validators=[
                LengthValidator(
                    min_length=100,
                    max_length=50000,
                    error_message="Content must be between 100 and 50,000 characters"
                ),
                IsHtmlValidator()  # Validate HTML content
            ]
        )

        excerpt: str = field(
            required=False,
            filters=[StringTrimFilter()],
            validators=[
                LengthValidator(max_length=500)
            ]
        )

        # SEO fields
        meta_title: str = field(
            required=False,
            filters=[StringTrimFilter()],
            validators=[LengthValidator(max_length=70)]
        )

        meta_description: str = field(
            required=False,
            filters=[StringTrimFilter()],
            validators=[
                LengthValidator(
                    max_length=160,
                    error_message="Meta description should not exceed 160 characters for SEO"
                )
            ]
        )

        tags: list = field(
            required=False,
            filters=[
                ArrayElementFilter(StringTrimFilter()),
                ArrayElementFilter(ToLowerFilter())
            ],
            validators=[
                IsArrayValidator(),
                ArrayLengthValidator(max_length=15),
                ArrayElementValidator(
                    LengthValidator(min_length=2, max_length=30)
                )
            ],
            default=[]
        )

        category: str = field(
            required=True,
            validators=[
                InArrayValidator([
                    'technology', 'business', 'lifestyle', 'travel',
                    'health', 'education', 'entertainment', 'sports'
                ])
            ]
        )

        status: str = field(
            required=False,
            validators=[InArrayValidator(['draft', 'published', 'archived'])],
            default='draft'
        )

        featured_image: str = field(
            required=False,
            validators=[IsUrlValidator()]
        )

        publish_date: datetime = field(
            required=False,
            filters=[ToDateTimeFilter()],
            validators=[
                IsDateTimeValidator(),
                CustomValidator(
                    lambda value: value >= datetime.now(),
                    error_message="Publish date cannot be in the past"
                )
            ]
        )

        # Auto-generate slug from title if not provided
        def __post_init__(self):
            if not self.get_data().get('slug') and self.get_data().get('title'):
                from slugify import slugify
                self.set_field_value('slug', slugify(self.get_data()['title']))

Contact Forms & Communication
----------------------------

Contact Form
~~~~~~~~~~~

Standard contact form with spam protection:

.. code-block:: python

    class ContactFormFilter(InputFilter):
        name: str = field(
            required=True,
            filters=[StringTrimFilter()],
            validators=[
                LengthValidator(min_length=2, max_length=100),
                RegexValidator(
                    pattern=r'^[a-zA-Z\s\-\'\.]+$',
                    error_message="Name can only contain letters, spaces, hyphens, apostrophes, and periods"
                )
            ]
        )

        email: str = field(
            required=True,
            filters=[StringTrimFilter(), ToLowerFilter()],
            validators=[IsEmailValidator()]
        )

        phone: str = field(
            required=False,
            filters=[StringTrimFilter(), ToDigitsFilter()],
            validators=[
                RegexValidator(
                    pattern=r'^\d{10,15}$',
                    error_message="Phone number must be 10-15 digits"
                )
            ]
        )

        subject: str = field(
            required=True,
            filters=[StringTrimFilter()],
            validators=[
                LengthValidator(min_length=5, max_length=200)
            ]
        )

        message: str = field(
            required=True,
            filters=[StringTrimFilter()],
            validators=[
                LengthValidator(
                    min_length=20,
                    max_length=2000,
                    error_message="Message must be between 20 and 2000 characters"
                )
            ]
        )

        # Honeypot field for spam protection (should remain empty)
        website: str = field(
            required=False,
            validators=[
                CustomValidator(
                    lambda value: not value,
                    error_message="Spam protection triggered"
                )
            ],
            default=""
        )

        # reCAPTCHA token
        recaptcha_token: str = field(
            required=True,
            validators=[
                LengthValidator(min_length=10),
                # Add custom validator to verify reCAPTCHA with Google's API
                CustomValidator(verify_recaptcha_token)
            ]
        )

        # Consent for data processing
        consent_data_processing: bool = field(
            required=True,
            validators=[
                IsBooleanValidator(),
                CustomValidator(
                    lambda value: value is True,
                    error_message="You must consent to data processing to submit this form"
                )
            ]
        )

Newsletter Subscription
~~~~~~~~~~~~~~~~~~~~~~

Newsletter signup with double opt-in:

.. code-block:: python

    class NewsletterSubscriptionFilter(InputFilter):
        email: str = field(
            required=True,
            filters=[StringTrimFilter(), ToLowerFilter()],
            validators=[IsEmailValidator()]
        )

        first_name: str = field(
            required=False,
            filters=[StringTrimFilter()],
            validators=[
                LengthValidator(min_length=2, max_length=50),
                RegexValidator(
                    pattern=r'^[a-zA-Z\-\'\.]+$',
                    error_message="First name can only contain letters, hyphens, apostrophes, and periods"
                )
            ]
        )

        interests: list = field(
            required=False,
            filters=[ArrayElementFilter(StringTrimFilter())],
            validators=[
                IsArrayValidator(),
                ArrayLengthValidator(max_length=10),
                ArrayElementValidator(
                    InArrayValidator([
                        'technology', 'business', 'lifestyle', 'travel',
                        'health', 'education', 'entertainment', 'sports'
                    ])
                )
            ],
            default=[]
        )

        frequency: str = field(
            required=False,
            validators=[InArrayValidator(['daily', 'weekly', 'monthly'])],
            default='weekly'
        )

        source: str = field(
            required=False,
            validators=[
                InArrayValidator([
                    'website', 'social_media', 'search_engine',
                    'referral', 'advertisement', 'other'
                ])
            ]
        )

        consent_marketing: bool = field(
            required=True,
            validators=[
                IsBooleanValidator(),
                CustomValidator(
                    lambda value: value is True,
                    error_message="Marketing consent is required for newsletter subscription"
                )
            ]
        )

        # Check if email is already subscribed
        is_existing_subscriber: bool = field(
            external_api={
                "url": "https://api.newsletter.com/check-subscription",
                "method": "GET",
                "params": {"email": "{{email}}"},
                "data_key": "is_subscribed"
            },
            validators=[IsBooleanValidator()]
        )

        _conditions = [
            CustomCondition(
                lambda data: not data.get('is_existing_subscriber', False),
                error_message="This email address is already subscribed to our newsletter"
            )
        ]

Financial & Payment Processing
-----------------------------

Credit Card Payment
~~~~~~~~~~~~~~~~~~

Secure credit card processing with validation:

.. code-block:: python

    class CreditCardPaymentFilter(InputFilter):
        # Card details
        card_number: str = field(
            required=True,
            filters=[StringTrimFilter(), ToDigitsFilter()],
            validators=[
                LengthValidator(min_length=13, max_length=19),
                CustomValidator(luhn_check, error_message="Invalid card number")
            ]
        )

        expiry_month: int = field(
            required=True,
            filters=[ToIntegerFilter()],
            validators=[
                IsIntegerValidator(),
                RangeValidator(min_value=1, max_value=12)
            ]
        )

        expiry_year: int = field(
            required=True,
            filters=[ToIntegerFilter()],
            validators=[
                IsIntegerValidator(),
                RangeValidator(
                    min_value=datetime.now().year,
                    max_value=datetime.now().year + 20
                )
            ]
        )

        cvv: str = field(
            required=True,
            filters=[ToDigitsFilter()],
            validators=[
                RegexValidator(
                    pattern=r'^\d{3,4}$',
                    error_message="CVV must be 3 or 4 digits"
                )
            ]
        )

        # Cardholder info
        cardholder_name: str = field(
            required=True,
            filters=[StringTrimFilter()],
            validators=[
                LengthValidator(min_length=2, max_length=100),
                RegexValidator(
                    pattern=r'^[a-zA-Z\s\-\'\.]+$',
                    error_message="Cardholder name contains invalid characters"
                )
            ]
        )

        # Billing address
        billing_address: str = field(
            required=True,
            filters=[StringTrimFilter()],
            validators=[LengthValidator(min_length=5, max_length=200)]
        )

        billing_city: str = field(
            required=True,
            filters=[StringTrimFilter()],
            validators=[
                LengthValidator(min_length=2, max_length=100),
                RegexValidator(r'^[a-zA-Z\s\-\'\.]+$')
            ]
        )

        billing_postal_code: str = field(
            required=True,
            filters=[StringTrimFilter()],
            validators=[
                RegexValidator(
                    pattern=r'^\d{5}(-\d{4})?$',  # US ZIP code format
                    error_message="Please enter a valid postal code"
                )
            ]
        )

        billing_country: str = field(
            required=True,
            validators=[
                RegexValidator(
                    pattern=r'^[A-Z]{2}$',
                    error_message="Country must be a 2-letter ISO code"
                )
            ]
        )

        # Payment amount
        amount: float = field(
            required=True,
            filters=[ToFloatFilter()],
            validators=[
                IsFloatValidator(),
                RangeValidator(
                    min_value=0.01,
                    max_value=999999.99,
                    error_message="Payment amount must be between $0.01 and $999,999.99"
                ),
                FloatPrecisionValidator(
                    decimal_places=2,
                    error_message="Amount cannot have more than 2 decimal places"
                )
            ]
        )

        currency: str = field(
            required=True,
            validators=[InArrayValidator(['USD', 'EUR', 'GBP', 'CAD', 'AUD'])]
        )

        # Validation for card expiry
        _conditions = [
            CustomCondition(
                lambda data: (
                    datetime.now() < datetime(
                        data.get('expiry_year', 2000),
                        data.get('expiry_month', 1),
                        1
                    )
                ),
                error_message="Credit card has expired"
            )
        ]

Bank Transfer
~~~~~~~~~~~~

Bank transfer validation for different regions:

.. code-block:: python

    class BankTransferFilter(InputFilter):
        # Account details
        account_number: str = field(
            required=True,
            filters=[StringTrimFilter(), ToDigitsFilter()],
            validators=[
                LengthValidator(min_length=8, max_length=34),  # IBAN can be up to 34 chars
                RegexValidator(r'^\d+$', error_message="Account number must contain only digits")
            ]
        )

        routing_number: str = field(
            required=True,
            filters=[StringTrimFilter()],
            validators=[
                LengthValidator(min_length=8, max_length=11),
                RegexValidator(
                    pattern=r'^\d{8,11}$',
                    error_message="Routing number must be 8-11 digits"
                )
            ]
        )

        account_holder_name: str = field(
            required=True,
            filters=[StringTrimFilter()],
            validators=[
                LengthValidator(min_length=2, max_length=100),
                RegexValidator(r'^[a-zA-Z\s\-\'\.]+$')
            ]
        )

        bank_name: str = field(
            required=True,
            filters=[StringTrimFilter()],
            validators=[LengthValidator(min_length=2, max_length=100)]
        )

        account_type: str = field(
            required=True,
            validators=[InArrayValidator(['checking', 'savings', 'business'])]
        )

        # Transfer details
        transfer_amount: float = field(
            required=True,
            filters=[ToFloatFilter()],
            validators=[
                IsFloatValidator(),
                RangeValidator(min_value=1.00, max_value=50000.00),
                FloatPrecisionValidator(decimal_places=2)
            ]
        )

        transfer_memo: str = field(
            required=False,
            filters=[StringTrimFilter()],
            validators=[LengthValidator(max_length=200)]
        )

        # Verification for large amounts
        verification_required: bool = field(
            external_api={
                "url": "https://api.compliance.com/verify-amount",
                "method": "POST",
                "data": {"amount": "{{transfer_amount}}"},
                "data_key": "requires_verification"
            },
            validators=[IsBooleanValidator()]
        )

Usage Examples
--------------

Using Recipes in Your Application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Here's how to integrate these recipes into your Flask application:

.. code-block:: python

    from flask import Flask, request, jsonify, g

    app = Flask(__name__)

    # User registration endpoint
    @app.route('/api/register', methods=['POST'])
    @UserRegistrationFilter.validate()
    def register():
        data = g.validated_data
        # Create user account with validated data
        user = create_user_account(data)
        return jsonify({"success": True, "user_id": user.id})

    # Product search endpoint
    @app.route('/api/products/search', methods=['GET'])
    @SearchFilter.validate()
    def search_products():
        filters = g.validated_data
        products = search_products_with_filters(filters)
        return jsonify({
            "products": products,
            "pagination": {
                "page": filters['page'],
                "per_page": filters['per_page'],
                "total": len(products)
            }
        })

    # Contact form endpoint
    @app.route('/api/contact', methods=['POST'])
    @ContactFormFilter.validate()
    def contact_form():
        data = g.validated_data
        # Send email and save to database
        send_contact_email(data)
        save_contact_message(data)
        return jsonify({"success": True, "message": "Thank you for your message!"})

Customizing Recipes
~~~~~~~~~~~~~~~~~~~

All recipes can be easily customized for your specific needs:

.. code-block:: python

    # Extend the UserRegistrationFilter for your specific requirements
    class CustomUserRegistrationFilter(UserRegistrationFilter):
        # Add custom fields
        company_name: str = field(
            required=False,
            filters=[StringTrimFilter()],
            validators=[LengthValidator(max_length=100)]
        )

        # Override password requirements
        password: str = field(
            required=True,
            validators=[
                LengthValidator(min_length=12),  # Stricter requirement
                # Add custom password strength validator
                CustomValidator(check_password_strength)
            ]
        )

        # Add custom conditions
        _conditions = UserRegistrationFilter._conditions + [
            CustomCondition(
                lambda data: not is_disposable_email(data.get('email')),
                error_message="Disposable email addresses are not allowed"
            )
        ]