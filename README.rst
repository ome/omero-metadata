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

The plugin is called from the command-line using the ``omero metadata`` command::

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
the table as a ``File Annotation`` to a parent container such as Screen, Plate, Project,
Dataset or Image. It also attempts to convert Image, Well or ROI names from the ``CSV`` into
object IDs in the ``OMERO.table``.

The ``CSV`` file must be provided as local file with ``--file path/to/file.csv``.

OMERO.tables have defined column types to specify the data-type such as ``double`` or ``long`` and special object-types of each column for storing OMERO object IDs such as ``ImageColumn`` or ``WellColumn``

The default behaviour of the script is to automatically detect the column types from an input ``CSV``. This behaviour works as follows:

*  Columns named with a supported object-type (e.g. ``plate``, ``well``, ``image``, ``dataset``, or ``roi``), with ``<object> id`` or ``<object> name`` will generate the corresponding column type in the OMERO.table. See table below for full list of supported column names.

============ ================= ==================== ==================================
Column Name  Column type       Detected Header Type Notes
============ ================= ==================== ==================================
Image        ``ImageColumn``   ``image``            Appends 'Image Name' column
Image Name   ``StringColumn``  ``s``                Appends 'Image' column
Image ID     ``ImageColumn``   ``image``            Appends 'Image Name' column
Dataset      ``DatasetColumn`` ``dataset``          \-
Dataset Name ``StringColumn``  ``s``                \-
Dataset ID   ``DatasetColumn`` ``dataset``          \-
Plate        ``PlateColumn``   ``plate``            Adds 'Plate' column
Plate Name   ``PlateColumn``   ``plate``            Adds 'Plate' column
Plate ID     ``LongColumn``    ``l``                \-
Well         ``WellColumn``    ``well``             Adds 'Well' column
Well Name    ``WellColumn``    ``well``             Adds 'Well' column
Well ID      ``LongColumn``    ``l``                \-
ROI          ``RoiColumn``     ``roi``              Appends 'ROI Name' column
ROI Name     ``StringColumn``  ``s``                Appends 'ROI' column
ROI ID       ``RoiColumn``     ``roi``              Appends 'ROI Name' column
============ ================= ==================== ==================================
         
Note: Column names are case insensitive. Space, no space, and underscore are all accepted as separators for column names (i.e. ``<object> name``/``<object> id```, ``<object>name``/``<object>id``, ``<object>_name``/``<object>_id`` are all accepted)

NB: Column names should not contain spaces if you want to be able to query by these columns.

*  All other column types will be detected based on the column's data using the pandas library. See table below.

=============== ================= ====================
Column Name     Column type       Detected Header Type
=============== ================= ====================
Example String  ``StringColumn``  ``s``      
Example Long    ``LongColumn``    ``l``      
Example Float   ``DoubleColumn``  ``d``      
Example boolean ``BoolColumn``    ``b``      
=============== ================= ====================


However, it is possible to manually define the header types, ignoring the automatic header detection, if a ``CSV`` with a ``# header`` row is passed. The ``# header`` row should be the first row of the CSV and defines columns according to the following list (see examples below):

- ``d``: ``DoubleColumn``, for floating point numbers
- ``l``: ``LongColumn``, for integer numbers
- ``s``: ``StringColumn``, for text
- ``b``: ``BoolColumn``, for true/false
- ``plate``, ``well``, ``image``, ``dataset``, ``roi`` to specify objects

Automatic header detection can also be ignored if using the ``--manual_headers`` flag. If the ``# header`` is not present and this flag is used, column types will default to ``String`` (unless the column names correspond to OMERO objects such as ``image`` or ``plate``).


Examples
^^^^^^^^^

The examples below will use the default automatic column types detection behaviour. It is possible to achieve the same results (or a different desired result) by manually adding a custom ``# header`` row at the top of the CSV.

**Project / Dataset**
^^^^^^^^^^^^^^^^^^^^^^

To add a table to a Project, the ``CSV`` file needs to specify ``Dataset Name`` or ``Dataset ID``
and ``Image Name`` or ``Image ID``::

    $ omero metadata populate Project:1 --file path/to/project.csv
    
Using ``Image Name`` and ``Dataset Name``:

project.csv::

    Image Name,Dataset Name,ROI_Area,Channel_Index,Channel_Name
    img-01.png,dataset01,0.0469,1,DAPI
    img-02.png,dataset01,0.142,2,GFP
    img-03.png,dataset01,0.093,3,TRITC
    img-04.png,dataset01,0.429,4,Cy5
    

The previous example will create an OMERO.table linked to the Project as follows with
a new ``Image`` column with IDs:

========== ============ ======== ============= ============ =====
Image Name Dataset Name ROI_Area Channel_Index Channel_Name Image
========== ============ ======== ============= ============ =====
img-01.png dataset01    0.0469   1             DAPI         36638
img-02.png dataset01    0.142    2             GFP          36639
img-03.png dataset01    0.093    3             TRITC        36640
img-04.png dataset01    0.429    4             Cy5          36641
========== ============ ======== ============= ============ =====

Note: equivalent to adding ``# header s,s,d,l,s`` row to the top of the ``project.csv`` for manual definition.

Using ``Image ID`` and ``Dataset ID``:

project.csv::

    image id,Dataset ID,ROI_Area,Channel_Index,Channel_Name
    36638,101,0.0469,1,DAPI
    36639,101,0.142,2,GFP
    36640,101,0.093,3,TRITC
    36641,101,0.429,4,Cy5


The previous example will create an OMERO.table linked to the Project as follows with
a new ``Image Name`` column with Names:

===== ======= ======== ============= ============ ==========
Image Dataset ROI_Area Channel_Index Channel_Name Image Name
===== ======= ======== ============= ============ ==========
36638 101     0.0469   1             DAPI         img-01.png 
36639 101     0.142    2             GFP          img-02.png 
36640 101     0.093    3             TRITC        img-03.png 
36641 101     0.429    4             Cy5          img-04.png
===== ======= ======== ============= ============ ==========

If the target is a Dataset instead of a Project, the ``Dataset Name`` column is not needed.

Note: equivalent to adding ``# header image,dataset,d,l,s`` row to the top of the ``project.csv`` for manual definition.

**Screen / Plate**
^^^^^^^^^^^^^^^^^^^

To add a table to a Screen, the ``CSV`` file needs to specify ``Plate`` name and ``Well``.
If a ``# header`` is specified, column types must be ``well`` and ``plate``::

    $ omero metadata populate Screen:1 --file path/to/screen.csv

screen.csv::

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

Note: equivalent to adding ``# header well,plate,s,d,l,d`` row to the top of the ``screen.csv`` for manual definition.

**ROIs**
^^^^^^^^^

If the target is an Image or a Dataset, a ``CSV`` with ROI-level or Shape-level data can be used to create an
``OMERO.table`` (bulk annotation) as a ``File Annotation`` linked to the target object.
If there is an ``roi`` column (header type ``roi``) containing ROI IDs, an ``Roi Name``
column will be appended automatically (see example below). If a column of Shape IDs named ``shape``
of type ``l`` is included, the Shape IDs will be validated (and set to -1 if invalid).
Also if an ``image`` column of Image IDs is included, an ``Image Name`` column will be added.
NB: Columns of type ``shape`` aren't yet supported on the OMERO.server::

    $ omero metadata populate Image:1 --file path/to/image.csv

image.csv::

    Roi,shape,object,probability,area
    501,1066,1,0.8,250
    502,1067,2,0.9,500
    503,1068,3,0.2,25
    503,1069,4,0.8,400
    503,1070,5,0.5,200
    

This will create an OMERO.table linked to the Image like this:

=== ===== ====== =========== ==== ========
Roi shape object probability area Roi Name
=== ===== ====== =========== ==== ========
501 1066  1      0.8         250  Sample1
502 1067  2      0.9         500  Sample2
503 1068  3      0.2         25   Sample3
503 1069  4      0.8         400  Sample3
503 1070  5      0.5         200  Sample3
=== ===== ====== =========== ==== ========

Note: equivalent to adding ``# header roi,l,l,d,l`` row to the top of the ``image.csv`` for manual definition.

Alternatively, if the target is an Image, the ROI input column can be
``Roi Name`` (with type ``s``), and an ``roi`` type column will be appended containing ROI IDs.
In this case, it is required that ROIs on the Image in OMERO have the ``Name`` attribute set.

Note that the ROI-level data from an ``OMERO.table`` is not visible
in the OMERO.web UI right-hand panel under the ``Tables`` tab,
but the table can be visualized by clicking the "eye" on the bulk annotation attachment on the Image.

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

2018-2022, The Open Microscopy Environment and Glencoe Software, Inc
