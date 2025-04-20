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
            "Cython or g++ not available. Falling back to pure Python implementation.\n"
            "Consult docs for better performance: https://leandercs.github.io/flask-inputfilter/guides/compile.html"
        )
        from .InputFilter import InputFilter
