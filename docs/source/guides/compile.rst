Use compiled version
====================

By default the pure python version of the lib is used as a fallback.
Using the compiled version is not mandatory but highly advised and
will give you a performance boost.

Getting started
---------------

To use the compiled version you will first need the cython module,
you can install the corresponding version by also installing the
``[compile]`` dependencies of the library.

.. code-block:: bash

    pip install flask-inputfilter[compile]

Secondly, you will need the c++ compiler.

Normally this is already installed on your system, but if not,
depending on your os, you can use:

.. grid:: 1
    :gutter: 2

    .. grid-item::
        .. card:: Linux

            Install the gcc compiler using apt.

            .. code-block:: bash

                sudo apt install g++

    .. grid-item::
        .. card:: MacOS

            Either install the Xcode command line tools or use homebrew:

            .. code-block:: bash

                xcode-select --install g++

            .. code-block:: bash

                brew install g++

    .. grid-item::
        .. card:: Windows

            1. Download MinGW:
                https://www.mingw-w64.org
            2. Install and add ``g++.exe`` to PATH.

If you have the c++ compiler installed and reinstall the library,
with or without the ``[compile]`` flag, depending if you already installed it,
it will automatically compile the files, that offer an optimized version.

After these steps you can use the library normally and should not get the warning in the console.

Verify Installation
-------------------

If you followed the steps above, you should not see the warning message in the console.

Additionally, you can verify if the compiled versions are
being used by running the following commands:

.. code-block:: bash

    python -c "import flask_inputfilter"
    python -c "InputFilter"

If the result is ``<class 'flask_inputfilter._InputFilter.InputFilter'>``,
the compiled version is being used.
