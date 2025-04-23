import shutil

from setuptools import setup

if shutil.which("g++") is not None:
    from Cython.Build import cythonize

    setup(
        ext_modules=cythonize(
            [
                "flask_inputfilter/Mixin/_ExternalApiMixin.pyx",
                "flask_inputfilter/_InputFilter.pyx",
            ],
            language_level=3,
        ),
    )
