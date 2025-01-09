from setuptools import find_packages, setup

setup(
    name="flask_inputfilter",
    version="0.0.4",
    author="Leander Cain Slotosch",
    author_email="slotosch.leander@outlook.de",
    description="A library to filter and validate input data in"
    "Flask applications",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/LeanderCS/flask-inputfilter",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "Flask>=0.10",
        "pillow>=2.0.0",
        "requests>=2.12.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
