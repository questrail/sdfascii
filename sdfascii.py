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

def read_sdf_file(sdf_filename):
    sdf_hdr = {}
    # Change sdf_data to a numpy array
    sdf_data = {}
    with open(sdf_filename, 'rb') as sdf_file:
        # Read SDF file_identfication
        sdf_hdr['file_identifier'] = sdf_file.read(2)

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
