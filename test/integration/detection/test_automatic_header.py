#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 Glencoe Software, Inc. All rights reserved.
#
# This software is distributed under the terms described by the LICENSE.txt
# file you can find at the root of the distribution bundle.  If the file is
# missing please request a copy by contacting info@glencoesoftware.com

"""
   Test of the default automatic column type detection behaviour
"""

from omero_metadata.cli import MetadataControl
import pandas as pd
import tempfile


def test_detect_headers():
    d = {
        'project_name': ['a', 'b', 'c'],
        'dataset_name': ['a', 'b', 'c'],
        'plate_name': ['a', 'b', 'c'],
        'well_name': ['a', 'b', 'c'],
        'image_name': ['a', 'b', 'c'],
        'roi_name': ['a', 'b', 'c'],
        'project_id': [1, 2, 3],
        'dataset_id': [1, 2, 3],
        'plate_id': [1, 2, 3],
        'well_id': [1, 2, 3],
        'image_id': [1, 2, 3],
        'roi_id': [1, 2, 3],
        'project': [1, 2, 3],
        'dataset': [1, 2, 3],
        'plate': [1, 2, 3],
        'well': [1, 2, 3],
        'image': [1, 2, 3],
        'roi': [1, 2, 3],
        'measurement 1': [11, 22, 33],
        'measurement 2': [0.1, 0.2, 0.3],
        'measurement 3': ['a', 'b', 'c'],
        'measurement 4': [True, True, False]
    }

    df = pd.DataFrame(data=d)
    tmp = tempfile.NamedTemporaryFile()
    df.to_csv(tmp.name, index=False)
    header = MetadataControl.detect_headers(tmp.name)
    expected_header = [
        's', 's', 'plate', 'well', 's', 's',
        'l', 'dataset', 'l', 'l', 'image', 'roi',
        'l', 'dataset', 'plate', 'well', 'image', 'roi',
        'l', 'd', 's', 'b'
        ]
    assert header == expected_header
