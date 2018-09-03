#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright (C) 2015 Glencoe Software, Inc. All Rights Reserved.
# Use is subject to license terms supplied in LICENSE.txt
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
   Test of the Tables service with the populate_metadata.py script

"""

from omero.testlib import ITest
import os

from omero.model import PlateI, WellI, WellSampleI, OriginalFileI
from omero.rtypes import rint, rstring, unwrap
from populate_metadata import ParsingContext
from omero.constants.namespaces import NSBULKANNOTATIONS


class TestPopulateMetadata(ITest):

    def create_csv(self, csv_filename):

        col_names = "Well,Well Type,Concentration"
        row_data = ["A1,Control,0", "A2,Treatment,10"]
        csv_file = open(csv_filename, 'w')
        try:
            csv_file.write(col_names)
            csv_file.write("\n")
            csv_file.write("\n".join(row_data))
        finally:
            csv_file.close()

    def create_plate(self, row_count, col_count):
        uuid = self.ctx.sessionUuid

        def create_well(row, column):
            well = WellI()
            well.row = rint(row)
            well.column = rint(column)
            ws = WellSampleI()
            image = self.new_image(name=uuid)
            ws.image = image
            well.addWellSample(ws)
            return well

        plate = PlateI()
        plate.name = rstring("TestPopulateMetadata%s" % uuid)
        for row in range(row_count):
            for col in range(col_count):
                well = create_well(row, col)
                plate.addWell(well)
        return self.client.sf.getUpdateService().saveAndReturnObject(plate)

    def test_populate_metadata_plate(self):
        """
            Create a small csv file, use populate_metadata.py to parse and
            attach to Plate. Then query to check table has expected content.
        """

        csv_name = "testCreate.csv"
        self.create_csv(csv_name)
        row_count = 1
        col_count = 2
        plate = self.create_plate(row_count, col_count)
        ctx = ParsingContext(self.client,
                             plate,
                             file=csv_name)
        ctx.parse()
        # Delete local temp file
        os.remove(csv_name)

        # Get file annotations
        query = """select p from Plate p
            left outer join fetch p.annotationLinks links
            left outer join fetch links.child
            where p.id=%s""" % plate.id.val
        qs = self.client.sf.getQueryService()
        plate = qs.findByQuery(query, None)
        anns = plate.linkedAnnotationList()
        # Only expect a single annotation which is a 'bulk annotation'
        assert len(anns) == 1
        table_file_ann = anns[0]
        assert unwrap(table_file_ann.getNs()) == NSBULKANNOTATIONS
        fileid = table_file_ann.file.id.val

        # Open table to check contents
        r = self.client.sf.sharedResources()
        t = r.openTable(OriginalFileI(fileid), None)
        cols = t.getHeaders()
        rows = t.getNumberOfRows()
        assert rows == row_count * col_count
        for hit in range(rows):
            row_values = [col.values[0] for col in t.read(range(len(cols)),
                                                          hit, hit+1).columns]
            assert len(row_values) == 4
            if "a1" in row_values:
                assert "Control" in row_values
            elif "a2" in row_values:
                assert "Treatment" in row_values
            else:
                assert False, "Row does not contain 'a1' or 'a2'"
