from Cython.Build import cythonize
from setuptools import Extension, find_packages, setup

ext_modules = cythonize(
    [
        Extension(name="", sources=["flask_inputfilter/InputFilter.pyx"]),
    ],
    compiler_directives={"language_level": "3"},
)

setup(
    name="flask_inputfilter",
    version="0.2.0",
    license="MIT",
    license_files=["LICENSE"],
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
    ext_modules=ext_modules,
    package_data={"flask_inputfilter": ["*.pyx", "*.py"]},
    include_package_data=True,
    install_requires=[
        "Flask>=2.1",
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
