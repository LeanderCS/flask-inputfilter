import shutil

from setuptools import setup

if shutil.which("g++") is not None:
    from Cython.Build import cythonize
    from setuptools.extension import Extension

    pyx_modules = [
        "flask_inputfilter.Mixin._ExternalApiMixin",
        "flask_inputfilter.Model._FieldModel",
        "flask_inputfilter._InputFilter",
    ]

    ext_modules = cythonize(
        module_list=[Extension(
            name=module,
            sources=[module.replace('.', '/') + ".pyx"],
            extra_compile_args=["-std=c++11"],
            language="c++"
        ) for module in pyx_modules],
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
