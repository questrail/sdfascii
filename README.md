# sdfascii

[![PyPI Version][pypi ver image]][pypi ver link]
[![Python Versions][pyversions image]][pypi ver link]
[![CI Status][ci image]][ci link]
[![Coverage Status][coveralls image]][coveralls link]
[![License Badge][license image]][LICENSE.txt]

[sdfascii][] is a Python 3.12+ module for reading the HP/Agilent Standard Data
Format (SDF) binary files and the ASCII files saved by HP/Agilent Dynamic Signal
Analyzers (DSA). A few examples of using [sdfascii][] can be found at [this
example repository][examples].

The HP/Agilent 35670A Dynamic Signal Analyzer has the ability to save
files as either SDF or ASCII format.

**WARNING:** Only SDF revision 2 is read in full. The revision 1 and 3 branches
decode the fields the revisions share and leave the rest.

## HP/Agilent SDF Binary Format

The ["Standard Data Format Utilities User's Guide"][sdf guide] version
B.02.01, P/N 5963-1715 was used to determine the SDF file format while
developing [sdfascii][].

## HP/Agilent DSA ASCII Format

Four files are created when saving to the HP/Agilent DSA ASCII format:

1. `.HDR` contains SDF header information
2. `.TXT` contains the y-axis information, preserving the same units as
   displayed on the analyzer screen when the trace was saved
3. `.X` contains the x-axis information
4. `.Z` contains the z-axis information, if the trace contains waterfall
   data

## Installation

You can install [sdfascii][] either via the Python Package Index (PyPI) or from
source.

To add it to a project managed with [uv][], which records it in your
`pyproject.toml` and lock file:

```bash
$ uv add sdfascii
```

Or to install it with pip:

```bash
$ pip install sdfascii
```

**Source:** https://github.com/questrail/sdfascii

## Requirements

[sdfascii][] requires the following Python package:

* [numpy][]

## Public API

The following functions are provided:

- `read_sdf_file(sdf_filename)` returns the header as a dictionary and the
  y-axis data as a numpy array. The data is `None` if the file carries no
  y-data record.
- `read_ascii_files(input_ascii_base_filename)` reads the `.X` and `.TXT`
  files sharing the given base name and returns them as a structured numpy
  array with `frequency` and `amplitude` fields.

## Command Line

`python -m sdfascii` parses an SDF file and writes its header to JSON, which is
how the files in `examples/` are produced:

```bash
$ python -m sdfascii sdf examples/HP35670A.DAT examples/hp35670a.json
```

## Contributing

Contributions are welcome! To contribute please:

1. Fork the repository
2. Create a feature branch
3. Add code and tests
4. Pass lint and tests
5. Submit a [pull request][]

## Development Setup

The project is managed with [uv][], and the development tasks are [just][]
recipes.

```bash
$ brew install uv just
```

`uv sync` creates the virtualenv and installs the dependencies, including the
development group, and `just` on its own lists the available recipes.

```bash
$ uv sync
$ just
```

The most common recipes are:

```bash
$ just test       # Run the tests using pytest
$ just lint       # Check lint, formatting, types, and workflows
$ just fix        # Lint and format the code using ruff, applying fixes
$ just cov        # Run the tests and report coverage
$ just examples   # Regenerate the parsed header JSON in examples/
$ just add X      # Add X as a dependency
$ just out        # List the outdated dependencies
```

[ruff][] and [pyright][] are deliberately absent from that `brew install` line.
Both are dev dependencies pinned in `uv.lock` and reached through `uv run`, so
every recipe and every CI job uses the same version. A `brew install ruff` would
put a second, unpinned copy on the path for an editor to find, and ruff releases
change how code is formatted: the editor would then reformat code that
`ruff format --check` rejects on the next run.

### Releasing to PyPI

`just release` cuts the release. It first checks that a release is possible at
all, then lints, type checks, and tests, then shows the entries waiting under
Unreleased and the version each kind of bump would produce, and asks which to
cut. Once answered it bumps the version, closes out the CHANGELOG, updates the
lock file, commits, and tags. Pushing the tag is what publishes.

```bash
$ just release
...
Which release? [1] 2

Tagged v0.9.0. Publish it with:

    git push --follow-tags
```

The tag push runs the [release workflow][], which waits on the whole [CI
workflow][ci link] before it does anything else: the 3.12, 3.13, and 3.14 matrix
and the dependency floor job. It then checks that the tagged commit is on
`master`, since a tag is only a pointer and one placed anywhere else would
otherwise publish whatever it points at, rechecks the tag against the version in
`pyproject.toml`, and builds.

Every check to that point runs against the source tree, so the workflow then
installs the wheel it just built somewhere `src/` is not on the path and
exercises it there, which is the only step that can catch a packaging mistake.
It uploads once that passes. There is no PyPI API token anywhere: the workflow
authenticates with [trusted publishing][], which mints a short lived credential
from the GitHub OIDC identity of that run. That same identity signs a [PEP
740][] attestation for each distribution, which PyPI serves beside the file it
attests.

Uploading is followed by a [GitHub release][releases] for the tag, carrying the
CHANGELOG section for that version as its notes and the built distributions as
its assets.

Pushing the tag is the point of no return, since PyPI never lets a version
number be reused. Everything `just release` does is local and amendable until
then, and it refuses to start against a dirty working tree, off `master`, on a
`master` behind its upstream, with a CHANGELOG whose Unreleased section is
empty, or when the tag it would create already exists. `just release-check` runs
those refusals on their own.

`just build` runs the same checks and produces the same distributions without
releasing anything, which is the way to inspect what CI would upload.

This depends on one piece of configuration that lives outside the repository. A
[trusted publisher][trusted publishing] has to be registered for `sdfascii` on
PyPI, pointing at the `questrail/sdfascii` repository, the `release.yml`
workflow, and the `pypi` environment. It is a one time setup per project.

## License

[sdfascii][] is released under the MIT license. Please see the
[LICENSE.txt][] file for more information.

[ci image]: https://github.com/questrail/sdfascii/actions/workflows/ci.yml/badge.svg?branch=master
[ci link]: https://github.com/questrail/sdfascii/actions/workflows/ci.yml
[coveralls image]: https://coveralls.io/repos/github/questrail/sdfascii/badge.svg?branch=master
[coveralls link]: https://coveralls.io/github/questrail/sdfascii?branch=master
[examples]: https://github.com/matthewrankin/sdfascii-examples
[just]: https://just.systems
[LICENSE.txt]: https://github.com/questrail/sdfascii/blob/master/LICENSE.txt
[license image]: https://img.shields.io/pypi/l/sdfascii.svg
[numpy]: https://numpy.org
[PEP 740]: https://peps.python.org/pep-0740/
[pull request]: https://help.github.com/articles/using-pull-requests
[pypi ver image]: https://img.shields.io/pypi/v/sdfascii.svg
[pypi ver link]: https://pypi.python.org/pypi/sdfascii/
[pyright]: https://microsoft.github.io/pyright/
[pyversions image]: https://img.shields.io/pypi/pyversions/sdfascii.svg
[release workflow]: https://github.com/questrail/sdfascii/blob/master/.github/workflows/release.yml
[releases]: https://github.com/questrail/sdfascii/releases
[ruff]: https://docs.astral.sh/ruff/
[sdf guide]: https://www.keysight.com/us/en/assets/9018-05246/user-manuals/9018-05246.pdf
[sdfascii]: https://github.com/questrail/sdfascii
[trusted publishing]: https://docs.pypi.org/trusted-publishers/
[uv]: https://docs.astral.sh/uv/
