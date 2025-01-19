Development
===========

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

    docker exec -it flask-inputfilter sh -c "isort ."
    docker exec -it flask-inputfilter sh -c "autoflake --in-place --remove-all-unused-imports --ignore-init-module-imports --recursive ."
    docker exec -it flask-inputfilter black .
