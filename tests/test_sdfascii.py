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

        ascii_ydata_file = os.path.join(source_10mVrms_3kHz_directory,
                                        'ASCII3KH.TXT')

        self.sdf_hdr, self.sdf_data = sdfascii.read_sdf_file(sdf_file)

        self.ascii_ydata = np.loadtxt(ascii_ydata_file)

    def tearDown(self):
        pass

    def test_reading_sdf_file_identifier(self):
        self.assertTrue(self.sdf_hdr['valid_file_identifier'],
                        'Invalid SDF file identifier')

    def test_sdf_file_hdr_record_size(self):
        self.assertEqual(self.sdf_hdr['file_hdr']['record_size'], 64)

    def test_sdf_file_hdr_sdf_revision(self):
        self.assertEqual(self.sdf_hdr['file_hdr']['sdf_revision'], 2)

    def test_sdf_file_hdr_application(self):
        self.assertEqual(self.sdf_hdr['file_hdr']['application'], 'HP 35670A')

    def test_sdf_file_hdr_measurement_start_datetime(self):
        self.assertEqual(
            self.sdf_hdr['file_hdr']['measurement_start_datetime'],
            datetime.datetime(2013, 2, 13, 9, 8))

    def test_sdf_file_hdr_application_version(self):
        self.assertEqual(
            self.sdf_hdr['file_hdr']['application_version'],
            'A.01.11')

    def test_sdf_file_hdr_num_data_hdr_records(self):
        self.assertEqual(self.sdf_hdr['file_hdr']['num_data_hdr_records'], 1)

    def test_sdf_file_hdr_num_vector_hdr_records(self):
        self.assertEqual(self.sdf_hdr['file_hdr']['num_vector_hdr_records'], 1)

    def test_sdf_file_hdr_num_channel_hdr_records(self):
        self.assertEqual(self.sdf_hdr['file_hdr']['num_channel_hdr_records'],
                         2)

    def test_sdf_file_hdr_num_unique_records(self):
        self.assertEqual(self.sdf_hdr['file_hdr']['num_unique_records'], 1)

    def test_sdf_file_hdr_num_scan_struct_records(self):
        self.assertEqual(self.sdf_hdr['file_hdr']['num_scan_struct_records'],
                         1)

    def test_sdf_file_hdr_num_xdata_records(self):
        self.assertEqual(self.sdf_hdr['file_hdr']['num_xdata_records'], 0)

    def test_sdf_file_hdr_offset_data_hdr_record(self):
        self.assertTrue('offset_data_hdr_record' in self.sdf_hdr['file_hdr'])
        self.assertEqual(self.sdf_hdr['file_hdr']['offset_data_hdr_record'],
                         206)

    def test_sdf_file_hdr_offset_vector_record(self):
        self.assertTrue('offset_vector_record' in self.sdf_hdr['file_hdr'])
        self.assertEqual(self.sdf_hdr['file_hdr']['offset_vector_record'],
                         340)

    def test_sdf_file_hdr_offset_channel_record(self):
        self.assertTrue('offset_channel_record' in self.sdf_hdr['file_hdr'])
        self.assertEqual(self.sdf_hdr['file_hdr']['offset_channel_record'],
                         358)

    def test_sdf_file_hdr_offset_unique_record(self):
        self.assertTrue('offset_unique_record' in self.sdf_hdr['file_hdr'])
        self.assertEqual(self.sdf_hdr['file_hdr']['offset_unique_record'],
                         742)

    def test_sdf_file_hdr_offset_scan_struct_record(self):
        self.assertTrue(
            'offset_scan_struct_record' in self.sdf_hdr['file_hdr'])
        self.assertEqual(self.sdf_hdr['file_hdr']['offset_scan_struct_record'],
                         1264)

    def test_sdf_file_hdr_offset_xdata_record(self):
        # Since a Python dictionary will return -1 if a key does not exist
        # I had to add a test to make sure that the key does in fact exist
        # I wouldn't have discovered this without writing the test first.
        # TDD actually provided some value!
        self.assertTrue('offset_xdata_record' in self.sdf_hdr['file_hdr'])
        self.assertEqual(self.sdf_hdr['file_hdr']['offset_xdata_record'],
                         -1)

    def test_sdf_file_hdr_offset_ydata_record(self):
        self.assertTrue('offset_ydata_record' in self.sdf_hdr['file_hdr'])
        self.assertEqual(self.sdf_hdr['file_hdr']['offset_ydata_record'],
                         1304)

    def test_sdf_meas_hdr_record_size(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['record_size'],
                         140)

    def test_sdf_meas_hdr_offset_unique_record(self):
        self.assertTrue('offset_unique_record' in self.sdf_hdr['meas_hdr'])
        self.assertEqual(self.sdf_hdr['meas_hdr']['offset_unique_record'],
                         -1)

    def test_sdf_meas_hdr_block_size(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['block_size'], 4096)

    def test_sdf_meas_hdr_zoom_mode_on(self):
        self.assertFalse(self.sdf_hdr['meas_hdr']['zoom_mode_on'])

    def test_sdf_meas_hdr_start_freq_index(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['start_freq_index'], 0)

    def test_sdf_meas_hdr_stop_freq_index(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['stop_freq_index'], 1600)

    def test_sdf_meas_hdr_average_type(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['average_type'], 'None')

    def test_sdf_meas_hdr_average_num(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['average_num'], 1)

    def test_sdf_meas_hdr_pct_overlap(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['pct_overlap'], 0.0)

    def test_sdf_meas_hdr_meas_title(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['meas_title'], '')

    def test_sdf_meas_hdr_video_bw(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['video_bw'], 0.0)

    def test_sdf_meas_hdr_center_freq(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['center_freq'], 8192.0)

    def test_sdf_meas_hdr_span_freq(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['span_freq'], 16384.0)

    def test_sdf_meas_hdr_sweep_freq(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['sweep_freq'], 0.0)

    def test_sdf_meas_hdr_meas_type(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['meas_type'],
                         'FFT measurement')

    def test_sdf_meas_hdr_real_time(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['real_time'], 'Continuous')

    def test_sdf_meas_hdr_detection(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['detection'],
                         'Sample detection')

    def test_sdf_meas_hdr_sweep_time(self):
        self.assertEqual(self.sdf_hdr['meas_hdr']['sweep_time'], 0.0)

    def test_sdf_data_hdr_record_size(self):
        self.assertEqual(self.sdf_hdr['data_hdr'][0]['record_size'], 134)

    def test_sdf_data_hdr_offset_unique_record(self):
        self.assertTrue('offset_unique_record' in self.sdf_hdr['data_hdr'][0])
        self.assertEqual(self.sdf_hdr['data_hdr'][0]['offset_unique_record'],
                         -1)

    def test_sdf_data_hdr_data_title(self):
        self.assertEqual(self.sdf_hdr['data_hdr'][0]['data_title'], 'Pwr Spec')

    def test_sdf_data_hdr_domain(self):
        self.assertEqual(self.sdf_hdr['data_hdr'][0]['domain'],
                         'Frequency domain')

    def test_sdf_data_hdr_data_type(self):
        self.assertEqual(self.sdf_hdr['data_hdr'][0]['data_type'],
                         'Auto-power spectrum')

    def test_sdf_data_hdr_num_points(self):
        self.assertEqual(self.sdf_hdr['data_hdr'][0]['num_points'], 2049)

    def test_sdf_data_hdr_last_valid_index(self):
        self.assertEqual(self.sdf_hdr['data_hdr'][0]['last_valid_index'], 2048)

    def test_sdf_data_hdr_x_resolution_type(self):
        self.assertTrue('x_resolution_type' in self.sdf_hdr['data_hdr'][0])
        self.assertEqual(self.sdf_hdr['data_hdr'][0]['x_resolution_type'],
                         'Linear')

    def test_sdf_data_hdr_x_data_type(self):
        self.assertTrue('x_data_type' in self.sdf_hdr['data_hdr'][0])
        self.assertEqual(self.sdf_hdr['data_hdr'][0]['x_data_type'], 'float')

    def test_sdf_data_hdr_x_per_point(self):
        self.assertEqual(self.sdf_hdr['data_hdr'][0]['x_per_point'], 0)

    def test_sdf_data_hdr_y_data_type(self):
        self.assertTrue('y_data_type' in self.sdf_hdr['data_hdr'][0])
        self.assertEqual(self.sdf_hdr['data_hdr'][0]['y_data_type'], 'float')

    def test_sdf_data_hdr_y_per_point(self):
        self.assertEqual(self.sdf_hdr['data_hdr'][0]['y_per_point'], 1)

    def test_sdf_data_hdr_y_is_complex(self):
        self.assertFalse(self.sdf_hdr['data_hdr'][0]['y_is_complex'])

    def test_sdf_data_hdr_y_is_normalized(self):
        self.assertFalse(self.sdf_hdr['data_hdr'][0]['y_is_normalized'])

    def test_sdf_data_hdr_y_is_power_data(self):
        self.assertFalse(self.sdf_hdr['data_hdr'][0]['y_is_power_data'])

    def test_sdf_data_hdr_y_is_valid(self):
        self.assertFalse(self.sdf_hdr['data_hdr'][0]['y_is_valid'])

    def test_sdf_data_hdr_first_vector_record_num(self):
        self.assertEqual(
            self.sdf_hdr['data_hdr'][0]['first_vector_record_num'], 0)

    def test_sdf_data_hdr_total_rows(self):
        self.assertEqual(self.sdf_hdr['data_hdr'][0]['total_rows'], 1)

    def test_sdf_data_hdr_total_cols(self):
        self.assertEqual(self.sdf_hdr['data_hdr'][0]['total_cols'], 1)

    def test_sdf_data_hdr_xunit(self):
        self.assertEqual(self.sdf_hdr['data_hdr'][0]['xunit']['label'], 'Hz')
        self.assertAlmostEqual(
            self.sdf_hdr['data_hdr'][0]['xunit']['factor'], 6.28318977)
        self.assertEqual(self.sdf_hdr['data_hdr'][0]['xunit']['mass'], 0)
        self.assertEqual(self.sdf_hdr['data_hdr'][0]['xunit']['length'], 0)
        self.assertEqual(self.sdf_hdr['data_hdr'][0]['xunit']['time'], -2)
        self.assertEqual(self.sdf_hdr['data_hdr'][0]['xunit']['current'], 0)
        self.assertEqual(
            self.sdf_hdr['data_hdr'][0]['xunit']['temperature'], 0)
        self.assertEqual(
            self.sdf_hdr['data_hdr'][0]['xunit']['luminal_intensity'], 0)
        self.assertEqual(self.sdf_hdr['data_hdr'][0]['xunit']['mole'], 0)
        self.assertEqual(
            self.sdf_hdr['data_hdr'][0]['xunit']['plane_angle'], 2)

    def test_sdf_data_hdr_y_unit_valid(self):
        self.assertFalse(self.sdf_hdr['data_hdr'][0]['y_unit_valid'])

    def test_sdf_data_hdr_yunit(self):
        self.assertEqual(self.sdf_hdr['data_hdr'][0]['yunit']['label'], '')
        self.assertAlmostEqual(
            self.sdf_hdr['data_hdr'][0]['yunit']['factor'], 1)
        self.assertEqual(self.sdf_hdr['data_hdr'][0]['yunit']['mass'], 0)
        self.assertEqual(self.sdf_hdr['data_hdr'][0]['yunit']['length'], 0)
        self.assertEqual(self.sdf_hdr['data_hdr'][0]['yunit']['time'], 0)
        self.assertEqual(self.sdf_hdr['data_hdr'][0]['yunit']['current'], 0)
        self.assertEqual(
            self.sdf_hdr['data_hdr'][0]['yunit']['temperature'], 0)
        self.assertEqual(
            self.sdf_hdr['data_hdr'][0]['yunit']['luminal_intensity'], 0)
        self.assertEqual(self.sdf_hdr['data_hdr'][0]['yunit']['mole'], 0)
        self.assertEqual(
            self.sdf_hdr['data_hdr'][0]['yunit']['plane_angle'], 0)

    def test_sdf_data_hdr_abscissa_first_x(self):
        self.assertEqual(self.sdf_hdr['data_hdr'][0]['abscissa_first_x'], 0.0)

    def test_sdf_data_hdr_abscissa_delta_x(self):
        self.assertEqual(self.sdf_hdr['data_hdr'][0]['abscissa_delta_x'], 8.0)

    def test_sdf_data_hdr_scan_data(self):
        self.assertFalse(self.sdf_hdr['data_hdr'][0]['scan_data'])

    def test_sdf_data_hdr_window_applied(self):
        self.assertTrue(self.sdf_hdr['data_hdr'][0]['window_applied'])

    def test_sdf_vector_hdr_record_size(self):
        self.assertEqual(self.sdf_hdr['vector_hdr'][0]['record_size'], 18)

    def test_sdf_vector_hdr_unique_record_offset(self):
        self.assertTrue(
            'offset_unique_record' in self.sdf_hdr['vector_hdr'][0])
        self.assertEqual(
            self.sdf_hdr['vector_hdr'][0]['offset_unique_record'], -1)

    def test_sdf_vector_hdr_channel_record(self):
        self.assertEqual(self.sdf_hdr['vector_hdr'][0]['channel_record'][0], 0)
        self.assertEqual(
            self.sdf_hdr['vector_hdr'][0]['channel_record'][1], -1)

    def test_sdf_vector_hdr_channel_power(self):
        self.assertEqual(
            self.sdf_hdr['vector_hdr'][0]['channel_power_48x'][0], 96)
        self.assertEqual(
            self.sdf_hdr['vector_hdr'][0]['channel_power_48x'][1], 0)

    def test_sdf_channel_hdr_record_size(self):
        self.assertEqual(self.sdf_hdr['channel_hdr'][0]['record_size'], 192)
        self.assertEqual(self.sdf_hdr['channel_hdr'][1]['record_size'], 192)

    def test_sdf_channel_hdr_unique_record_offset(self):
        self.assertTrue(
            'offset_unique_record' in self.sdf_hdr['channel_hdr'][0])
        self.assertEqual(
            self.sdf_hdr['channel_hdr'][0]['offset_unique_record'], -1)
        self.assertTrue(
            'offset_unique_record' in self.sdf_hdr['channel_hdr'][1])
        self.assertEqual(
            self.sdf_hdr['channel_hdr'][1]['offset_unique_record'], -1)

    def test_sdf_channel_hdr_channel_label(self):
        self.assertEqual(
            self.sdf_hdr['channel_hdr'][0]['channel_label'], 'Chan  1')
        self.assertEqual(
            self.sdf_hdr['channel_hdr'][1]['channel_label'], 'Chan  1')

    def test_sdf_channel_hdr_module_id(self):
        self.assertEqual(self.sdf_hdr['channel_hdr'][0]['module_id'],
                         'HP35670A')
        self.assertEqual(self.sdf_hdr['channel_hdr'][1]['module_id'],
                         'HP35670A')

    def test_sdf_channel_hdr_serial_number(self):
        self.assertEqual(self.sdf_hdr['channel_hdr'][0]['serial_number'],
                         'MY42506778')
        self.assertEqual(self.sdf_hdr['channel_hdr'][1]['serial_number'],
                         'MY42506778')

    def test_sdf_channel_hdr_window(self):
        self.assertEqual(
            self.sdf_hdr['channel_hdr'][0]['window']['window_type'],
            'Flat Top')
        self.assertEqual(
            self.sdf_hdr['channel_hdr'][0]['window']['correction_mode'],
            'Correction not applied')
        self.assertAlmostEqual(self.sdf_hdr['channel_hdr'][0]['window']['bw'],
                               3.81935954)
        self.assertEqual(
            self.sdf_hdr['channel_hdr'][0]['window']['time_const'], 0.0)
        self.assertEqual(
            self.sdf_hdr['channel_hdr'][0]['window']['trunc'], 0.0)
        self.assertAlmostEqual(
            self.sdf_hdr['channel_hdr'][0]['window']['wide_band_corr'],
            2.39823508262)
        self.assertAlmostEqual(
            self.sdf_hdr['channel_hdr'][0]['window']['narrow_band_corr'],
            4.68691444)

    def test_sdf_channel_hdr_weight(self):
        self.assertEqual(self.sdf_hdr['channel_hdr'][0]['weight'],
                         'No weighting')

    def test_sdf_channel_hdr_delay(self):
        self.assertEqual(self.sdf_hdr['channel_hdr'][0]['delay'], 0.0)

    def test_sdf_channel_hdf_range(self):
        self.assertAlmostEqual(self.sdf_hdr['channel_hdr'][0]['range'],
                               -32.943313598)

    def test_sdf_channel_hdr_direction(self):
        self.assertEqual(self.sdf_hdr['channel_hdr'][0]['direction'], 'Z')

    def test_sdf_channel_hdr_point_num(self):
        self.assertEqual(self.sdf_hdr['channel_hdr'][0]['point_num'], 1)

    def test_sdf_channel_hdr_coupling(self):
        self.assertEqual(self.sdf_hdr['channel_hdr'][0]['coupling'], 'DC')

    def test_sdf_channel_hdr_overload(self):
        self.assertFalse(self.sdf_hdr['channel_hdr'][1]['overloaded'])

    def test_sdf_channel_hdr_int_label(self):
        self.assertEqual(self.sdf_hdr['channel_hdr'][0]['int_label'], 'V')

    def test_sdf_channel_hdr_eng_unit(self):
        self.assertEqual(self.sdf_hdr['channel_hdr'][0]['eng_unit']['label'],
                         'V')
        self.assertAlmostEqual(
            self.sdf_hdr['channel_hdr'][0]['eng_unit']['factor'], 1)
        self.assertEqual(self.sdf_hdr['channel_hdr'][0]['eng_unit']['mass'], 2)
        self.assertEqual(
            self.sdf_hdr['channel_hdr'][0]['eng_unit']['length'], 4)
        self.assertEqual(
            self.sdf_hdr['channel_hdr'][0]['eng_unit']['time'], -6)
        self.assertEqual(
            self.sdf_hdr['channel_hdr'][0]['eng_unit']['current'], -2)
        self.assertEqual(
            self.sdf_hdr['channel_hdr'][0]['eng_unit']['temperature'], 0)
        self.assertEqual(
            self.sdf_hdr['channel_hdr'][0]['eng_unit']['luminal_intensity'], 0)
        self.assertEqual(self.sdf_hdr['channel_hdr'][0]['eng_unit']['mole'], 0)
        self.assertEqual(
            self.sdf_hdr['channel_hdr'][0]['eng_unit']['plane_angle'], 0)

    def test_sdf_channel_hdr_int_2_eng_unit(self):
        self.assertEqual(self.sdf_hdr['channel_hdr'][0]['int_2_eng_unit'], 1.0)

    def test_sdf_channel_hdr_input_impedance(self):
        self.assertEqual(
            self.sdf_hdr['channel_hdr'][0]['input_impedance'], 50.0)

    def test_sdf_channel_hdr_channel_attribute(self):
        self.assertEqual(
            self.sdf_hdr['channel_hdr'][0]['channel_attribute'],
            'No attribute')

    def test_sdf_channel_hdr_alias_protected(self):
        self.assertTrue(self.sdf_hdr['channel_hdr'][0]['alias_protected'])

    def test_sdf_channel_hdr_digital_channel(self):
        self.assertFalse(self.sdf_hdr['channel_hdr'][0]['digital_channel'])

    def test_sdf_channel_hdr_channel_scale(self):
        self.assertEqual(self.sdf_hdr['channel_hdr'][0]['channel_scale'], 1.0)

    def test_sdf_channel_hdr_channel_offset(self):
        self.assertEqual(self.sdf_hdr['channel_hdr'][0]['channel_offset'], 0.0)

    def test_sdf_channel_hdr_gate_begin(self):
        self.assertEqual(self.sdf_hdr['channel_hdr'][0]['gate_begin'], 0.0)

    def test_sdf_channel_hdr_gate_end(self):
        self.assertEqual(self.sdf_hdr['channel_hdr'][0]['gate_end'], 0.0)

    def test_sdf_channel_hdr_user_delay(self):
        self.assertEqual(self.sdf_hdr['channel_hdr'][0]['user_delay'], 0.0)

    def test_sdf_scan_struct_record_size(self):
        self.assertEqual(self.sdf_hdr['scan_struct']['record_size'], 40)

    def test_sdf_scan_struct_num_of_scans(self):
        self.assertEqual(self.sdf_hdr['scan_struct']['num_of_scans'], 1)

    def test_sdf_scan_struct_last_scan_index(self):
        self.assertEqual(self.sdf_hdr['scan_struct']['last_scan_index'], 0)

    def test_sdf_scan_struct_scan_type(self):
        self.assertEqual(self.sdf_hdr['scan_struct']['scan_type'], 'Scan')

    def test_sdf_scan_struct_scan_var_type(self):
        self.assertEqual(self.sdf_hdr['scan_struct']['scan_var_type'], 'Float')

    def test_sdf_scan_struct_scan_unit(self):
        self.assertEqual(
            self.sdf_hdr['scan_struct']['scan_unit']['label'], 'count')
        self.assertAlmostEqual(
            self.sdf_hdr['scan_struct']['scan_unit']['factor'], 1)
        self.assertEqual(self.sdf_hdr['scan_struct']['scan_unit']['mass'], 0)
        self.assertEqual(self.sdf_hdr['scan_struct']['scan_unit']['length'], 0)
        self.assertEqual(self.sdf_hdr['scan_struct']['scan_unit']['time'], 0)
        self.assertEqual(
            self.sdf_hdr['scan_struct']['scan_unit']['current'], 0)
        self.assertEqual(
            self.sdf_hdr['scan_struct']['scan_unit']['temperature'], 0)
        self.assertEqual(
            self.sdf_hdr['scan_struct']['scan_unit']['luminal_intensity'], 0)
        self.assertEqual(self.sdf_hdr['scan_struct']['scan_unit']['mole'], 0)
        self.assertEqual(
            self.sdf_hdr['scan_struct']['scan_unit']['plane_angle'], 0)

    def test_ydata_max_value(self):
        max_value = self.sdf_data[self.sdf_data.argmax()]
        self.assertAlmostEqual(max_value, 0.01009883)

    def test_ydata(self):
        np.testing.assert_array_almost_equal(self.sdf_data, self.ascii_ydata)


class TestReadingASCIIFormat(unittest.TestCase):

    def setUp(self):
        source_10mVrms_3kHz_directory = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'source_10mVrms_3kHz')

        ascii_file_basename = os.path.join(source_10mVrms_3kHz_directory,
                                           'ASCII3KH')

        self.ascii_data = sdfascii.read_ascii_files(ascii_file_basename)

    def tearDown(self):
        pass

    def test_starting_frequency(self):
        self.assertEqual(self.ascii_data['frequency'][0], 0)

    def test_ending_frequency(self):
        self.assertEqual(self.ascii_data['frequency'][-1], 12800)

    def test_all_frequencies(self):
        frequency_answer = np.linspace(0, 12800, 1601)
        np.testing.assert_array_equal(self.ascii_data['frequency'],
                                      frequency_answer)

    def test_ydata_max_value(self):
        max_value = self.ascii_data.amplitude[
            self.ascii_data.amplitude.argmax()]
        self.assertAlmostEqual(max_value, 0.01009883)
