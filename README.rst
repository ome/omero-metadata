.. image:: https://github.com/ome/omero-metadata/workflows/OMERO/badge.svg
    :target: https://github.com/ome/omero-metadata/actions

.. image:: https://badge.fury.io/py/omero-metadata.svg
    :target: https://badge.fury.io/py/omero-metadata

OMERO metadata plugin
=====================

Plugin for use in the OMERO CLI. Provides tools for bulk
management of annotations on objects in OMERO.

Requirements
============

* OMERO 5.6.0 or newer
* Python 3.6 or newer


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

Usage
=====

The plugin is called from the command-line using the `omero` command::

    $ omero metadata <subcommand>

Help for each command can be shown using the ``-h`` flag.
Objects can be specified as arguments in the format ``Class:ID``, such
as ``Project:123``.

Bulk-annotations are HDF-based tables with the NSBULKANNOTATION
namespace, sometimes referred to as OMERO.tables.

Available subcommands are:

- ``allanns``: Provide a list of all annotations linked to the given object
- ``bulkanns``: Provide a list of the NSBULKANNOTATION tables linked to the given object
- ``mapanns``: Provide a list of all MapAnnotations linked to the given object
- ``measures``: Provide a list of the NSMEASUREMENT tables linked to the given object
- ``original``: Print the original metadata in ini format
- ``pixelsize``: Set physical pixel size
- ``populate``: Add metadata (bulk-annotations) to an object (see below)
- ``rois``: Manage ROIs
- ``summary``: Provide a general summary of available metadata
- ``testtables``: Tests whether tables can be created and initialized

populate
--------

This command creates an ``OMERO.table`` (bulk annotation) from a ``CSV`` file and links 
the table as a ``File Annotation`` to a parent container such as Screen, Plate, Project
or Dataset. It also attempts to convert Image or Well names from the ``CSV`` into
Image or Well IDs in the ``OMERO.table``.

The ``CSV`` file must be provided as local file with ``--file path/to/file.csv``.

If you wish to ensure that ``number`` columns are created for numerical data, this will
allow you to make numerical queries on the table.
Column Types are:

- ``d``: ``DoubleColumn``, for floating point numbers
- ``l``: ``LongColumn``, for integer numbers
- ``s``: ``StringColumn``, for text
- ``b``: ``BoolColumn``, for true/false
- ``plate``, ``well``, ``image``, ``dataset``, ``roi`` to specify objects

These can be specified in the first row of a ``CSV`` with a ``# header`` tag (see examples below).
The ``# header`` row is optional. Default column type is ``String``.

NB: Column names should not contain spaces if you want to be able to query
by these columns.

Examples:

To add a table to a Project, the ``CSV`` file needs to specify ``Dataset Name``
and ``Image Name``::

    $ omero metadata populate Project:1 --file path/to/project.csv

project.csv::

    # header s,s,d,l,s
    Image Name,Dataset Name,ROI_Area,Channel_Index,Channel_Name
    img-01.png,dataset01,0.0469,1,DAPI
    img-02.png,dataset01,0.142,2,GFP
    img-03.png,dataset01,0.093,3,TRITC
    img-04.png,dataset01,0.429,4,Cy5

This will create an OMERO.table linked to the Project like this:

========== ============ ======== ============= ============ =====
Image Name Dataset Name ROI_Area Channel_Index Channel_Name Image
========== ============ ======== ============= ============ =====
img-01.png dataset01    0.0469   1             DAPI         36638
img-02.png dataset01    0.142    2             GFP          36639
img-03.png dataset01    0.093    3             TRITC        36640
img-04.png dataset01    0.429    4             Cy5          36641
========== ============ ======== ============= ============ =====

If the target is a Dataset instead of a Project, the ``Dataset Name`` column is not needed.

To add a table to a Screen, the ``CSV`` file needs to specify ``Plate`` name and ``Well``.
If a ``# header`` is specified, column types must be ``well`` and ``plate``.

screen.csv::

    # header well,plate,s,d,l,d
    Well,Plate,Drug,Concentration,Cell_Count,Percent_Mitotic
    A1,plate01,DMSO,10.1,10,25.4
    A2,plate01,DMSO,0.1,1000,2.54
    A3,plate01,DMSO,5.5,550,4
    B1,plate01,DrugX,12.3,50,44.43

This will create an OMERO.table linked to the Screen, with the
``Well Name`` and ``Plate Name`` columns added and the ``Well`` and
``Plate`` columns used for IDs:

===== ====== ====== ============== =========== ================ =========== ===========
Well  Plate  Drug   Concentration  Cell_Count  Percent_Mitotic  Well Name   Plate Name
===== ====== ====== ============== =========== ================ =========== ===========
9154  3855   DMSO   10.1           10          25.4             a1          plate01
9155  3855   DMSO   0.1            1000        2.54             a2          plate01
9156  3855   DMSO   5.5            550         4.0              a3          plate01
9157  3855   DrugX  12.3           50          44.43            b1          plate01
===== ====== ====== ============== =========== ================ =========== ===========

If the target is a Plate instead of a Screen, the ``Plate`` column is not needed.

If the target is an Image, a csv with ROI-level and object-level data can be used to create an
``OMERO.table`` (bulk annotation) as a ``File Annotation`` on an Image.
The ROI identifying column can be an ``roi`` type column containing ROI ID, and ``Roi Name``
column will be appended automatically (see example below). Alternatively, the input column can be
``Roi Name`` (with type ``s``), and an ``roi`` type column will be appended containing ROI IDs.
In this case, it is required that ROIs on the Image in OMERO have the ``Name`` attribute set.

image.csv::

    # header roi,l,d,l
    Roi,object,probability,area
    501,1,0.8,250
    502,1,0.9,500
    503,1,0.2,25
    503,2,0.8,400
    503,3,0.5,200

This will create an OMERO.table linked to the Image like this:

=== ====== =========== ==== ========
Roi object probability area Roi Name
=== ====== =========== ==== ========
501 1      0.8         250  Sample1
502 1      0.9         500  Sample2
503 1      0.2         25   Sample3
503 2      0.8         400  Sample3
503 3      0.5         200  Sample3
=== ====== =========== ==== ========

Note that the ROI-level ``OMERO.table`` is not visible in the OMERO.web UI right-hand panel, but can be visualized by clicking the "eye" on the bulk annotation attachment on the Image.

Developer install
=================

This plugin can be installed from the source code with::

    $ cd omero-metadata
    $ pip install .


License
-------

This project, similar to many Open Microscopy Environment (OME) projects, is
licensed under the terms of the GNU General Public License (GPL) v2 or later.

Copyright
---------

2018-2021, The Open Microscopy Environment
