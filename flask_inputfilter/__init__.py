import logging
import shutil

try:
    from ._InputFilter import InputFilter

except ImportError:
    if shutil.which("g++") is not None:
        import logging

        import pyximport

        pyximport.install(setup_args={"script_args": ["--quiet"]})

        from ._InputFilter import InputFilter

    else:
        logging.getLogger(__name__).warning(
            "Cython is not installed and g++ is not available. "
            "Falling back to pure Python implementation. "
            "Consider installing Cython and g++ for better performance."
        )
        from .InputFilter import InputFilter
