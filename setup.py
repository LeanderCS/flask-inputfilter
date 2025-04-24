import shutil

from setuptools import setup

if shutil.which("g++") is not None:
    from Cython.Build import cythonize

    ext_modules = cythonize(
        [
            "flask_inputfilter/Mixin/_ExternalApiMixin.pyx",
            "flask_inputfilter/Model/_FieldModel.pyx",
            "flask_inputfilter/_InputFilter.pyx",
        ],
        language_level=3,
    )
    options = {
        "build_ext": {"include_dirs": ["flask_inputfilter/include"]},
    }

else:
    ext_modules = []
    options = {}

setup(
    ext_modules=ext_modules,
    options=options,
)
