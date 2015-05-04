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

Using docker and fig
--------------------

Docker and fig are used to assist with developing this software.  Both
of these tools should be installed on the host server.  Some variables
have required values for development: ::

    # DEBUG must be True when using fig
    DEBUG=True

    # Container uses this value
    PUBLIC_ROOT=/opt/public

.. note:: If `squid-deb-proxy`_ is running on port 8000, the Dockerfile
   will access the cache when retrieving packages from the Internet.
   This can save considerable time when rebuilding images.

The containers can be built with the following command: ::

    $ fig build

To run the existing test suite, use the following command: ::

    $ fig run web python manage.py test

The containers can be rebuilt and populated with test data using the
following command: ::

    $ ./dev-setup.sh

.. todo:: A database dump and collection of media files are both
   required to run this command.  These are not currently supplied,
   but fixing that has a high priority!

To bring up the web site on port 8001: ::

    $ fig up

.. _`squid-deb-proxy`: https://launchpad.net/squid-deb-proxy
