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
        'measurement 1': [11, 22, 33],
        'measurement 2': [0.1, 0.2, 0.3],
        'measurement 3': ['a', 'b', 'c'],
        'measurement 4': [True, True, False],
        'measurement 5': [11, 0.1, True]
    }
    prefix_list = ['project', 'dataset', 'plate', 'well', 'image', 'roi', ]
    # Create a dictionary with every combination of headers
    # eg plate_name/platename/plate name/plate_id/plateid/plate id
    for prefix in prefix_list:
        d[f'{prefix}_name'] = ['a', 'b', 'c']
        d[f'{prefix} name'] = ['a', 'b', 'c']
        d[f'{prefix}name'] = ['a', 'b', 'c']
        d[f'{prefix}_id'] = [1, 2, 3]
        d[f'{prefix} id'] = [1, 2, 3]
        d[f'{prefix}id'] = [1, 2, 3]
        d[f'{prefix}'] = [1, 2, 3]

    df = pd.DataFrame(data=d)
    tmp = tempfile.NamedTemporaryFile()
    df.to_csv(tmp.name, index=False)
    header = MetadataControl.detect_headers(tmp.name)
    expected_header = [
        'l', 'd', 's', 'b', 's',
        's', 's', 's', 'l', 'l', 'l', 'l',
        's', 's', 's', 'dataset', 'dataset', 'dataset', 'dataset',
        'plate', 'plate', 'plate', 'l', 'l', 'l', 'plate',
        'well', 'well', 'well', 'l', 'l', 'l', 'well',
        's', 's', 's', 'image', 'image', 'image', 'image',
        's', 's', 's', 'roi', 'roi', 'roi', 'roi'
    ]
    assert header == expected_header
