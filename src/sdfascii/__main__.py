# Copyright (c) 2013-2026 The sdfascii developers. All rights reserved.
# Project site: https://github.com/questrail/sdfascii
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Dump the header of an SDF file to JSON.

    uv run python -m sdfascii sdf examples/HP35670A.DAT examples/hp35670a.json

This is what used to sit under `if __name__ == "__main__":` at the foot of the
module. That block ran when the module was a file invoked as a script; now
that it is a package, nothing would ever have reached it.
"""

import argparse
import json

from . import read_sdf_file


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="sdfascii", description=__doc__)
    # `ascii` was accepted here and then silently did nothing: the body only
    # ever handled `sdf`, so an ASCII run wrote no file and exited 0. Naming
    # the one implemented choice turns that into an argparse error.
    parser.add_argument(
        "filetype", choices=("sdf",), help="the format of the input file"
    )
    parser.add_argument("inputfile", help="the SDF file to read")
    parser.add_argument("outputfile", help="the JSON file to write the header to")
    args = parser.parse_args(argv)

    sdf_hdr, _sdf_data = read_sdf_file(args.inputfile)
    with open(args.outputfile, "w") as outfile:
        json.dump(sdf_hdr, outfile, indent=2, default=str)


if __name__ == "__main__":
    main()
