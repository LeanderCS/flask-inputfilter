"""
Performance configuration for Flask-InputFilter.

This module provides configuration options to fine-tune the performance
characteristics of the library based on specific use cases.
"""

from __future__ import annotations

from typing import ClassVar


class PerformanceConfig:
    """
    Global performance configuration for Flask-InputFilter.

    Attributes:
        USE_LAZY_EVALUATION: Enable lazy evaluation for filter chains
            (default: True)
        LAZY_EVALUATION_THRESHOLD: Minimum number of filters to trigger lazy
            evaluation (default: 5)
        REGEX_CACHE_SIZE: Maximum number of compiled regex patterns to cache
            (default: 128)
        USE_STRING_INTERNING: Enable automatic string interning for field
            names (default: True)
        LARGE_DATASET_THRESHOLD: Number of fields to consider as "large"
            for optimization (default: 10)
        USE_CYTHON: Use Cython-compiled modules when available (default: True)
    """

    USE_LAZY_EVALUATION: ClassVar[bool] = True
    LAZY_EVALUATION_THRESHOLD: ClassVar[int] = 5
    REGEX_CACHE_SIZE: ClassVar[int] = 128
    USE_STRING_INTERNING: ClassVar[bool] = True
    LARGE_DATASET_THRESHOLD: ClassVar[int] = 10
    USE_CYTHON: ClassVar[bool] = True

    @classmethod
    def set_high_performance(cls) -> None:
        """Configure for maximum performance (may use more memory)."""
        cls.USE_LAZY_EVALUATION = True
        cls.LAZY_EVALUATION_THRESHOLD = 3
        cls.REGEX_CACHE_SIZE = 256
        cls.USE_STRING_INTERNING = True
        cls.LARGE_DATASET_THRESHOLD = 5
        cls.USE_CYTHON = True

    @classmethod
    def set_low_memory(cls) -> None:
        """Configure for minimal memory usage (may be slower)."""
        cls.USE_LAZY_EVALUATION = False
        cls.LAZY_EVALUATION_THRESHOLD = 10
        cls.REGEX_CACHE_SIZE = 32
        cls.USE_STRING_INTERNING = False
        cls.LARGE_DATASET_THRESHOLD = 20
        cls.USE_CYTHON = True

    @classmethod
    def set_balanced(cls) -> None:
        """Reset to balanced default configuration."""
        cls.USE_LAZY_EVALUATION = True
        cls.LAZY_EVALUATION_THRESHOLD = 5
        cls.REGEX_CACHE_SIZE = 128
        cls.USE_STRING_INTERNING = True
        cls.LARGE_DATASET_THRESHOLD = 10
        cls.USE_CYTHON = True
