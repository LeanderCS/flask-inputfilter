Development
===========

This guide will help you set up a development environment for the library project.

You can find the source code for the library in the `GitHub repository <https://github.com/LeanderCS/flask-inputfilter>`_.

Build docker image
-------------------

.. code-block:: bash

    docker build -t flask-inputfilter .

Run docker container in interactive mode
----------------------------------------

.. code-block:: bash

    docker compose up -d

.. code-block:: bash

    docker exec -it flask-inputfilter /bin/bash

Run tests
---------

.. code-block:: bash

    docker exec -it flask-inputfilter pytest

Run linting
-----------

.. code-block:: bash

    docker exec -it flask-inputfilter lint
