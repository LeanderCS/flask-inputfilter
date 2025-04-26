try:
    from ._input_filter import InputFilter

except ImportError:
    import shutil

    if shutil.which("g++") is not None:
        import os

        import pyximport

        THIS_DIR = os.path.dirname(__file__)
        INCLUDE_DIR = os.path.join(THIS_DIR, "include")

        pyximport.install(
            language_level=3,
            setup_args={
                "script_args": ["--quiet"],
                "include_dirs": [INCLUDE_DIR],
            },
            reload_support=True,
        )

        from ._input_filter import InputFilter

    else:
        import logging

        logging.getLogger(__name__).warning(
            "Cython or g++ not available. Falling back to pure Python implementation.\n"
            "Consult docs for better performance: https://leandercs.github.io/flask-inputfilter/guides/compile.html"
        )
        from .input_filter import InputFilter
