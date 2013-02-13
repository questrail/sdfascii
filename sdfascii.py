#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
sdfascii.py

Read SDF and ASCII files created by HP/Agilent Dynamic Signal Analyzers.
'''

# Try to future proof code so that it's Python 3.x ready
from __future__ import print_function
from __future__ import unicode_literals
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

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', action='store',
            help='Input filename excluding extension')
    args = parser.parse_args()


