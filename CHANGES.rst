CHANGES
=======

0.3.0
-----

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
