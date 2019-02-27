#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   Test of ROI mask utils

   Copyright (C) 2019 University of Dundee. All rights reserved.
   Use is subject to license terms supplied in LICENSE.txt
"""
from omero.rtypes import unwrap
import numpy as np
import pytest

from omero_metadata import (
    mask_from_binary_image,
    masks_from_label_image,
)


@pytest.fixture
def binary_image():
    return np.array([
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 0],
    ])


@pytest.fixture
def label_image():
    return np.array([
        [0, 0, 0, 2],
        [0, 1, 1, 0],
        [0, 1, 2, 0],
        [0, 0, 0, 0],
    ])


class TestMaskUtils(object):

    @pytest.mark.parametrize('args', [
        {},
        {'rgba': (255, 128, 64, 128), 'z': 1, 'c': 2, 't': 3, 'text': 'test'}
    ])
    def test_mask_from_binary_image(self, binary_image, args):
        mask = mask_from_binary_image(binary_image, **args)

        assert unwrap(mask.getWidth()) == 2
        assert unwrap(mask.getHeight()) == 2
        assert unwrap(mask.getX()) == 1
        assert unwrap(mask.getY()) == 1

        if args:
            assert unwrap(mask.getTheZ()) == 1
            assert unwrap(mask.getTheC()) == 2
            assert unwrap(mask.getTheT()) == 3
            assert unwrap(mask.getTextValue()) == 'test'
        else:
            assert unwrap(mask.getTheZ()) is None
            assert unwrap(mask.getTheC()) is None
            assert unwrap(mask.getTheT()) is None
            assert unwrap(mask.getTextValue()) is None

    @pytest.mark.parametrize('args', [
        {},
        {'rgba': (255, 128, 64, 128), 'z': 1, 'c': 2, 't': 3, 'text': 'test'}
    ])
    def test_masks_from_label_image(self, label_image, args):
        masks = masks_from_label_image(label_image, **args)
        expected_whxy = (
            (2, 2, 1, 1),
            (2, 3, 2, 0),
        )

        assert len(masks) == 2

        for i, mask in enumerate(masks):
            assert unwrap(mask.getWidth()) == expected_whxy[i][0]
            assert unwrap(mask.getHeight()) == expected_whxy[i][1]
            assert unwrap(mask.getX()) == expected_whxy[i][2]
            assert unwrap(mask.getY()) == expected_whxy[i][3]

            if args:
                assert unwrap(mask.getTheZ()) == 1
                assert unwrap(mask.getTheC()) == 2
                assert unwrap(mask.getTheT()) == 3
                assert unwrap(mask.getTextValue()) == 'test'
            else:
                assert unwrap(mask.getTheZ()) is None
                assert unwrap(mask.getTheC()) is None
                assert unwrap(mask.getTheT()) is None
                assert unwrap(mask.getTextValue()) is None
