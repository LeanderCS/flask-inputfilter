import shutil

from setuptools import setup

if shutil.which("g++") is not None:
    from pathlib import Path

    from Cython.Build import cythonize
    from setuptools.extension import Extension

    pyx_files = Path("flask_inputfilter").rglob("*.pyx")

    pyx_modules = [".".join(path.with_suffix("").parts) for path in pyx_files]

    ext_modules = cythonize(
        module_list=[
            Extension(
                name=module,
                sources=[str(Path(*module.split(".")).with_suffix(".pyx"))],
                extra_compile_args=["-std=c++11"],
                language="c++",
            )
            for module in pyx_modules
        ],
        language_level=3,
        compiler_directives={
            "binding": True,
            "boundscheck": False,
            "cdivision": True,
            "embedsignature": True,
            "infer_types": True,
            "initializedcheck": False,
            "linetrace": False,
            "profile": False,
            "wraparound": False,
        },
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
