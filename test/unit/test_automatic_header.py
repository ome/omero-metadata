#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2022 Glencoe Software, Inc. All rights reserved.
#
# This software is distributed under the terms described by the LICENSE.txt
# file you can find at the root of the distribution bundle.  If the file is
# missing please request a copy by contacting info@glencoesoftware.com


from omero.model import ScreenI, ProjectI
from omero_metadata.populate import HeaderResolver
from omero_metadata.cli import MetadataControl
import pandas as pd
import tempfile
from omero.grid import ImageColumn, LongColumn, PlateColumn, RoiColumn, \
    StringColumn, WellColumn, DoubleColumn, BoolColumn, DatasetColumn


def test_detect_headers():
    '''
    Test of the default automatic column type detection behaviour
    '''
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


class TestColumnTypes:
    '''
    To test resolved column types and column names.
    '''
    def assert_expected(
              self, target_object, column_name, header_type,
              expected_resolved_column_type, expected_resolved_column_names
              ):
        header_resolver = HeaderResolver(
            target_object, column_name, column_types=header_type)
        resolved_column_types = header_resolver.create_columns()
        for index, col in enumerate(resolved_column_types):
            assert col.__class__ == expected_resolved_column_type[index]
            assert col.name == expected_resolved_column_names[index]

    def test_plate_name_well_name(self):
        column_name = [
            'plate_name', 'well_name', 'measurement 1',
            'measurement 2', 'measurement 3', 'measurement 4']

        header_type = ['plate', 'well', 'l', 'd', 's', 'b']

        # We expect populate to append 'Plate Name' and 'Well Name' at the end
        expected_resolved_column_names = [
            'Plate', 'Well', 'measurement 1', 'measurement 2', 'measurement 3',
            'measurement 4', 'Plate Name', 'Well Name']

        expected_resolved_column_type = [
            PlateColumn, WellColumn,
            LongColumn, DoubleColumn, StringColumn, BoolColumn,
            StringColumn, StringColumn]

        target_object = ScreenI(0, None)  # Target object is Screen
        self.assert_expected(
            target_object, column_name, header_type,
            expected_resolved_column_type, expected_resolved_column_names)

    def test_plate_id_well_id(self):
        column_name = [
            'plate_id', 'well_id', 'measurement 1',
            'measurement 2', 'measurement 3', 'measurement 4']

        # plate_id = 'l' since 'plate' header type is not supported for plateid
        header_type = ['l', 'l', 'l', 'd', 's', 'b']

        expected_resolved_column_names = [
            'plate_id', 'well_id', 'measurement 1', 'measurement 2',
            'measurement 3', 'measurement 4']

        expected_resolved_column_type = [
            LongColumn, LongColumn,
            LongColumn, DoubleColumn, StringColumn, BoolColumn]

        target_object = ScreenI(0, None)  # Target object is Screen

        self.assert_expected(
            target_object, column_name, header_type,
            expected_resolved_column_type, expected_resolved_column_names)

    def test_plate_well(self):
        column_name = [
            'plate', 'well', 'measurement 1',
            'measurement 2', 'measurement 3', 'measurement 4']

        header_type = ['plate', 'well', 'l', 'd', 's', 'b']

        expected_resolved_column_names = [
            'Plate', 'Well', 'measurement 1', 'measurement 2', 'measurement 3',
            'measurement 4', 'Plate Name', 'Well Name']

        expected_resolved_column_type = [
            PlateColumn, WellColumn,
            LongColumn, DoubleColumn, StringColumn, BoolColumn,
            StringColumn, StringColumn]

        target_object = ScreenI(0, None)  # Target object is Screen

        self.assert_expected(
            target_object, column_name, header_type,
            expected_resolved_column_type, expected_resolved_column_names)

    def test_dataset_name_image_name(self):
        '''
        In the case column name is 'Image Name' (case sensitive),
        specific behaviour is executed.
        '''
        column_name = [
            'dataset_name', 'Image Name', 'measurement 1',
            'measurement 2', 'measurement 3', 'measurement 4']

        header_type = ['s', 's', 'l', 'd', 's', 'b']

        expected_resolved_column_names = [
            'dataset_name', 'Image Name', 'measurement 1', 'measurement 2',
            'measurement 3', 'measurement 4', 'Image']

        expected_resolved_column_type = [
            StringColumn, StringColumn,
            LongColumn, DoubleColumn, StringColumn, BoolColumn, ImageColumn]

        target_object = ProjectI(0, None)  # Target object is Project

        self.assert_expected(
            target_object, column_name, header_type,
            expected_resolved_column_type, expected_resolved_column_names)

    def test_dataset_id_image_id(self):
        column_name = [
            'dataset_id', 'image_id', 'measurement 1',
            'measurement 2', 'measurement 3', 'measurement 4']

        header_type = ['dataset', 'image', 'l', 'd', 's', 'b']

        expected_resolved_column_names = [
            'Dataset', 'Image', 'measurement 1', 'measurement 2',
            'measurement 3', 'measurement 4', 'Image Name']

        expected_resolved_column_type = [
            DatasetColumn, ImageColumn,
            LongColumn, DoubleColumn, StringColumn, BoolColumn, StringColumn]

        target_object = ProjectI(0, None)  # Target object is Project

        self.assert_expected(
            target_object, column_name, header_type,
            expected_resolved_column_type, expected_resolved_column_names)

    def test_dataset_image(self):
        column_name = [
            'dataset', 'image', 'measurement 1',
            'measurement 2', 'measurement 3', 'measurement 4']

        header_type = ['dataset', 'image', 'l', 'd', 's', 'b']

        expected_resolved_column_names = [
            'Dataset', 'Image', 'measurement 1', 'measurement 2',
            'measurement 3', 'measurement 4', 'Image Name', ]

        expected_resolved_column_type = [
            DatasetColumn, ImageColumn,
            LongColumn, DoubleColumn, StringColumn, BoolColumn, StringColumn]

        target_object = ProjectI(0, None)  # Target object is Project

        self.assert_expected(
            target_object, column_name, header_type,
            expected_resolved_column_type, expected_resolved_column_names)

    def test_roi(self):
        column_name = [
            'image', 'roi', 'measurement 1',
            'measurement 2', 'measurement 3', 'measurement 4']

        header_type = ['image', 'roi', 'l', 'd', 's', 'b']

        expected_resolved_column_names = [
            'Image', 'Roi', 'measurement 1', 'measurement 2',
            'measurement 3', 'measurement 4', 'Image Name', 'Roi Name']

        expected_resolved_column_type = [
            ImageColumn, RoiColumn,
            LongColumn, DoubleColumn, StringColumn, BoolColumn,
            StringColumn, StringColumn]

        target_object = ProjectI(0, None)  # Target object is Project

        self.assert_expected(
            target_object, column_name, header_type,
            expected_resolved_column_type, expected_resolved_column_names)
