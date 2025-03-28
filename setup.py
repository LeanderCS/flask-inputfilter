from setuptools import Extension, find_packages, setup

try:
    from Cython.Build import cythonize
    USE_CYTHON = True
except ImportError:
    USE_CYTHON = False

ext = ".pyx" if USE_CYTHON else ".c"

extensions = [
    Extension(
        name="flask_inputfilter.InputFilter",
        sources=[f"flask_inputfilter/InputFilter{ext}"],
    ),
]

if USE_CYTHON:
    extensions = cythonize(extensions, language_level=3)

setup(
    name="flask_inputfilter",
    version="0.2.0a3",
    license="MIT",
    author="Leander Cain Slotosch",
    author_email="slotosch.leander@outlook.de",
    description="A library to filter and validate input data in "
    "Flask applications",
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    url="https://github.com/LeanderCS/flask-inputfilter",
    packages=find_packages(
        include=["flask_inputfilter", "flask_inputfilter.*"]
    ),
    ext_modules=extensions,
    package_data={"flask_inputfilter": ["*.pyx", "*.py", "*.c"]},
    include_package_data=True,
    install_requires=[
        "flask>=2.1",
        "pillow>=8.0.0",
        "requests>=2.22.0",
        "typing_extensions>=3.6.2",
    ],
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
