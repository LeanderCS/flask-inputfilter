try:
    from .InputFilter import InputFilter

except ImportError:
    import logging

    import pyximport

    pyximport.install(setup_args={"script_args": ["--quiet"]})

    from .InputFilter import InputFilter

    logging.getLogger(__name__).warning(
        "flask-inputfilter not compiled, using pure Python version. "
        + "Consider installing a C compiler to compile the Cython version for better performance."
    )
