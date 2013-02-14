# -*- coding: utf-8 -*-
import datetime
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

    def test_sdf_file_hdr_record_size(self):
        self.assertEqual(self.sdf_hdr['file_hdr']['record_size'],64)

    def test_sdf_file_hdr_sdf_revision(self):
        self.assertEqual(self.sdf_hdr['file_hdr']['sdf_revision'],2)

    def test_sdf_file_hdr_application(self):
        self.assertEqual(self.sdf_hdr['file_hdr']['application'],'HP 35670A')

    def test_sdf_file_hdr_measurement_start_datetime(self):
        self.assertEqual(self.sdf_hdr['file_hdr']['measurement_start_datetime'],
                datetime.datetime(2013, 2, 13, 9, 8))

    def test_sdf_file_hdr_application_version(self):
        self.assertEqual(self.sdf_hdr['file_hdr']['application_version'],
                'A.01.11')

    def test_sdf_file_hdr_num_data_hdr_records(self):
        self.assertEqual(self.sdf_hdr['file_hdr']['num_data_hdr_records'],1)

    def test_sdf_file_hdr_num_vector_hdr_records(self):
        self.assertEqual(self.sdf_hdr['file_hdr']['num_vector_hdr_records'],1)

    def test_sdf_file_hdr_num_channel_hdr_records(self):
        self.assertEqual(self.sdf_hdr['file_hdr']['num_channel_hdr_records'],2)

    def test_sdf_file_hdr_num_unique_records(self):
        self.assertEqual(self.sdf_hdr['file_hdr']['num_unique_records'],1)

    def test_sdf_file_hdr_num_scan_struct_records(self):
        self.assertEqual(self.sdf_hdr['file_hdr']['num_scan_struct_records'],1)

    def test_sdf_file_hdr_num_xdata_records(self):
        self.assertEqual(self.sdf_hdr['file_hdr']['num_xdata_records'],0)

    def test_sdf_file_hdr_offset_data_hdr_record(self):
        self.assertTrue('offset_data_hdr_record' in self.sdf_hdr['file_hdr'])
        self.assertEqual(self.sdf_hdr['file_hdr']['offset_data_hdr_record'],206)

    def test_sdf_file_hdr_offset_vector_record(self):
        self.assertTrue('offset_vector_record' in self.sdf_hdr['file_hdr'])
        self.assertEqual(self.sdf_hdr['file_hdr']['offset_vector_record'],340)

    def test_sdf_file_hdr_offset_channel_record(self):
        self.assertTrue('offset_channel_record' in self.sdf_hdr['file_hdr'])
        self.assertEqual(self.sdf_hdr['file_hdr']['offset_channel_record'],358)

    def test_sdf_file_hdr_offset_unique_record(self):
        self.assertTrue('offset_unique_record' in self.sdf_hdr['file_hdr'])
        self.assertEqual(self.sdf_hdr['file_hdr']['offset_unique_record'],742)

    def test_sdf_file_hdr_offset_scan_struct_record(self):
        self.assertTrue('offset_scan_struct_record' in self.sdf_hdr['file_hdr'])
        self.assertEqual(self.sdf_hdr['file_hdr']['offset_scan_struct_record'],1264)

    def test_sdf_file_hdr_offset_xdata_record(self):
        # Since a Python dictionary will return -1 if a key does not exist
        # I had to add a test to make sure that the key does in fact exist
        # I wouldn't have discovered this without writing the test first.
        # TDD actually provided some value!
        self.assertTrue('offset_xdata_record' in self.sdf_hdr['file_hdr'])
        self.assertEqual(self.sdf_hdr['file_hdr']['offset_xdata_record'],-1)

    def test_sdf_file_hdr_offset_ydata_record(self):
        self.assertTrue('offset_ydata_record' in self.sdf_hdr['file_hdr'])
        self.assertEqual(self.sdf_hdr['file_hdr']['offset_ydata_record'],1304)

    def test_sdf_meas_hdr_record_size(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['record_size'],140)

    def test_sdf_meas_hdr_offset_unique_record(self):
        self.assertTrue('offset_unique_record' in self.sdf_hdr['meas_hdr'])
        self.assertEqual(self.sdf_hdr['meas_hdr']['offset_unique_record'],-1)

    def test_sdf_meas_hdr_block_size(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['block_size'],4096)

    def test_sdf_meas_hdr_zoom_mode_on(self):
        self.assertFalse(self.sdf_hdr['meas_hdr']['zoom_mode_on'])

    def test_sdf_meas_hdr_start_freq_index(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['start_freq_index'],0)

    def test_sdf_meas_hdr_stop_freq_index(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['stop_freq_index'],1600)

    def test_sdf_meas_hdr_average_type(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['average_type'],'None')

    def test_sdf_meas_hdr_average_num(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['average_num'],1)

    def test_sdf_meas_hdr_pct_overlap(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['pct_overlap'],0.0)

    def test_sdf_meas_hdr_meas_title(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['meas_title'],'')

    def test_sdf_meas_hdr_video_bw(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['video_bw'],0.0)

    def test_sdf_meas_hdr_center_freq(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['center_freq'],8192.0)

    def test_sdf_meas_hdr_span_freq(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['span_freq'],16384.0)

    def test_sdf_meas_hdr_sweep_freq(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['sweep_freq'],0.0)

    def test_sdf_meas_hdr_meas_type(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['meas_type'],'FFT measurement')

    def test_sdf_meas_hdr_real_time(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['real_time'],'Continuous')

    def test_sdf_meas_hdr_detection(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['detection'],'Sample detection')

    def test_sdf_meas_hdr_sweep_time(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['sweep_time'], 0.0)

