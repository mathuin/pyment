Developer's Guide
=================

Getting started
---------------

The ``pyment`` source code is hosted on GitHub. ::

    $ git clone git://github.com/mathuin/pyment

The `GitHub Flow`_ development model is used for this project.

All pull requests should be created from the ``master`` branch, and
should include relevant updates to the documentation.

All bug fixes should include tests which confirm both the original
presence of the bug and its eradication.

.. _`GitHub Flow`: https://guides.github.com/introduction/flow/

Using docker and docker-compose
-------------------------------

Docker and docker-compose are used to assist with developing this software.
Both of these tools should be installed on the host server.

The containers can be built with the following command: ::

    $ docker-compose build

To run the existing test suite, use the following command: ::

    $ docker-compose run --rm web python manage.py test

The containers can be rebuilt and populated with test data using the
following command: ::

    $ ./dev-setup.sh

To bring up the web site on port 8000: ::

    $ docker-compose up

Updating documentation
----------------------

This documentation is generated using Sphinx.

To rebuild the documentation after changes: ::

    $ docker-compose run --rm web make -C docs html
