from setuptools import setup, find_packages
from setuptools.extension import Extension

try:
    from Cython.Build import cythonize
    USE_CYTHON = True
except ImportError:
    USE_CYTHON = False

ext_modules = []
if USE_CYTHON:
    ext_modules = cythonize([
        Extension(
            "flask_inputfilter.InputFilter",
            ["flask_inputfilter/InputFilter.pyx"],
            extra_compile_args=["-O3"]
        )
    ])

setup(
    name="flask_inputfilter",
    version="0.3.0a4",
    license="MIT",
    author="Leander Cain Slotosch",
    author_email="slotosch.leander@outlook.de",
    description="A library to easily filter and validate input data in "
    "Flask applications",
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    url="https://github.com/LeanderCS/flask-inputfilter",
    packages=find_packages(include=["flask_inputfilter", "flask_inputfilter.*"]),
    package_data={
        "flask_inputfilter": ["*.pyx", "*.pxd"]
    },
    setup_requires=[
        "cython>=0.29.0",
    ],
    ext_modules=ext_modules,
    install_requires=[
        "flask>=2.1",
        "typing_extensions>=3.6.2",
    ],
    extras_require={
        "optional": [
            "pillow>=8.0.0",
            "requests>=2.22.0",
        ],
    },
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires=">=3.7",
    project_urls={
        "Documentation": "https://leandercs.github.io/flask-inputfilter",
        "Source": "https://github.com/LeanderCS/flask-inputfilter",
    },
)
