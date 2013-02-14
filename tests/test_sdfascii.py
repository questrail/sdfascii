# -*- coding: utf-8 -*-
import os
import unittest

import numpy as np

import sdfascii

class TestReadingSDFFormat(unittest.TestCase):

    def setUp(self):
        source_10mVrms_3kHz_directory = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'source_10mVrms_3kHz')

        sdf_file = os.path.join(source_10mVrms_3kHz_directory,
                'SDF3KHZ.DAT')

        self.sdf_hdr, self.sdf_data = sdfascii.read_sdf_file(sdf_file)

    def tearDown(self):
        pass

    def test_reading_sdf_file_identifier(self):
        self.assertTrue(self.sdf_hdr['valid_file_identifier'],
                'Invalid SDF file identifier')
