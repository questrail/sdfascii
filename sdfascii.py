#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
sdfascii.py

Read SDF and ASCII files created by HP/Agilent Dynamic Signal Analyzers.
'''

# Try to future proof code so that it's Python 3.x ready
from __future__ import print_function
#from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import

# Standard module imports
import struct
import sys

# Data analysis related imports
import numpy as np

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

def _process_sdf_file_hdr(record_type, record_size, binary_data):
    '''
    record_size is the total size of the binary_data including the
    record_type and record_size, which are not in binary_data
    '''
    return {}

def read_sdf_file(sdf_filename):
    '''
    Read the binary SDF file.

    The SDF format is described in Appendix B of the Standard
    Data Format Utilities User's Guide.

    There are three different versions of SDF.

    '''
    sdf_hdr = {}
    # Change sdf_data to a numpy array
    sdf_data = {}
    sdf_hdr['valid_file_identifier'] = False
    sdf_hdr['file_hdr'] = {}     # There's only 1 file header record
    sdf_hdr['measurement_hdr'] = {}     # There's only 1 measurement header record
    sdf_hdr['data_hdr'] = []     # There are 0 or more data header records
    sdf_hdr['vector_hdr'] = []   # There are 0 or more vector header records
    sdf_hdr['channel_hdr'] = []  # There are 0 or more channel header records

    with open(sdf_filename, 'rb') as sdf_file:
        # Read SDF file_identfication
        file_identifier = sdf_file.read(2)
        if file_identifier == 'B\x00':
            sdf_hdr['valid_file_identifier'] = True
        else:
            # Didn't find a valid file identifer, so bail out
            sys.exit('Did not find a valid file identifier.')

        # Process the file header record
        # Determine record type (short) and record size (long)
        record_type_size_format = '>hl'
        record_type, record_size = struct.unpack(record_type_size_format,
                sdf_file.read(struct.calcsize(record_type_size_format)))
        if record_type == 10:
            # Found the file header record
            sdf_hdr['file_hdr'] = _process_sdf_file_hdr(record_type, record_size,
                    sdf_file.read(record_size - struct.calcsize(record_type_size_format)))
        else:
            sys.exit('Error processing SDF file; expected file header')

        # Process the measurement header record
        # Determine record type (short) and record size (long)
        record_type_size_format = '>hl'
        record_type, record_size = struct.unpack(record_type_size_format,
                sdf_file.read(struct.calcsize(record_type_size_format)))
        if record_type == 11:
            # Found the measurement header record
            pass
        else:
            sys.exit('Error processing SDF file; expect measurement header')

        all_records_processed = False
        while not all_records_processed:
            # Determine record type (short) and record size (long)
            record_type_size_format = '>hl'
            record_type, record_size = struct.unpack(record_type_size_format,
                    sdf_file.read(struct.calcsize(record_type_size_format)))
            print('Processing record_type {rec_type}, which is {rec_size} bytes'.format(
                rec_type=record_type,
                rec_size=record_size))
            if record_type == 12:
                # Process a data header record (could be more than one)
                sdf_hdr['data_hdr'].append(_process_sdf_data_hdr(record_type,
                    record_size, sdf_file.read(record_size - struct.calcsize(
                        record_type_size_format))))
            elif record_type == 13:
                # Process a vector header record (could be more than one)
                sdf_hdr['vector_hdr'].append(_process_sdf_vector_hdr(record_type,
                    record_size, sdf_file.read(record_size - struct.calcsize(
                        record_type_size_format))))
            elif record_type == 14:
                # Process channel header record (could be more than one)
                sdf_hdr['channel_hdr'].append('Process me.')
            elif record_type == 15:
                # Process a scan structure record
                sdf_hdr['scan_structure'] = 'Process me.'

            # Only read one record at this point
            all_records_processed = True



        #dt = np.dtype([('file_id', '|a2')])
        #sdf_data = np.fromfile(sdf_file, dtype=dt, count=1, sep='')

        #dt = np.dtype([('sdf_file_hdr', [('record_type', 'i1'), ('record_size', 'i2')])])
        #sdf_data2 = np.fromfile(sdf_file, dtype=dt, count=1, sep='')

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
