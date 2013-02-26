#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
sdfascii.py

Read SDF and ASCII files created by HP/Agilent Dynamic Signal Analyzers.

**WARNING:** Currently, only supporting SDF version 2 as produced by an
Agilent 35670A DSA.
'''

# Try to future proof code so that it's Python 3.x ready
from __future__ import print_function
#from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

# Standard module imports
import datetime
import string
import struct
import sys

# Data analysis related imports
import numpy as np

def _strip_nonprintable(input_string):
    return input_string.split('\x00',1)[0]

def _convert_sdf_unit_to_dictionary(sdf_unit):
    keys = ('label', 'factor', 'mass', 'length', 'time', 'current',
            'temperature', 'luminal_intensity', 'mole', 'plane_angle')
    sdf_unit_dictionary = dict(zip(keys, sdf_unit))
    sdf_unit_dictionary['label'] = _strip_nonprintable(sdf_unit_dictionary['label'])
    return sdf_unit_dictionary

def _convert_sdf_window_to_dictionary(sdf_window):
    keys = ('window_type', 'correction_mode', 'bw', 'time_const',
            'trunc', 'wide_band_corr', 'narrow_band_corr')
    sdf_window_dictionary = dict(zip(keys, sdf_window))
    # FIXME: Add remaining window types
    window_type_decoder = {0: 'Window not applied', 1: 'Hanning',
            2: 'Flat Top', 3: 'Uniform', 4: 'Force'}
    sdf_window_dictionary['window_type'] = window_type_decoder[
            sdf_window_dictionary['window_type']]
    correction_mode_decoder = {0: 'Correction not applied',
            1: 'Narrow band correction applied',
            2: 'Wide band correction applied'}
    sdf_window_dictionary['correction_mode'] = correction_mode_decoder[
            sdf_window_dictionary['correction_mode']]
    return sdf_window_dictionary

def _read_hdr(input_hdr_filename):
    pass

def _read_txt(input_txt_filename):
    pass

def _read_x(input_x_filename):
    pass

def _read_z(input_z_filename):
    pass

def read_ascii(input_ascii_base_filename):
    pass

def _decode_sdf_file_hdr(record_size, binary_data):
    '''
    * record_size is the total size of the binary_data including the
    record_type and record_size
    * file_hdr_binary contains all the binary data for the file header
    including the record_type and record_size.
    * The HP documentation lists the binary indices starting a 1, whereas
    Python uses 0 based arrays/indices
    '''
    file_hdr = {}
    file_hdr['record_size'] = record_size
    file_hdr['sdf_revision'], = struct.unpack('>h', binary_data[6:8])
    application_code, = struct.unpack('>h', binary_data[8:10])
    application_decoder = { -1: 'HP VISTA', -2: 'HP SINE', -3: 'HP 35660A', 
            -4: 'HP 3562A, HP 3563A', -5: 'HP 3588A', -6: 'HP 3589A', -99: 'Unknown',
            1: 'HP 3566A, HP 3567A', 2: 'HP 35665A', 3: 'HP 3560A', 
            4: 'HP 89410A, HP 89440A', 7: 'HP 35635R', 8: 'HP 35654A-S1A',
            9: 'HP 3569A', 10: 'HP 35670A', 11: 'HP 3587S'}
    file_hdr['application'] = application_decoder[application_code]
    msr_year, msr_month_day, msr_hour_min = struct.unpack('>hhh', binary_data[10:16])
    msr_month, msr_day = divmod(msr_month_day, 100)
    msr_hour, msr_sec = divmod(msr_hour_min, 100)
    file_hdr['measurement_start_datetime'] = datetime.datetime(msr_year,
            msr_month, msr_day, msr_hour, msr_sec)
    file_hdr['application_version'] = _strip_nonprintable(
            struct.unpack('>8s', binary_data[16:24])[0])
    (file_hdr['num_data_hdr_records'], file_hdr['num_vector_hdr_records'],
            file_hdr['num_channel_hdr_records'], file_hdr['num_unique_records'],
            file_hdr['num_scan_struct_records'], file_hdr['num_xdata_records']) = \
                    struct.unpack('>6h', binary_data[24:36])
    (file_hdr['offset_data_hdr_record'], file_hdr['offset_vector_record'],
            file_hdr['offset_channel_record'], file_hdr['offset_unique_record'],
            file_hdr['offset_scan_struct_record'], file_hdr['offset_xdata_record'],
            file_hdr['offset_ydata_record']) = \
            struct.unpack('>7l', binary_data[36:64])

    if file_hdr['sdf_revision'] == 3:
        # Continue reading bytes 65-80 if this is SDF ver. 3
        # FIXME: Need to add the code for SDF ver. 3 in the future.
        pass

    return file_hdr

def _decode_sdf_meas_hdr(record_size, sdf_revision, binary_data):
    '''
    Decode the measurement header binary data
    '''
    meas_hdr = {}
    meas_hdr['record_size'] = record_size
    (meas_hdr['offset_unique_record'],) = \
            struct.unpack('>1l', binary_data[6:10])
    meas_hdr['block_size'], = struct.unpack('>l', binary_data[18:22])
    meas_hdr['zoom_mode_on'], = struct.unpack('>h', binary_data[22:24])
    meas_hdr['zoom_mode_on'] = bool(meas_hdr['zoom_mode_on'])
    coded_average_type, = struct.unpack('>h', binary_data[28:30])
    average_type_decoder = {0: 'None', 1: 'RMS', 2: 'RMS Exponential',
            3: 'Vector', 4: 'Vector Exponential', 5: 'Continuous Peak Hold',
            6: 'Peak'}
    meas_hdr['average_type'] = average_type_decoder[coded_average_type]
    meas_hdr['average_num'], = struct.unpack('>l', binary_data[30:34])
    meas_hdr['pct_overlap'], = struct.unpack('>f', binary_data[34:38])
    meas_hdr['meas_title'] = _strip_nonprintable(
            struct.unpack('>60s', binary_data[38:98])[0])
    meas_hdr['video_bw'], = struct.unpack('>f', binary_data[98:102])
    (meas_hdr['center_freq'], meas_hdr['span_freq'],
            meas_hdr['sweep_freq']) = \
            struct.unpack('>3d', binary_data[102:126])
    coded_meas_type, = struct.unpack('>h', binary_data[126:128])
    # FIXME: Need to add the other measurement types
    meas_type_decoder = {-99: 'Unknown measurement', 0: 'Spectrum measurement',
            1: 'Network measurement', 2: 'Swept measurement',
            3: 'FFT measurement'}
    meas_hdr['meas_type'] = meas_type_decoder[coded_meas_type]
    coded_real_time, = struct.unpack('>h', binary_data[128:130])
    real_time_decoder = {0: 'Not continuous', 1: 'Continuous'}
    meas_hdr['real_time'] = real_time_decoder[coded_real_time]
    coded_detection, = struct.unpack('>h', binary_data[130:132])
    detection_decoder = {-99: 'Unknown detection type',
            0: 'Sample detection', 1: 'Positive peak detection',
            2: 'Negative peak detection', 3: 'Rose-and-fell detection'}
    meas_hdr['detection'] = detection_decoder[coded_detection]
    meas_hdr['sweep_time'], = struct.unpack('>d', binary_data[132:140])

    if sdf_revision == 1:
        # Decode the revision 1 stuff
        # FIXME: Add rev 1 stuff later
        pass
    elif sdf_revision == 2:
        # Decode the revision 2 stuff
        (meas_hdr['start_freq_index'], meas_hdr['stop_freq_index']) = \
                struct.unpack('>2h', binary_data[24:28])
    elif sdf_revision == 3:
        # Decode the revision 3 related stuff
        # FIXME: Add rev 3 stuff later
        pass
    else:
        # SDF revision not recognized
        sys.exit('Did not recognize SDF revision')

    return meas_hdr

def _decode_sdf_data_hdr(record_size, sdf_revision, binary_data):
    '''
    Decode the data header binary data
    '''
    data_hdr = {}
    data_hdr['record_size'] = record_size
    (data_hdr['offset_unique_record'],) = \
            struct.unpack('>1l', binary_data[6:10])
    data_hdr['data_title'] = _strip_nonprintable(
            struct.unpack('>16s', binary_data[10:26])[0])
    coded_domain, = struct.unpack('>h', binary_data[26:28])
    domain_decoder = {-99: 'Unknown', 0: 'Frequency domain',
            1: 'Time domain', 2: 'Amplitude domain',
            3: 'RPM', 4: 'Order', 5: 'Channel', 6: 'Octave'}
    data_hdr['domain'] = domain_decoder[coded_domain]
    coded_data_type, = struct.unpack('>h', binary_data[28:30])
    # FIXME: Add more data_type codes
    data_type_decoder = {-99: 'Unknown', 0: 'Time',
            1: 'Linear spectrum', 2: 'Auto-power spectrum',}
    data_hdr['data_type'] = data_type_decoder[coded_data_type]
    coded_x_resolution_type, = struct.unpack('>h', binary_data[42:44])
    x_resolution_type_decoder = {0: 'Linear', 1: 'Logarithmic',
            2: 'Arbitrary, one per file', 3: 'Arbitrary, one per data type',
            4: 'Arbitrary, one per trace'}
    data_hdr['x_resolution_type'] = x_resolution_type_decoder[coded_x_resolution_type]
    coded_x_data_type, = struct.unpack('>h', binary_data[44:46])
    x_data_type_decoder = {1: 'short', 2: 'long', 3: 'float', 4: 'double'}
    data_hdr['x_data_type'] = x_data_type_decoder[coded_x_data_type]
    data_hdr['x_per_point'], = struct.unpack('>h', binary_data[46:48])
    coded_y_data_type, = struct.unpack('>h', binary_data[48:50])
    y_data_type_decoder = {1: 'short', 2: 'long', 3: 'float', 4: 'double'}
    data_hdr['y_data_type'] = y_data_type_decoder[coded_y_data_type]
    data_hdr['y_per_point'], = struct.unpack('>h', binary_data[50:52])
    data_hdr['y_is_complex'], = struct.unpack('>h', binary_data[52:54])
    data_hdr['y_is_complex'] = bool(data_hdr['y_is_complex'])
    data_hdr['y_is_normalized'], = struct.unpack('>h', binary_data[54:56])
    data_hdr['y_is_normalized'] = bool(data_hdr['y_is_complex'])
    data_hdr['y_is_power_data'], = struct.unpack('>h', binary_data[56:58])
    data_hdr['y_is_power_data'] = bool(data_hdr['y_is_complex'])
    data_hdr['y_is_valid'], = struct.unpack('>h', binary_data[58:60])
    data_hdr['y_is_valid'] = bool(data_hdr['y_is_complex'])
    data_hdr['first_vector_record_num'], = struct.unpack('>l', binary_data[60:64])
    data_hdr['total_rows'], data_hdr['total_cols'] = struct.unpack('>2h', binary_data[64:68])
    xunit = struct.unpack('>10sf8b', binary_data[68:90])
    data_hdr['xunit'] = _convert_sdf_unit_to_dictionary(xunit)
    data_hdr['y_unit_valid'], = struct.unpack('>h', binary_data[90:92])
    data_hdr['y_unit_valid'] = bool(data_hdr['y_unit_valid'])
    yunit = struct.unpack('>10sf8b', binary_data[92:114])
    data_hdr['yunit'] = _convert_sdf_unit_to_dictionary(yunit)

    if sdf_revision == 1:
        # Decode the revision 1 stuff
        # FIXME: Add rev 1 stuff later
        (data_hdr['abscissa_first_x'], data_hdr['abscissa_delta_x']) = \
                struct.unpack('>2f', binary_data[34:42])
    elif sdf_revision == 2:
        # Decode the revision 2 stuff
        (data_hdr['num_points'], data_hdr['last_valid_index']) = \
                struct.unpack('>2h', binary_data[30:34])
        (data_hdr['abscissa_first_x'], data_hdr['abscissa_delta_x']) = \
                struct.unpack('>2d', binary_data[114:130])
        data_hdr['scan_data'], = struct.unpack('>h', binary_data[130:132])
        data_hdr['scan_data'] = bool(data_hdr['scan_data'])
        data_hdr['window_applied'], = struct.unpack('>h', binary_data[132:134])
        data_hdr['window_applied'] = bool(data_hdr['window_applied'])
    elif sdf_revision == 3:
        # Decode the revision 3 related stuff
        # FIXME: Add rev 3 stuff later
        pass
    else:
        # SDF revision not recognized
        sys.exit('Did not recognize SDF revision')

    return data_hdr

def _decode_sdf_vector_hdr(record_size, sdf_revision, binary_data):
    '''
    Decode the vector header binary data
    '''
    vector_hdr = {}
    vector_hdr['record_size'] = record_size
    (vector_hdr['offset_unique_record'],) = \
            struct.unpack('>l', binary_data[6:10])
    vector_hdr['channel_record'] = struct.unpack('>2h', binary_data[10:14])
    vector_hdr['channel_power_48x'] = struct.unpack('>2h', binary_data[14:18])

    return vector_hdr

def _decode_sdf_channel_hdr(record_size, sdf_revision, binary_data):
    '''
    Decode the channel header binary data
    '''
    channel_hdr = {}
    channel_hdr['record_size'] = record_size
    (channel_hdr['offset_unique_record'],) = \
            struct.unpack('>l', binary_data[6:10])
    channel_hdr['channel_label'] = _strip_nonprintable(
            struct.unpack('>30s', binary_data[10:40])[0])
    channel_hdr['module_id'] = _strip_nonprintable(
            struct.unpack('>12s', binary_data[40:52])[0])
    channel_hdr['serial_number'] = _strip_nonprintable(
            struct.unpack('>12s', binary_data[52:64])[0])
    window = struct.unpack('>2h5f', binary_data[64:88])
    channel_hdr['window'] = _convert_sdf_window_to_dictionary(window)
    coded_weight, = struct.unpack('>h', binary_data[88:90])
    weight_decoder = {0: 'No weighting', 1: 'A-weighting',
            2: 'B-weighting', 3: 'C-weighting'}
    channel_hdr['weight'] = weight_decoder[coded_weight]
    (channel_hdr['delay'], channel_hdr['range']) = struct.unpack('>2f', binary_data[90:98])
    coded_direction, = struct.unpack('>h', binary_data[98:100])
    direction_decoder = {-9: '-TZ', -8: '-TY', -7: '-TX', -3: '-Z', -2: '-Y',
            -1: 'X', 0: 'No direction specified', 1: 'X', 2: 'Y', 3: 'Z',
            4: 'Radial', 5: 'Tangential, theta angle', 6: 'Tangential, phi angle',
            7: 'TX', 8: 'TY', 9: 'TZ'}
    channel_hdr['direction'] = direction_decoder[coded_direction]
    channel_hdr['point_num'], = struct.unpack('>h', binary_data[100:102])
    coded_coupling, = struct.unpack('>h', binary_data[102:104])
    coupling_decoder = {0: 'DC', 1: 'AC'}
    channel_hdr['coupling'] = coupling_decoder[coded_coupling]
    channel_hdr['overloaded'], = struct.unpack('>h', binary_data[104:106])
    channel_hdr['overloaded'] = bool(channel_hdr['overloaded'])
    channel_hdr['int_label'] = _strip_nonprintable(
            struct.unpack('>10s', binary_data[106:116])[0])
    eng_unit = struct.unpack('>10sf8b', binary_data[116:138])
    channel_hdr['eng_unit'] = _convert_sdf_unit_to_dictionary(eng_unit)
    channel_hdr['int_2_eng_unit'], = struct.unpack('>f', binary_data[138:142])
    channel_hdr['input_impedance'], = struct.unpack('>f', binary_data[142:146])
    coded_channel_attribute, = struct.unpack('>h', binary_data[146:148])
    channel_attribute_decoder = {-99: 'Unknown attribute', 0: 'No attribute',
            1: 'Tach attribute', 2: 'Reference attribute',
            3: 'Tach and reference attribute', 4: 'Clockwise attribute'}
    channel_hdr['channel_attribute'] = channel_attribute_decoder[coded_channel_attribute]
    channel_hdr['alias_protected'], = struct.unpack('>h', binary_data[148:150])
    channel_hdr['alias_protected'] = bool(channel_hdr['alias_protected'])
    channel_hdr['digital_channel'], = struct.unpack('>h', binary_data[150:152])
    channel_hdr['digital_channel'] = bool(channel_hdr['digital_channel'])
    (channel_hdr['channel_scale'], channel_hdr['channel_offset'],
            channel_hdr['gate_begin'], channel_hdr['gate_end'],
            channel_hdr['user_delay']) = struct.unpack('>5d', binary_data[152:192])

    return channel_hdr

def _decode_sdf_scan_struct(record_size, sdf_revision, binary_data):
    '''
    Decode the channel header binary data
    '''
    scan_struct = {}
    scan_struct['record_size'] = record_size
    scan_struct['num_of_scans'], = struct.unpack('>h', binary_data[6:8])
    scan_struct['last_scan_index'], = struct.unpack('>h', binary_data[8:10])
    coded_scan_type, = struct.unpack('>h', binary_data[10:12])
    # The HP Standard Data Foramt Utilties User's Guide shows 0 = Depth and 1 = Scan
    # However, the .DAT file created by 35670A shows 1 = Depth.
    # I'm going to believe the documentation
    scan_type_decoder = {0: 'Depth', 1: 'Scan'}
    scan_struct['scan_type'] = scan_type_decoder[coded_scan_type]
    coded_scan_var_type, = struct.unpack('>h', binary_data[12:14])
    scan_var_type_decoder = {1: 'Short', 2: 'Long', 3: 'Float',
            4: 'Double'}
    scan_struct['scan_var_type'] = scan_var_type_decoder[coded_scan_var_type]
    scan_unit = struct.unpack('>10sf8b', binary_data[14:36])
    scan_struct['scan_unit'] = _convert_sdf_unit_to_dictionary(scan_unit)

    return scan_struct

def read_sdf_file(sdf_filename):
    '''
    Read the binary SDF file.

    The SDF format is described in Appendix B of the Standard
    Data Format Utilities User's Guide.

    There are three different versions of SDF.

    '''
    sdf_hdr = {}
    sdf_hdr['valid_file_identifier'] = False
    sdf_hdr['channel_hdr'] = []  # There are 0 or more channel header records

    with open(sdf_filename, 'rb') as sdf_file:
        # Read SDF file_identfication
        file_identifier = sdf_file.read(2)
        if file_identifier == 'B\x00':
            sdf_hdr['valid_file_identifier'] = True
            sdf_file_start = sdf_file.tell()
        else:
            # Didn't find a valid file identifer, so bail out
            sys.exit('Did not find a valid file identifier.')

        # Determine record type (short) and record size (long)
        # Every record has these two special fields at the start
        record_type_size_format = '>hl'

        # Process the file header record
        file_hdr_record_type, file_hdr_record_size = struct.unpack(
                record_type_size_format,
                sdf_file.read(struct.calcsize(record_type_size_format)))
        if file_hdr_record_type == 10:
            # Found the file header record
            # Process the entire file header record including the record type
            # (short) and record size (long)
            sdf_file.seek(sdf_file.tell() - struct.calcsize(record_type_size_format))
            sdf_hdr['file_hdr'] = _decode_sdf_file_hdr(file_hdr_record_size,
                    sdf_file.read(file_hdr_record_size))
        else:
            sys.exit('Error processing SDF file; expected file header')

        # Process the measurement header record
        meas_hdr_record_type, meas_hdr_record_size = struct.unpack(record_type_size_format,
                sdf_file.read(struct.calcsize(record_type_size_format)))
        if meas_hdr_record_type == 11:
            # Found the measurement header record
            sdf_file.seek(sdf_file.tell() - struct.calcsize(record_type_size_format))
            sdf_hdr['meas_hdr'] = _decode_sdf_meas_hdr(meas_hdr_record_size,
                    sdf_hdr['file_hdr']['sdf_revision'], sdf_file.read(meas_hdr_record_size))
        else:
            sys.exit('Error processing SDF file; expected measurement header')

        # Decode the data header records
        sdf_hdr['data_hdr'] = []
        # Initialize record size to 0 until we know the answer
        data_hdr_record_size = 0
        for data_hdr_record_index in range(sdf_hdr['file_hdr']['num_data_hdr_records']):
            # Move to the start of the data header record
            sdf_file.seek(sdf_hdr['file_hdr']['offset_data_hdr_record'] +
                    data_hdr_record_index * data_hdr_record_size)
            # Read the record type and size
            data_hdr_record_type, data_hdr_record_size = struct.unpack(
                    record_type_size_format,
                    sdf_file.read(struct.calcsize(record_type_size_format)))
            if data_hdr_record_type == 12:
                # This is a data header record
                sdf_file.seek(sdf_file.tell() - struct.calcsize(record_type_size_format))
                sdf_hdr['data_hdr'].append(_decode_sdf_data_hdr(
                        data_hdr_record_size, sdf_hdr['file_hdr']['sdf_revision'],
                        sdf_file.read(data_hdr_record_size)))
            else:
                sys.exit('This should have been a data header record.')

        # Decode the vector header records
        sdf_hdr['vector_hdr'] = []
        # Initialize record size to 0 until we know the answer
        vector_hdr_record_size = 0
        for vector_hdr_record_index in range(sdf_hdr['file_hdr']['num_vector_hdr_records']):
            # Move to the start of the vector header record
            sdf_file.seek(sdf_hdr['file_hdr']['offset_vector_record'] +
                    vector_hdr_record_index * vector_hdr_record_size)
            # Read the record type and size
            vector_hdr_record_type, vector_hdr_record_size = struct.unpack(
                    record_type_size_format,
                    sdf_file.read(struct.calcsize(record_type_size_format)))
            if vector_hdr_record_type == 13:
                # This is a vector header record
                # Backup and read all of the vector header record including
                # the record type and record size
                sdf_file.seek(sdf_file.tell() - struct.calcsize(record_type_size_format))
                sdf_hdr['vector_hdr'].append(_decode_sdf_vector_hdr(
                    vector_hdr_record_size, sdf_hdr['file_hdr']['sdf_revision'],
                    sdf_file.read(vector_hdr_record_size)))
            else:
                sys.exit('This should have been a vector header record.')

        # Decode the channel header records
        sdf_hdr['channel_hdr'] = []
        # Initialize record size to 0 until we know the answer
        channel_hdr_record_size = 0
        for channel_hdr_record_index in range(sdf_hdr['file_hdr']['num_channel_hdr_records']):
            # Move to the start of the channel header record
            sdf_file.seek(sdf_hdr['file_hdr']['offset_channel_record'] +
                    channel_hdr_record_index * channel_hdr_record_size)
            # Read the record type and size
            channel_hdr_record_type, channel_hdr_record_size = struct.unpack(
                    record_type_size_format,
                    sdf_file.read(struct.calcsize(record_type_size_format)))
            if channel_hdr_record_type == 14:
                # This is a channel header record
                # Backup and read all of the channel header record including
                # the record type and record size
                sdf_file.seek(sdf_file.tell() - struct.calcsize(record_type_size_format))
                sdf_hdr['channel_hdr'].append(_decode_sdf_channel_hdr(
                    channel_hdr_record_size, sdf_hdr['file_hdr']['sdf_revision'],
                    sdf_file.read(channel_hdr_record_size)))
            else:
                sys.exit('This should have been a channel header record.')

        # Decode the scan structure records
        # Initialize record size to 0 until we know the answer
        scan_struct_record_size = 0
        for scan_struct_record_index in range(sdf_hdr['file_hdr']['num_scan_struct_records']):
            # Move to the start of the scan struct record
            sdf_file.seek(sdf_hdr['file_hdr']['offset_scan_struct_record'] +
                    scan_struct_record_index * scan_struct_record_size)
            # Read the record type and size
            scan_struct_record_type, scan_struct_record_size = struct.unpack(
                    record_type_size_format,
                    sdf_file.read(struct.calcsize(record_type_size_format)))
            if scan_struct_record_type == 15:
                # This is a channel header record
                # Backup and read all of the channel header record including
                # the record type and record size
                sdf_file.seek(sdf_file.tell() - struct.calcsize(record_type_size_format))
                sdf_hdr['scan_struct'] = _decode_sdf_scan_struct(
                    scan_struct_record_size, sdf_hdr['file_hdr']['sdf_revision'],
                    sdf_file.read(scan_struct_record_size))
            else:
                sys.exit('This should have been a scan struct record.')

        # Decode the Y-axis data records
        # The y-data offset will be -1 if there is no y-data
        if sdf_hdr['file_hdr']['offset_ydata_record'] >= 0:
            # Move to the start of the y-axis data record
            sdf_file.seek(sdf_hdr['file_hdr']['offset_ydata_record'])
            # Read the record type and size
            yaxis_data_record_type, yaxis_data_record_size = struct.unpack(
                    record_type_size_format,
                    sdf_file.read(struct.calcsize(record_type_size_format)))
            if yaxis_data_record_type == 17:
                # This is a y-axis data record
                sdf_data = np.fromfile(sdf_file, '>f',
                        count=sdf_hdr['data_hdr'][0]['num_points'], sep='')
                # TODO: Should probably leave in the native units unless
                # the user requests something else, but I'm going to cheat
                # and return just Vrms given this only works for the 
                # 35670A DSA currently.
                # FIXME: I'm cheating! I know that my data is only on the first channel
                # and that it uses the narrow_band_correction to convert from
                # Vpk^2 (native units) to Vrms
                channel_correction_factor = ((sdf_hdr['channel_hdr'][0]['window']['narrow_band_corr'] /
                    sdf_hdr['channel_hdr'][0]['int_2_eng_unit']) **
                        (sdf_hdr['vector_hdr'][0]['channel_power_48x'][0] / 48))
                # Apply the correction factor and then convert from
                # Vpk^2 to Vpk and then to Vrms
                sdf_data = np.sqrt(channel_correction_factor * sdf_data) / np.sqrt(2)
            else:
                sys.exit('This should have been a scan struct record.')


    return sdf_hdr, sdf_data

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', action='store',
            help='Input filename excluding extension')
    parser.add_argument('filetype', action='store',
            help='Input filetype should be sdf or ascii')
    args = parser.parse_args()

    if args.filetype == 'sdf':
        sdf_hdr, sdf_data = read_sdf_file(args.inputfile)
