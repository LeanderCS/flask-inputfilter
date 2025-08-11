Performance Configuration
=========================

The Flask-InputFilter library provides various performance optimization settings that can be tuned based on your specific use case.

Overview
--------

The ``PerformanceConfig`` class allows you to control various performance-related settings such as lazy evaluation, caching, and string interning.

Configuration Options
---------------------

The following options are available:

- **USE_LAZY_EVALUATION**: Enable lazy evaluation for filter chains (default: ``True``)
- **LAZY_EVALUATION_THRESHOLD**: Minimum number of filters to trigger lazy evaluation (default: ``5``)
- **REGEX_CACHE_SIZE**: Maximum number of compiled regex patterns to cache (default: ``128``)
- **USE_STRING_INTERNING**: Enable automatic string interning for field names (default: ``True``)
- **LARGE_DATASET_THRESHOLD**: Number of fields to consider as "large" for optimization (default: ``10``)
- **USE_CYTHON**: Use Cython-compiled modules when available (default: ``True``)

Usage Examples
--------------

Basic Configuration
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from flask_inputfilter.performance_config import PerformanceConfig
    
    # Set individual options
    PerformanceConfig.USE_LAZY_EVALUATION = True
    PerformanceConfig.REGEX_CACHE_SIZE = 256

Preset Configurations
~~~~~~~~~~~~~~~~~~~~~

The library provides preset configurations for common scenarios:

**High Performance Mode**

Optimized for maximum speed, may use more memory:

.. code-block:: python

    from flask_inputfilter.performance_config import PerformanceConfig
    
    PerformanceConfig.set_high_performance()

**Low Memory Mode**

Optimized for minimal memory usage, may be slower:

.. code-block:: python

    from flask_inputfilter.performance_config import PerformanceConfig
    
    PerformanceConfig.set_low_memory()

**Balanced Mode**

Reset to default balanced configuration:

.. code-block:: python

    from flask_inputfilter.performance_config import PerformanceConfig
    
    PerformanceConfig.set_balanced()

Lazy Filter Chain
-----------------

The ``LazyFilterChain`` class provides lazy evaluation for filter chains, which can significantly improve performance when dealing with large filter chains or when early filters might invalidate the need for later processing.

.. autoclass:: flask_inputfilter.filters.LazyFilterChain
   :members:
   :undoc-members:
   :show-inheritance:

Performance Config API
----------------------

.. autoclass:: flask_inputfilter.performance_config.PerformanceConfig
   :members:
   :undoc-members:
   :show-inheritance:

Best Practices
--------------

1. **For High-Volume APIs**: Use ``set_high_performance()`` to maximize throughput
2. **For Memory-Constrained Environments**: Use ``set_low_memory()`` to minimize memory footprint
3. **For Complex Validation Chains**: Keep ``USE_LAZY_EVALUATION`` enabled to avoid unnecessary processing
4. **For Regex-Heavy Validation**: Increase ``REGEX_CACHE_SIZE`` if you have many unique regex patterns

Performance Tips
----------------

- String interning is most effective when you have many repeated field names across requests
- Lazy evaluation provides the most benefit when you have long filter chains (>5 filters)
- The regex cache is shared across all validator instances, so increasing its size helps with diverse patterns
- Cython compilation provides 30-50% performance improvement for core validation logic