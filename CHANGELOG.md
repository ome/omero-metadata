0.11.1
------

* Reduce logging level of post_process statement ([#78](https://github.com/ome/omero-metadata/pull/78))

0.11.0
------

* Add support for column type auto-detection using pandas ([#67](https://github.com/ome/omero-metadata/pull/67), [#71](https://github.com/ome/omero-metadata/pull/67), [#72](https://github.com/ome/omero-metadata/pull/72), [#75](https://github.com/ome/omero-metadata/pull/75), [#77](https://github.com/ome/omero-metadata/pull/77))
* Skip empty rows when reading CSV files ([#70](https://github.com/ome/omero-metadata/pull/70))

0.10.0
------

* Populate metadata supports ROIs and Shapes when target is a Dataset

0.9.0
-----

* Add support for specifying the table name in ParsingContext

0.8.2
-----

* Pass allow-nan to all contexts

0.8.1
-----

* Do not require ROI.name if ROI is specified by ID
* Use Roi for the name of the RoiColumn

0.8.0
-----

* Add --allow-nan option to handle missing values in Double/Float columns

0.7.1
-----

* Close callbacks

0.7.0
-----

* Add new `deletebulkanns` commands for deleting all bulk annotations of a target

0.6.0
-----

* Add support for image-level OMERO.table population with ROI-level data

0.5.1
-----

* Deprecate `--report` option in `omero metadata populate` subcommand in favor or `-v/-q`
* Use GitHub actions

0.5.0
-----

* Drop support for Python 2

0.4.1
-----

* Expand README to describe the usage of the populate command
* Remove Well/Plate warnings when populating a Project/Dataset

0.4.0
-----

* Rename imports to omero_metadata.{cli,populate}
* Handle change in table closing semantics

0.3.1
-----

* Allow to filter CSV annotation file and populate only a Dataset or a Plate

0.3.0
-----

* Drop support for Python 2.6
* Unify naming of the Image column in OMERO.tables
* Fix CLI metadata populate --context deletemap --dry-run behavior
* Propagate delete options in DeleteMapAnnotationContext
* Added bulk annotations for Projects and Datasets
* Changed csv parsing to proceed line-by-line (streaming)


0.2.2
-----

* Update the source code to be flake8 compliant
* Activate the metadata and table integration tests in Travis

0.2.1
-----

This is the first release deployed to PyPI

0.2.0
-----

This release contains the metadata code matching the state of OMERO 5.4.7.

* Add metadata code filtered from the develop branch of
  openmicroscopy/openmicroscopy
* Remove OMERO_DEV_PLUGINS variable
* Add infrastructure for releasing the module to PyPI
* Activate Travis CI for running the integration tests using omero-test-infra

0.1.0
-----

* Filter metadata code from the metadata53 branch of
  openmicroscopy/openmicroscopy
