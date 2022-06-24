# -*- coding: utf-8 -*-
# Copyright (c) 2022 The sdfascii developers. All rights reserved.
# Project site: https://github.com/questrail/sdfascii
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
import codecs
import os
import re
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    """Read parts of a file

    Taken from pip's setup.py
    intentionally *not* adding an encoding option to open
    see: https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    """
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    """Find version in source file

    Read the version number from a source file.
    Code taken from pip's setup.py
    """
    version_file = read(*file_paths)
    # The version line must have the form:
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name='sdfascii',
    version=find_version('sdfascii.py'),
    author='Matthew Rankin',
    author_email='matthew@questrail.com',
    py_modules=['sdfascii'],
    url='http://github.com/questrail/sdfascii',
    license='MIT',
    description='Read HP SDF binary and ASCII files',
    long_description=long_description,
    long_description_content_type="text/markdown",
    requires=['numpy (>=1.22.0)'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
