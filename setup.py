import shutil

from setuptools import setup

if shutil.which("g++") is not None:
    from Cython.Build import cythonize

    ext_modules = cythonize(
        [
            "flask_inputfilter/Mixin/_ExternalApiMixin.pyx",
            "flask_inputfilter/_InputFilter.pyx",
        ],
        language_level=3,
    )
else:
    ext_modules = []

setup(ext_modules=ext_modules)
