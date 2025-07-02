try:
    from ._input_filter import InputFilter

except ImportError:
    import shutil
    from pathlib import Path

    _HAS_GPP = shutil.which("g++") is not None

    if _HAS_GPP:
        try:
            import pyximport

            THIS_DIR = Path(__file__).parent
            INCLUDE_DIR = THIS_DIR / "include"

            pyximport.install(
                language_level=3,
                setup_args={
                    "script_args": ["--quiet"],
                    "include_dirs": [str(INCLUDE_DIR)],
                },
                reload_support=True,
            )

            from ._input_filter import InputFilter

        except ImportError:
            import logging

            logging.getLogger(__name__).debug(
                "Pyximport failed, falling back to pure Python implementation."
            )
            from .input_filter import InputFilter

    else:
        import logging

        logging.getLogger(__name__).warning(
            "Cython or g++ not available. Falling back to pure Python "
            "implementation.\n"
            "Consult docs for better performance: https://leandercs.github.io"
            "/flask-inputfilter/guides/compile.html"
        )
        from .input_filter import InputFilter

__all__ = [
    "InputFilter",
]
