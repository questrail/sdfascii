# Copyright (c) 2013-2026 The sdfascii developers. All rights reserved.
# Project site: https://github.com/questrail/sdfascii
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Check a built wheel from outside the source tree.

Every other check in this project runs against `src/`, so a packaging mistake
that leaves a module or `py.typed` out of the distribution passes ruff,
pyright, and the whole suite and ships anyway. Run this with the wheel
installed somewhere `src/` cannot be reached:

    uv run --isolated --no-project --with dist/*.whl \
        python scripts/smoke_test_wheel.py 0.8.2

Python puts this file's own directory on `sys.path` rather than the working
directory, so `import sdfascii` below can only resolve to the installed wheel.
"""

import argparse
import importlib.metadata
import importlib.resources
import importlib.util

import sdfascii


def main(expected: str) -> None:
    installed = importlib.metadata.version("sdfascii")
    if installed != expected:
        raise SystemExit(f"The wheel installed {installed}, expected {expected}")

    # __version__ is read back from the installed metadata rather than written
    # in the source, so a wheel that failed to record it would report the
    # wrong thing here rather than in a bug report.
    if sdfascii.__version__ != expected:
        raise SystemExit(
            f"sdfascii.__version__ is {sdfascii.__version__}, expected {expected}"
        )

    for name in sdfascii.__all__:
        if not callable(getattr(sdfascii, name)):
            raise SystemExit(f"{name} is missing from the wheel")

    # `python -m sdfascii` is the CLI, and __main__.py is a second file in the
    # package: a wheel that shipped __init__.py alone would pass every check
    # above. Located rather than imported, since importing it under any name
    # but __main__ is not what the CLI does.
    if importlib.util.find_spec("sdfascii.__main__") is None:
        raise SystemExit("The wheel is missing __main__.py")

    if not importlib.resources.files("sdfascii").joinpath("py.typed").is_file():
        raise SystemExit("The wheel is missing py.typed")

    print(f"sdfascii {installed} imported from {sdfascii.__file__}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check a built sdfascii wheel from outside the source tree."
    )
    parser.add_argument(
        "expected_version", help="the version the wheel is expected to install"
    )
    main(parser.parse_args().expected_version)
