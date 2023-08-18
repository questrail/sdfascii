#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013-2023 The sdfascii developers. All rights reserved.
# Project site: https://github.com/questrail/sdfascii
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
'''
sdfascii.py

Read Standard Data Format (SDF) and ASCII files created by HP/Agilent Dynamic
Signal Analyzers.

**WARNING:** Currently, only supporting SDF version 2.
'''

# Future imports
from __future__ import annotations

# Standard module imports
from datetime import datetime
import json
import struct
import sys
from typing import Any, Dict, TypedDict, Union, cast

# Data analysis related imports
import numpy as np
# import numpy.typing as npt

__version__ = '0.6.1'


FILE_HDR_RECORD_TYPE = 10
MEAS_HDR_RECORD_TYPE = 11
DATA_HDR_RECORD_TYPE = 12
VECTOR_HDR_RECORD_TYPE = 13
CHANNEL_HDR_RECORD_TYPE = 14
SCAN_STRUCT_RECORD_TYPE = 15
XDATA_HDR_RECORD_TYPE = 16
YDATA_HDR_RECORD_TYPE = 17
SCAN_BIG_RECORD_TYPE = 18
SCAN_VAR_RECORD_TYPE = 19
COMMENT_HDR_RECORD_TYPE = 20


class SDFFileHdrBase(TypedDict):
    record_size: int
    sdf_revision: int
    application: str
    measurement_start_datetime: datetime
    application_version: str
    num_data_hdr_records: int
    num_vector_hdr_records: int
    num_channel_hdr_records: int
    num_unique_records: int
    num_scan_struct_records: int
    num_xdata_records: int
    offset_data_hdr_record: int
    offset_vector_record: int
    offset_channel_record: int
    offset_unique_record: int
    offset_scan_struct_record: int
    offset_xdata_record: int
    offset_ydata_record: int


class SDFFileHdrV1(SDFFileHdrBase):
    pass


class SDFFileHdrV2(SDFFileHdrBase):
    pass


class SDFFileHdrV3(SDFFileHdrBase):
    pass


class SDFMeasHdrBase(TypedDict):
    record_size: int
    offset_unique_record: int
    block_size: int
    zoom_mode_on: bool
    average_type: str
    average_num: int
    pct_overlap: float
    meas_title: str
    center_freq: float
    span_freq: float
    sweep_freq: float
    meas_type: str
    real_time: str
    detection: str
    sweep_time: float


class SDFMeasHdrV1(SDFMeasHdrBase):
    pass


class SDFMeasHdrV2(SDFMeasHdrBase):
    start_freq_index: int
    stop_freq_index: int


class SDFMeasHdrV3(SDFMeasHdrBase):
    start_freq_index: int
    stop_freq_index: int


class SDFDataHdrBase(TypedDict):
    record_size: int
    offset_unique_record: int
    data_title: str
    domain: str
    data_type: str
    x_resolution_type: str
    x_data_type: str
    x_per_point: int
    y_data_type: str
    y_per_point: int
    y_is_complex: bool
    y_is_normalized: bool
    y_is_power_data: bool
    y_is_valid: bool
    first_vector_record_num: int
    total_rows: int
    xunit: SDFUnit
    y_unit_valid: bool
    yunit: SDFUnit
    abscissa_first_x: float
    abscissa_delta_x: float


class SDFDataHdrV1(SDFDataHdrBase):
    pass


class SDFDataHdrV2(SDFDataHdrBase):
    scan_data: bool
    window_applied: bool


class SDFDataHdrV3(SDFDataHdrBase):
    scan_data: bool
    window_applied: bool


class SDFVectorHdr(TypedDict):
    record_size: int
    offset_unique_record: int
    channel_record: tuple[int]
    channel_power_48x: tuple[int]


class SDFChannelHdr(TypedDict):
    record_size: int
    offset_unique_record: int
    channel_label: str
    module_id: str
    serial_number: str
    window: SDFWindow
    weight: str
    delay: float
    range: float
    direction: str
    point_num: int
    coupling: str
    overloaded: bool
    int_label: str
    eng_unit: SDFUnit
    int_2_eng_unit: float
    input_impedance: float
    channel_attribute: str
    alias_protected: bool
    digital_channel: bool
    channel_scale: float
    channel_offset: float
    gate_begin: float
    gate_end: float
    user_delay: float


class SDFScanStruct(TypedDict):
    record_size: int
    num_of_scans: int
    last_scan_index: int
    scan_type: str
    scan_var_type: str
    scan_unit: SDFUnit


class SDFUnit(TypedDict):
    label: str
    factor: float
    mass: int
    length: int
    time: int
    current: int
    temperature: int
    luminal_intensity: int
    mole: int
    plane_angle: int


class SDFWindow(TypedDict):
    window_type: int
    correction_mode: int
    bw: float
    time_const: float
    trunc: float
    wide_band_corr: float
    narrow_band_corr: float


class SDFHdrV1(TypedDict, total=False):
    valid_file_identifier: bool
    file_hdr: SDFFileHdrV1
    meas_hdr: SDFMeasHdrV1
    data_hdr: list[SDFDataHdrV1]
    vector_hdr: list[SDFVectorHdr]
    channel_hdr: list[SDFChannelHdr]
    scan_struct: SDFScanStruct


class SDFHdrV2(TypedDict, total=False):
    valid_file_identifier: bool
    file_hdr: SDFFileHdrV2
    meas_hdr: SDFMeasHdrV2
    data_hdr: list[SDFDataHdrV2]
    vector_hdr: list[SDFVectorHdr]
    channel_hdr: list[SDFChannelHdr]
    scan_struct: SDFScanStruct


class SDFHdrV3(TypedDict, total=False):
    valid_file_identifier: bool
    file_hdr: SDFFileHdrV3
    meas_hdr: SDFMeasHdrV3
    data_hdr: list[SDFDataHdrV3]
    vector_hdr: list[SDFVectorHdr]
    channel_hdr: list[SDFChannelHdr]
    scan_struct: SDFScanStruct


def _strip_nonprintable(input_bytes: bytes) -> str:
    r"""
    Convert a bytes object into a string returning any character up to, but not
    including, the first instance of \x00.
    """
    return input_bytes.decode('utf-8', 'replace').split('\x00', 1)[0]


def _decode_sdf_unit(binary_data: bytes) -> SDFUnit:
    values = struct.unpack('>10sf8b', binary_data)
    keys = ('label', 'factor', 'mass', 'length', 'time', 'current',
            'temperature', 'luminal_intensity', 'mole',
            'plane_angle')
    unit_dict = dict(zip(keys, values))
    unit_dict['label'] = _strip_nonprintable(unit_dict['label'])
    return cast(SDFUnit, unit_dict)


def _decode_sdf_window(binary_data: bytes) -> SDFWindow:
    values = struct.unpack(b'>2h5f', binary_data)
    keys = ('window_type', 'correction_mode', 'bw', 'time_const',
            'trunc', 'wide_band_corr', 'narrow_band_corr')
    window_dict = dict(zip(keys, values))
    window_type_decoder = {0: 'Window not applied',
                           1: 'Hanning',
                           2: 'Flat Top',
                           3: 'Uniform',
                           4: 'Force',
                           5: 'Response',
                           6: 'user-defined',
                           7: 'Hamming',
                           8: 'P301',
                           9: 'P310',
                           10: 'Kaiser-Bessel',
                           11: 'Harris',
                           12: 'Blackman',
                           13: 'Resolution filter',
                           14: 'Correlation Lead Lag',
                           15: 'Correlation Lag',
                           16: 'Gated',
                           17: 'P400',
                           }
    window_dict['window_type'] = window_type_decoder[
        window_dict['window_type']]
    correction_mode_decoder = {0: 'Correction not applied',
                               1: 'Narrow band correction applied',
                               2: 'Wide band correction applied'}
    window_dict['correction_mode'] = correction_mode_decoder[
        window_dict['correction_mode']]
    return cast(SDFWindow, window_dict)


def read_ascii_files(input_ascii_base_filename):
    # Create the four filenames
    ascii_ydata_filename = input_ascii_base_filename + '.TXT'
    ascii_xdata_filename = input_ascii_base_filename + '.X'

    # Read the x and y data
    xdata = np.loadtxt(ascii_xdata_filename)
    ydata = np.loadtxt(ascii_ydata_filename)

    # Return the x and y data as a structured array
    return np.core.records.fromarrays(
        [xdata, ydata], names='frequency,amplitude')


def _decode_sdf_file_hdr(
        record_size: int,
        binary_data: bytes) -> SDFFileHdrV1 | SDFFileHdrV2 | SDFFileHdrV3:
    """Decode the header information in the SDF file.

    Note: The HP documentation lists the binary indices starting a 1, whereas
    Python uses 0 based arrays/indices.

    Args:
        record_size: An integer indicating the total size of the binary_data
            including the record_type and record_size.
        file_hdr_binary: The binary data for the file header including the
            record_type and record_size.

    Returns:
        A dictionary containing the SDF header information.
    """

    file_hdr: Dict[str, Union[int, str, datetime]] = {}
    file_hdr['record_size'] = record_size
    file_hdr['sdf_revision'], = struct.unpack('>h', binary_data[6:8])
    application_code, = struct.unpack('>h', binary_data[8:10])
    application_decoder = {-1: 'HP VISTA', -2: 'HP SINE', -3: 'HP 35660A',
                           -4: 'HP 3562A, HP 3563A', -5: 'HP 3588A',
                           -6: 'HP 3589A', -99: 'Unknown',
                           1: 'HP 3566A, HP 3567A', 2: 'HP 35665A',
                           3: 'HP 3560A', 4: 'HP 89410A, HP 89440A',
                           7: 'HP 35635R', 8: 'HP 35654A-S1A',
                           9: 'HP 3569A', 10: 'HP 35670A', 11: 'HP 3587S'}
    file_hdr['application'] = application_decoder[application_code]
    msr_year, msr_month_day, msr_hour_min = struct.unpack(
        '>hhh', binary_data[10:16])
    msr_month, msr_day = divmod(msr_month_day, 100)
    msr_hour, msr_sec = divmod(msr_hour_min, 100)
    file_hdr['measurement_start_datetime'] = datetime(
        msr_year, msr_month, msr_day, msr_hour, msr_sec)
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

    if file_hdr['sdf_revision'] == 1:
        temp_file_hdr = cast(SDFFileHdrV1, file_hdr)
    elif file_hdr['sdf_revision'] == 2:
        temp_file_hdr = cast(SDFFileHdrV2, file_hdr)
    elif file_hdr['sdf_revision'] == 3:
        # Continue reading bytes 65-80 if this is SDF ver. 3
        # FIXME: Need to add the code for SDF ver. 3 in the future.
        temp_file_hdr = cast(SDFFileHdrV3, file_hdr)
    else:
        # SDF revision not recognized
        sys.exit('Did not recognize SDF revision in file header.')

    return temp_file_hdr


def _decode_sdf_meas_hdr(
        record_size: int,
        sdf_revision: int,
        binary_data: bytes) -> SDFMeasHdrV1 | SDFMeasHdrV2 | SDFMeasHdrV3:
    '''
    Decode the measurement header binary data
    '''
    meas_hdr: dict = {}
    # FIXME(mdr): Check that the record_type is 11 (short int 0:2).
    record_size_from_binary_data = struct.unpack('>l', binary_data[2:6])[0]
    if record_size != record_size_from_binary_data:
        sys.exit('Bad record size in SDF_MEAS_HDR')
    meas_hdr['record_size'] = record_size
    (meas_hdr['offset_unique_record'],) = struct.unpack(
        b'>1l', binary_data[6:10])
    meas_hdr['block_size'], = struct.unpack('>l', binary_data[18:22])
    meas_hdr['zoom_mode_on'], = struct.unpack('>h', binary_data[22:24])
    meas_hdr['zoom_mode_on'] = bool(meas_hdr['zoom_mode_on'])
    coded_average_type, = struct.unpack('>h', binary_data[28:30])
    average_type_decoder = {0: 'None', 1: 'RMS', 2: 'RMS Exponential',
                            3: 'Vector', 4: 'Vector Exponential',
                            5: 'Continuous Peak Hold', 6: 'Peak'}
    meas_hdr['average_type'] = average_type_decoder[coded_average_type]
    meas_hdr['average_num'], = struct.unpack('>l', binary_data[30:34])
    meas_hdr['pct_overlap'], = struct.unpack(b'>f', binary_data[34:38])
    meas_hdr['meas_title'] = _strip_nonprintable(binary_data[38:98])
    meas_hdr['video_bw'], = struct.unpack('>f', binary_data[98:102])
    (meas_hdr['center_freq'], meas_hdr['span_freq'],
        meas_hdr['sweep_freq']) = struct.unpack(
            b'>3d', binary_data[102:126])
    coded_meas_type, = struct.unpack('>h', binary_data[126:128])
    meas_type_decoder = {-99: 'Unknown measurement',
                         0: 'Spectrum measurement',
                         1: 'Network measurement',
                         2: 'Swept measurement',
                         3: 'FFT measurement',
                         4: 'Orders measurement',
                         5: 'Octave measurement',
                         6: 'Capture measurement',
                         7: 'Correlation measurement',
                         8: 'Histogram measurement',
                         9: 'Swept network measurement',
                         10: 'FFT network measurement',
                         }
    meas_hdr['meas_type'] = meas_type_decoder[coded_meas_type]
    coded_real_time, = struct.unpack('>h', binary_data[128:130])
    real_time_decoder = {0: 'Not continuous', 1: 'Continuous'}
    meas_hdr['real_time'] = real_time_decoder[coded_real_time]
    coded_detection, = struct.unpack('>h', binary_data[130:132])
    detection_decoder = {-99: 'Unknown detection type',
                         0: 'Sample detection',
                         1: 'Positive peak detection',
                         2: 'Negative peak detection',
                         3: 'Rose-and-fell detection'}
    meas_hdr['detection'] = detection_decoder[coded_detection]
    meas_hdr['sweep_time'], = struct.unpack(b'>d', binary_data[132:140])

    if sdf_revision == 1:
        # Decode the revision 1 stuff
        # FIXME: Add rev 1 stuff later
        temp_meas_hdr = cast(SDFMeasHdrV1, meas_hdr)
    elif sdf_revision == 2:
        # Decode the revision 2 stuff
        (meas_hdr['start_freq_index'], meas_hdr['stop_freq_index']) = \
            struct.unpack(b'>2h', binary_data[24:28])
        temp_meas_hdr = cast(SDFMeasHdrV2, meas_hdr)
    elif sdf_revision == 3:
        # Decode the revision 3 related stuff
        # FIXME: Add rev 3 stuff later
        temp_meas_hdr = cast(SDFMeasHdrV3, meas_hdr)
    else:
        # SDF revision not recognized
        sys.exit('Did not recognize SDF revision passed to meas hdr.')

    return temp_meas_hdr


def _decode_sdf_data_hdr(
        record_size: int,
        sdf_revision: int,
        binary_data: bytes) -> Union[SDFDataHdrV1, SDFDataHdrV2]:
    '''
    Decode the data header binary data
    '''
    data_hdr: dict = {}
    data_hdr['record_size'] = record_size
    (data_hdr['offset_unique_record'],) = \
        struct.unpack('>1l', binary_data[6:10])
    data_hdr['data_title'] = _strip_nonprintable(
        struct.unpack(b'>16s', binary_data[10:26])[0])
    coded_domain, = struct.unpack('>h', binary_data[26:28])
    domain_decoder = {-99: 'Unknown',
                      0: 'Frequency domain',
                      1: 'Time domain',
                      2: 'Amplitude domain',
                      3: 'RPM',
                      4: 'Order',
                      5: 'Channel',
                      6: 'Octave'}
    data_hdr['domain'] = domain_decoder[coded_domain]
    coded_data_type, = struct.unpack('>h', binary_data[28:30])
    data_type_decoder = {-99: 'Unknown',
                         0: 'Time',
                         1: 'Linear spectrum',
                         2: 'Auto-power spectrum',
                         3: 'Cross-power spectrum',
                         4: 'Frequency response',
                         5: 'Auto-correlation',
                         6: 'Cross-correlation',
                         7: 'Impulse response',
                         8: 'Ordinary coherence',
                         9: 'Partial coherence',
                         10: 'Multiple coherence',
                         11: 'Full octave',
                         12: 'Third octave',
                         13: 'Convolution',
                         14: 'Histogram',
                         15: 'Probability density function',
                         16: 'Cumulative density function,',
                         17: 'Power spectrum order tracking',
                         18: 'Composite power tracking',
                         19: 'Phase order tracking',
                         20: 'RPM spectral',
                         21: 'Order ratio',
                         22: 'Orbit',
                         23: 'HP 35650 series calibration',
                         24: 'Sine rms pwr data',
                         25: 'Sine variance data',
                         26: 'Sine range data',
                         27: 'Sine settle time data',
                         28: 'Sine integ time data',
                         29: 'Sine source data',
                         30: 'Sine overload data',
                         31: 'Sine linear data',
                         32: 'Synthesis',
                         33: 'Curve fit weighting function',
                         34: 'Frequency corrections (for capture)',
                         35: 'All pass time data',
                         36: 'Norm reference data',
                         37: 'tachometer data',
                         38: 'limit line data',
                         39: 'twelfth octave data',
                         40: 'S11 data',
                         41: 'S21 data',
                         42: 'S12 data',
                         43: 'S22 data',
                         44: 'PSD data',
                         45: 'decimated time data',
                         46: 'overload data',
                         47: 'compressed time data',
                         48: 'external trigger data',
                         49: 'pressure data',
                         50: 'intensity data',
                         51: 'PI index data',
                         52: 'velocity data',
                         53: 'PV index data',
                         54: 'sound power data',
                         55: 'field indicator data',
                         56: 'partial power data',
                         57: 'Ln 1 data',
                         58: 'Ln 10 data',
                         59: 'Ln 50 data',
                         60: 'Ln 90 data',
                         61: 'Ln 99 data',
                         62: 'Ln user data',
                         63: 'T20 data',
                         64: 'T30 data',
                         65: 'RT60 data',
                         66: 'average count data',
                         68: ' IQ measured time',
                         69: ' IQ measured spectrum',
                         70: ' IQ reference time',
                         71: ' IQ reference spectrum',
                         72: ' IQ error magnitude',
                         73: ' IQ error phase',
                         74: ' IQ error vector time',
                         75: ' IQ error vector spectrum',
                         76: ' symbol table data',
                         }
    data_hdr['data_type'] = data_type_decoder[coded_data_type]
    coded_x_resolution_type, = struct.unpack('>h', binary_data[42:44])
    x_resolution_type_decoder = {0: 'Linear', 1: 'Logarithmic',
                                 2: 'Arbitrary, one per file',
                                 3: 'Arbitrary, one per data type',
                                 4: 'Arbitrary, one per trace'}
    data_hdr['x_resolution_type'] = \
        x_resolution_type_decoder[coded_x_resolution_type]
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
    data_hdr['y_is_normalized'] = bool(data_hdr['y_is_normalized'])
    data_hdr['y_is_power_data'], = struct.unpack('>h', binary_data[56:58])
    data_hdr['y_is_power_data'] = bool(data_hdr['y_is_power_data'])
    data_hdr['y_is_valid'], = struct.unpack('>h', binary_data[58:60])
    data_hdr['y_is_valid'] = bool(data_hdr['y_is_valid'])
    data_hdr['first_vector_record_num'], = struct.unpack(
        '>l', binary_data[60:64])
    data_hdr['total_rows'], data_hdr['total_cols'] = struct.unpack(
        '>2h', binary_data[64:68])
    data_hdr['xunit'] = _decode_sdf_unit(binary_data[68:90])
    data_hdr['y_unit_valid'], = struct.unpack('>h', binary_data[90:92])
    data_hdr['y_unit_valid'] = bool(data_hdr['y_unit_valid'])
    data_hdr['yunit'] = _decode_sdf_unit(binary_data[92:114])

    if sdf_revision == 1:
        # Decode the revision 1 stuff
        # FIXME: Add rev 1 stuff later
        (data_hdr['abscissa_first_x'], data_hdr['abscissa_delta_x']) = \
            struct.unpack('>2f', binary_data[34:42])
        temp_data_hdr = cast(SDFDataHdrV1, data_hdr)
    elif sdf_revision == 2:
        # Decode the revision 2 stuff
        (data_hdr['num_points'], data_hdr['last_valid_index']) = \
            struct.unpack('>2h', binary_data[30:34])
        (data_hdr['abscissa_first_x'], data_hdr['abscissa_delta_x']) = \
            struct.unpack(b'>2d', binary_data[114:130])
        data_hdr['scan_data'], = struct.unpack('>h', binary_data[130:132])
        data_hdr['scan_data'] = bool(data_hdr['scan_data'])
        data_hdr['window_applied'], = struct.unpack('>h', binary_data[132:134])
        data_hdr['window_applied'] = bool(data_hdr['window_applied'])
        temp_data_hdr = cast(SDFDataHdrV2, data_hdr)
    elif sdf_revision == 3:
        # Decode the revision 3 related stuff
        # FIXME: Add rev 3 stuff later
        pass
    else:
        # SDF revision not recognized
        sys.exit('Did not recognize SDF revision')

    return temp_data_hdr


def _decode_sdf_vector_hdr(
        record_size: int,
        sdf_revision: int,
        binary_data: bytes) -> SDFVectorHdr:
    '''
    Decode the vector header binary data
    '''
    vector_hdr: dict = {}
    vector_hdr['record_size'] = record_size
    (vector_hdr['offset_unique_record'],) = \
        struct.unpack('>l', binary_data[6:10])
    vector_hdr['channel_record'] = struct.unpack('>2h', binary_data[10:14])
    vector_hdr['channel_power_48x'] = struct.unpack('>2h', binary_data[14:18])

    return cast(SDFVectorHdr, vector_hdr)


def _decode_sdf_channel_hdr(
        record_size: int,
        sdf_revision: int,
        binary_data: bytes) -> SDFChannelHdr:
    """Decode the channel header binary data to a dictionary.
    """
    channel_hdr: dict = {}
    channel_hdr['record_size'] = record_size
    (channel_hdr['offset_unique_record'],) = \
        struct.unpack('>l', binary_data[6:10])
    channel_hdr['channel_label'] = _strip_nonprintable(
        struct.unpack(b'>30s', binary_data[10:40])[0])
    channel_hdr['module_id'] = _strip_nonprintable(
        struct.unpack(b'>12s', binary_data[40:52])[0])
    channel_hdr['serial_number'] = _strip_nonprintable(
        struct.unpack('>12s', binary_data[52:64])[0])
    channel_hdr['window'] = _decode_sdf_window(binary_data[64:88])
    coded_weight, = struct.unpack('>h', binary_data[88:90])
    weight_decoder = {0: 'No weighting', 1: 'A-weighting',
                      2: 'B-weighting', 3: 'C-weighting'}
    channel_hdr['weight'] = weight_decoder[coded_weight]
    (channel_hdr['delay'], channel_hdr['range']) = struct.unpack(
        b'>2f', binary_data[90:98])
    coded_direction, = struct.unpack('>h', binary_data[98:100])
    direction_decoder = {-9: '-TZ', -8: '-TY', -7: '-TX', -3: '-Z',
                         -2: '-Y', -1: 'X', 0: 'No direction specified',
                         1: 'X', 2: 'Y', 3: 'Z', 4: 'Radial',
                         5: 'Tangential, theta angle',
                         6: 'Tangential, phi angle', 7: 'TX',
                         8: 'TY', 9: 'TZ'}
    channel_hdr['direction'] = direction_decoder[coded_direction]
    channel_hdr['point_num'], = struct.unpack('>h', binary_data[100:102])
    coded_coupling, = struct.unpack('>h', binary_data[102:104])
    coupling_decoder = {0: 'DC', 1: 'AC'}
    channel_hdr['coupling'] = coupling_decoder[coded_coupling]
    channel_hdr['overloaded'], = struct.unpack('>h', binary_data[104:106])
    channel_hdr['overloaded'] = bool(channel_hdr['overloaded'])
    channel_hdr['int_label'] = _strip_nonprintable(
        struct.unpack(b'>10s', binary_data[106:116])[0])
    channel_hdr['eng_unit'] = _decode_sdf_unit(binary_data[116:138])
    channel_hdr['int_2_eng_unit'], = struct.unpack('>f', binary_data[138:142])
    channel_hdr['input_impedance'], = struct.unpack('>f', binary_data[142:146])
    coded_channel_attribute, = struct.unpack('>h', binary_data[146:148])
    channel_attribute_decoder = {-99: 'Unknown attribute', 0: 'No attribute',
                                 1: 'Tach attribute', 2: 'Reference attribute',
                                 3: 'Tach and reference attribute',
                                 4: 'Clockwise attribute'}
    channel_hdr['channel_attribute'] = \
        channel_attribute_decoder[coded_channel_attribute]
    channel_hdr['alias_protected'], = struct.unpack('>h', binary_data[148:150])
    channel_hdr['alias_protected'] = bool(channel_hdr['alias_protected'])
    channel_hdr['digital_channel'], = struct.unpack('>h', binary_data[150:152])
    channel_hdr['digital_channel'] = bool(channel_hdr['digital_channel'])
    (channel_hdr['channel_scale'], channel_hdr['channel_offset'],
        channel_hdr['gate_begin'], channel_hdr['gate_end'],
        channel_hdr['user_delay']) = struct.unpack(
            b'>5d', binary_data[152:192])

    return cast(SDFChannelHdr, channel_hdr)


def _decode_sdf_scan_struct(
        record_size: int,
        sdf_revision: int,
        binary_data: bytes) -> SDFScanStruct:
    """Decode the scan structure binary data to a dictionary.
    """
    scan_struct: dict = {}
    scan_struct['record_size'] = record_size
    scan_struct['num_of_scans'], = struct.unpack('>h', binary_data[6:8])
    scan_struct['last_scan_index'], = struct.unpack('>h', binary_data[8:10])
    coded_scan_type, = struct.unpack('>h', binary_data[10:12])
    # The HP Standard Data Foramt Utilties User's Guide shows 0 = Depth and
    # 1 = Scan.
    # However, the .DAT file created by 35670A shows 1 = Depth.
    # I'm going to believe the documentation
    scan_type_decoder = {0: 'Depth', 1: 'Scan'}
    scan_struct['scan_type'] = scan_type_decoder[coded_scan_type]
    coded_scan_var_type, = struct.unpack('>h', binary_data[12:14])
    scan_var_type_decoder = {1: 'Short', 2: 'Long', 3: 'Float',
                             4: 'Double'}
    scan_struct['scan_var_type'] = scan_var_type_decoder[coded_scan_var_type]
    scan_struct['scan_unit'] = _decode_sdf_unit(binary_data[14:36])

    return cast(SDFScanStruct, scan_struct)


def read_sdf_file(sdf_filename: str) -> tuple[Any, Any]:
    """Read the binary SDF file into a dictionary.

    The SDF format is described in Appendix B of the Standard Data Format
    Utilities User's Guide. There are three different versions of the SDF file
    format.

    Args:
        sdf_filename: A string containing the SDF filename to be read.

    Returns:
        A tuple containing a dictionary of the header information and a numpy
            array containing the data.
    """
    sdf_hdr: dict = {}
    sdf_hdr['valid_file_identifier'] = False
    # There are zero or more channel header records.
    sdf_hdr['channel_hdr'] = []

    with open(sdf_filename, 'rb') as sdf_file:
        # Read SDF file_identfication
        file_identifier = sdf_file.read(2)
        if file_identifier != b'B\x00':
            # Didn't find a valid file identifer, so bail out
            sys.exit(f'Invalid file identifier: {file_identifier!r}')
        sdf_hdr['valid_file_identifier'] = True

        # Determine record type (short) and record size (long)
        # Every record has these two special fields at the start
        record_type_size_format = '>hl'

        # Process the file header record
        file_hdr_record_type, file_hdr_record_size = struct.unpack(
            record_type_size_format,
            sdf_file.read(struct.calcsize(
                record_type_size_format.encode())))
        # Confirm this is a file header record.
        if file_hdr_record_type != FILE_HDR_RECORD_TYPE:
            sys.exit('Error processing SDF file; expected file header')
        # Found the file header record
        # Process the entire file header record including the record type
        # (short) and record size (long)
        sdf_file.seek(sdf_file.tell() -
                      struct.calcsize(record_type_size_format))
        sdf_hdr['file_hdr'] = _decode_sdf_file_hdr(
            file_hdr_record_size,
            sdf_file.read(file_hdr_record_size))

        # Process the measurement header record
        meas_hdr_record_type, meas_hdr_record_size = struct.unpack(
            record_type_size_format,
            sdf_file.read(struct.calcsize(record_type_size_format)))
        # Confirm this is a measurement header record.
        if meas_hdr_record_type != MEAS_HDR_RECORD_TYPE:
            sys.exit('Error processing SDF file; expected measurement header')
        # Found the measurement header record
        sdf_file.seek(sdf_file.tell() -
                      struct.calcsize(record_type_size_format))
        sdf_hdr['meas_hdr'] = _decode_sdf_meas_hdr(
            meas_hdr_record_size,
            sdf_hdr['file_hdr']['sdf_revision'],
            sdf_file.read(meas_hdr_record_size))

        # Decode the data header records
        sdf_hdr['data_hdr'] = []
        # Initialize record size to 0 until we know the answer
        data_hdr_record_size = 0
        for data_hdr_record_index in range(
                sdf_hdr['file_hdr']['num_data_hdr_records']):
            # Move to the start of the data header record
            sdf_file.seek(sdf_hdr['file_hdr']['offset_data_hdr_record'] +
                          data_hdr_record_index * data_hdr_record_size)
            # Read the record type and size
            data_hdr_record_type, data_hdr_record_size = struct.unpack(
                record_type_size_format,
                sdf_file.read(struct.calcsize(record_type_size_format)))
            # Confirm this is a data header record.
            if data_hdr_record_type != DATA_HDR_RECORD_TYPE:
                sys.exit('This should have been a data header record.')
            # This is a data header record
            sdf_file.seek(sdf_file.tell() -
                          struct.calcsize(record_type_size_format))
            sdf_hdr['data_hdr'].append(
                _decode_sdf_data_hdr(
                    data_hdr_record_size,
                    sdf_hdr['file_hdr']['sdf_revision'],
                    sdf_file.read(data_hdr_record_size)))

        # Decode the vector header records
        sdf_hdr['vector_hdr'] = []
        # Initialize record size to 0 until we know the answer
        vector_hdr_record_size = 0
        for vector_hdr_record_index in range(
                sdf_hdr['file_hdr']['num_vector_hdr_records']):
            # Move to the start of the vector header record
            sdf_file.seek(sdf_hdr['file_hdr']['offset_vector_record'] +
                          vector_hdr_record_index * vector_hdr_record_size)
            # Read the record type and size
            # The record type should be 13 and the size should be 18 bytes
            vector_hdr_record_type, vector_hdr_record_size = struct.unpack(
                record_type_size_format,
                sdf_file.read(struct.calcsize(record_type_size_format)))
            # Confirm this is a vector header record.
            if vector_hdr_record_type != VECTOR_HDR_RECORD_TYPE:
                sys.exit('This should have been a vector header record.')
            # This is a vector header record
            # Backup and read all of the vector header record including
            # the record type and record size
            sdf_file.seek(sdf_file.tell() -
                          struct.calcsize(record_type_size_format))
            sdf_hdr['vector_hdr'].append(_decode_sdf_vector_hdr(
                vector_hdr_record_size,
                sdf_hdr['file_hdr']['sdf_revision'],
                sdf_file.read(vector_hdr_record_size)))

        # Decode the channel header records
        sdf_hdr['channel_hdr'] = []
        # Initialize record size to 0 until we know the answer
        channel_hdr_record_size = 0
        for channel_hdr_record_index in range(
                sdf_hdr['file_hdr']['num_channel_hdr_records']):
            # Move to the start of the channel header record
            sdf_file.seek(sdf_hdr['file_hdr']['offset_channel_record'] +
                          channel_hdr_record_index * channel_hdr_record_size)
            # Read the record type and size
            channel_hdr_record_type, channel_hdr_record_size = struct.unpack(
                record_type_size_format,
                sdf_file.read(struct.calcsize(record_type_size_format)))
            # Confirm this is a channel header record.
            if channel_hdr_record_type != CHANNEL_HDR_RECORD_TYPE:
                sys.exit('This should have been a channel header record.')
            # This is a channel header record
            # Backup and read all of the channel header record including
            # the record type and record size
            sdf_file.seek(sdf_file.tell() -
                          struct.calcsize(record_type_size_format))
            sdf_hdr['channel_hdr'].append(_decode_sdf_channel_hdr(
                channel_hdr_record_size,
                sdf_hdr['file_hdr']['sdf_revision'],
                sdf_file.read(channel_hdr_record_size)))

        # Decode the scan structure records
        # Initialize record size to 0 until we know the answer
        scan_struct_record_size = 0
        for scan_struct_record_index in range(
                sdf_hdr['file_hdr']['num_scan_struct_records']):
            # Move to the start of the scan struct record
            sdf_file.seek(sdf_hdr['file_hdr']['offset_scan_struct_record'] +
                          scan_struct_record_index * scan_struct_record_size)
            # Read the record type and size
            scan_struct_record_type, scan_struct_record_size = struct.unpack(
                record_type_size_format,
                sdf_file.read(struct.calcsize(record_type_size_format)))
            # Confirm this is a channel header record.
            if scan_struct_record_type != SCAN_STRUCT_RECORD_TYPE:
                sys.exit('This should have been a scan struct record.')
            # This is a channel header record
            # Backup and read all of the channel header record including
            # the record type and record size
            sdf_file.seek(sdf_file.tell() -
                          struct.calcsize(record_type_size_format))
            sdf_hdr['scan_struct'] = _decode_sdf_scan_struct(
                scan_struct_record_size,
                sdf_hdr['file_hdr']['sdf_revision'],
                sdf_file.read(scan_struct_record_size))

        # ------------------------------------------------------------------- #
        # Decode the Y-axis data records
        # The y-data offset will be -1 if there is no y-data
        # ------------------------------------------------------------------- #
        if sdf_hdr['file_hdr']['offset_ydata_record'] >= 0:
            # Move to the start of the y-axis data record
            sdf_file.seek(sdf_hdr['file_hdr']['offset_ydata_record'])
            # Read the record type and size
            yaxis_data_record_type, yaxis_data_record_size = struct.unpack(
                record_type_size_format,
                sdf_file.read(struct.calcsize(record_type_size_format)))
            # Confirm we received a y-axis data record
            if yaxis_data_record_type != YDATA_HDR_RECORD_TYPE:
                sys.exit('This should have been a scan struct record.')

            # FIXME: Need to handle more than just the first data_hdr
            data_hdr = sdf_hdr['data_hdr'][0]
            vector_id = data_hdr['first_vector_record_num']

            # Create the combined trace correction factor.
            vector_hdr = sdf_hdr['vector_hdr'][vector_id]
            resp_ch_id = vector_hdr['channel_record'][0]
            pwr_of_resp_ch = vector_hdr['channel_power_48x'][0]
            exciter_ch_id = vector_hdr['channel_record'][1]
            pwr_of_exciter_ch = vector_hdr['channel_power_48x'][1]

            # Calculate the response channel combined correction factor.
            if resp_ch_id == -1:
                resp_ch_corr_factor = 1
            else:
                resp_ch = sdf_hdr['channel_hdr'][resp_ch_id]
                # Calculate the engineering unit (EU) correction. EU correction
                # allows you to convert y-axis data from the instrument’s
                # internal unit to some user-defined unit (such as g — the
                # acceleration of gravity). An EU correction factor is included
                # in each Channel Header record; the factor’s field name is
                # int2engrUnit.
                resp_eu_corr = resp_ch['int_2_eng_unit']

                # Calculate the window correction, which is necessary only for
                # FREQ or ORDER domain data.
                if data_hdr['domain'] == 'Frequency domain' or \
                        data_hdr['domain'] == 'Channel':
                    resp_window_corr = \
                        resp_ch['window']['narrow_band_corr']
                else:
                    resp_window_corr = 1.0

                # Calculate te combined correction factor for the response
                # channel.
                resp_ch_corr_factor = (
                    (resp_window_corr / resp_eu_corr) ** (pwr_of_resp_ch / 48))

            # Calculate the exciter channel combined correction factor.
            if exciter_ch_id == -1:
                exciter_ch_corr_factor = 1
            else:
                exciter_ch = sdf_hdr['channel_hdr'][exciter_ch_id]
                exciter_eu_corr = exciter_ch['int_2_eng_unit']

                # Calculate the window correction, which is necessary only for
                # FREQ or ORDER domain data.
                if data_hdr['domain'] == 'Frequency domain' or \
                        data_hdr['domain'] == 'Channel':
                    exciter_window_corr = \
                        exciter_ch['window']['narrow_band_corr']
                else:
                    exciter_window_corr = 1.0

                # Calculate te combined correction factor for the exciter
                # channel.
                exciter_ch_corr_factor = (
                    (exciter_window_corr / exciter_eu_corr) **
                    (pwr_of_exciter_ch / 48))

            trace_corr_factor = resp_ch_corr_factor * exciter_ch_corr_factor

            # Read the y-axis data record
            # FIXME: Need to handle cases where the y-data has muliple points.
            # Right now we're only handling either single floats or single
            # complex values.
            dtype = '>f'
            if data_hdr['y_is_complex']:
                dtype = np.dtype('>c16')
            sdf_data = np.fromfile(
                file=sdf_file,
                dtype=dtype,
                count=data_hdr['num_points'],
                sep='')

            # Apply the trace correction factor.
            sdf_data = trace_corr_factor * sdf_data

            # FIXME: I'm cheating if this is a 35670A measurement and
            # converting from the Vpk^2 (native units) to Vrms. Convert from
            # Vpk^2 to Vpk and then to Vrms
            if sdf_hdr['file_hdr']['application'] == 'HP 35670A':
                sdf_data = np.sqrt(sdf_data) / np.sqrt(2)

            # FIXME: I'm only returning the data over the start and stop
            # frequency indices, which are 0 & 1600, respectively. The
            # last_valid_index is 2048. Why the discrepancy?
            start_idx = sdf_hdr['meas_hdr']['start_freq_index']
            stop_idx = sdf_hdr['meas_hdr']['stop_freq_index']
            sdf_data = sdf_data[start_idx:stop_idx+1]

    return sdf_hdr, sdf_data


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('filetype', action='store',
                        help='Input filetype should be sdf or ascii')
    parser.add_argument('inputfile', action='store',
                        help='Input filename excluding extension')
    parser.add_argument('outputfile', action='store',
                        help='Output json filename')
    args = parser.parse_args()

    if args.filetype == 'sdf':
        sdf_hdr, sdf_data = read_sdf_file(args.inputfile)
        with open(args.outputfile, "w") as outfile:
            json.dump(sdf_hdr, outfile, indent=2, default=str)
