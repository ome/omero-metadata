#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 University of Dundee.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
import os

from setuptools import setup


def read(fname):
    """
    Utility function to read the README file.
    :rtype : String
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


version = '0.12.1.dev0'
url = "https://github.com/ome/omero-metadata/"

setup(
    version=version,
    packages=['', 'omero_metadata', 'omero.plugins'],
    package_dir={"": "src"},
    name='omero-metadata',
    description="Metadata plugin for use in the OMERO CLI.",
    long_description=read('README.rst'),
    classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Plugins',
          'Intended Audience :: Developers',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: GNU General Public License v2 '
          'or later (GPLv2+)',
          'Natural Language :: English',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Libraries :: Python Modules',
      ],  # Get strings from
          # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    author='The Open Microscopy Team',
    author_email='ome-devel@lists.openmicroscopy.org.uk',
    license='GPL-2.0+',
    url='%s' % url,
    zip_safe=True,
    download_url='%s/v%s.tar.gz' % (url, version),
    keywords=['OMERO.CLI', 'plugin'],
    install_requires=[
        'omero-py>=5.6.0',
        'PyYAML',
        'jinja2',
        'pandas'
    ],
    python_requires='>=3',
    tests_require=[
        'omero-py>=5.17.0',
        'pytest'],
)
