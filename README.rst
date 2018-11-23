.. image:: https://travis-ci.org/ome/omero-metadata.svg?branch=master
    :target: https://travis-ci.org/ome/omero-metadata

.. image:: https://badge.fury.io/py/omero-metadata.svg
    :target: https://badge.fury.io/py/omero-metadata

OMERO metadata plugin
=====================

Plugin for use in the OMERO CLI.

Requirements
============

* OMERO 5.4.0 or newer
* Python 2.7


Installing from PyPI
====================

This section assumes that an OMERO.py is already installed.

Install the command-line tool using `pip <https://pip.pypa.io/en/stable/>`_:

::

    $ pip install -U omero-metadata

Note the original version of this code is still available as deprecated code in
version 5.4.x of OMERO.py. When using the CLI metadata plugin, the
`OMERO_DEV_PLUGINS` environment variable should not be set to prevent
conflicts when importing the Python module.

License
-------

This project, similar to many Open Microscopy Environment (OME) projects, is
licensed under the terms of the GNU General Public License (GPL) v2 or later.

Copyright
---------

2018, The Open Microscopy Environment
