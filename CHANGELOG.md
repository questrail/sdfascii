# CHANGELOG.md

This file contains all notable changes to the [sdfascii][] project.

## Unreleased

### Added

- Continuous integration on GitHub Actions, replacing a `.travis.yml` that
  pointed at travis-ci.org and had not run in years. Every push and pull
  request lints, checks formatting, type checks, and runs the suite on 3.12,
  3.13, and 3.14, the versions the classifiers claim. A second job installs
  the oldest numpy `pyproject.toml` allows, so the floor is a tested promise
  rather than a hopeful one. A third audits the workflows with [zizmor][],
  since they are the part of the repository that can mint a PyPI credential.
  Coverage goes to Coveralls from the 3.13 leg.
- Releases publish from a tag rather than from a laptop. `just release`
  refuses a dirty tree, a branch other than `master`, a `master` behind its
  upstream, an empty Unreleased section, or an existing tag; then lints and
  tests; then shows the entries waiting to ship beside the version each kind
  of bump would produce, and asks which to cut. It bumps the version, closes
  out the CHANGELOG, commits, and tags. Pushing the tag is what publishes.
  `just release-check` runs the refusals on their own.
- The release workflow waits on the whole CI run before it uploads anything,
  confirms the tag sits on `master` and matches the version in
  `pyproject.toml`, and authenticates to PyPI with [trusted publishing][], so
  there is no API token to paste, store, or leak. It signs a [PEP 740][]
  attestation for each distribution against the same identity, and creates a
  GitHub release carrying the CHANGELOG section for that version as its notes.
- Dependabot keeps the pinned actions and the lock file moving. The actions in
  both workflows are pinned to commit SHAs, so a fix published upstream does
  not reach this repository the way it would behind a moving tag; without
  something to move them, pinning would amount to staying on one commit
  forever. It reads `pyproject.toml` and `uv.lock` together as well, so a
  dependency update arrives as a lock file change that CI checks with
  `uv sync --locked`.
- `scripts/smoke_test_wheel.py`, which installs the built wheel where `src/`
  cannot be reached and checks the version, `__version__`, every name in
  `__all__`, `__main__.py`, and `py.typed`. Every other check runs against the
  source tree, so this is the only one that can catch a packaging mistake.
  `just build` runs it after building.
- `just cov`, which runs the suite under coverage and writes both a terminal
  summary and `htmlcov/`, and the `pytest-cov` it needs. A floor of 88%, what
  the suite covers today, means uncovered code has to arrive with either a
  test or a deliberate edit to that line.
- Tests for the command line entry point, which had none: one that parses a
  real SDF file to JSON and reads the result back, and one that pins the
  refusal recorded below.
- `py.typed`, so that the type hints already written reach anyone installing
  the package. Without the marker a type checker treats an installed package
  as untyped and ignores its annotations.
- `SDF_REVISION_1`, `SDF_REVISION_2`, and `SDF_REVISION_3`, naming the three
  values the `sdf_revision` field of a file header is compared against, beside
  the record type constants that were already named.

### Fixed

- `_decode_sdf_data_hdr()` never bound `temp_data_hdr` on the revision 3
  branch, so decoding a revision 3 data header raised `UnboundLocalError` from
  the `return` below rather than giving back the fields the revisions share.
  The file and measurement header decoders beside it both cast to their V3
  type; this one was the odd one out, in the branch and in the return
  annotation. Found by [pyright][].
- `read_sdf_file()` raised `UnboundLocalError` on a file whose header reports
  no y-data record. Every assignment to `sdf_data` sat inside the branch that
  a negative `offset_ydata_record` skips, so the guard written to let those
  files through was the one thing that could not survive the return. It now
  returns `None` for the data, with the header decoded as before.
- `read_ascii_files()` reached numpy's record array constructor through
  `np.core`, which numpy 2.0 renamed to `np._core` and left behind as a shim
  that warns on every attribute access. It uses `np.rec`, the supported
  spelling.
- The `zip()` calls that pair a struct format string with the field names
  beside it pass `strict=True`, so a format string and a key list that fall
  out of step raise rather than silently producing a short dictionary.

### Changed

- Moved to [uv][] and a `pyproject.toml` built by hatchling, replacing
  `setup.py`, `setup.cfg`, `requirements.txt`, and `MANIFEST.in`. The sdist
  names what it ships rather than taking hatchling's default of everything
  `.gitignore` does not exclude, and leaves out `PIC3KHZ.JPG`, a 2.7 MB
  photograph of the bench that is 99% of what the sdist would otherwise weigh
  and that nothing in the suite reads.
- Replaced the [Invoke][] `tasks.py` with a [just][] `Justfile`, matching the
  recipes and groups used by the other questrail projects. The `example1` and
  `example2` tasks become one `just examples` recipe that regenerates both
  files.
- Swapped the tooling: ruff for pep8/pep8-naming, pytest for nose2, and
  [pyright][] for mypy. The code was reformatted by ruff, and the `Dict` and
  `Union` annotations were rewritten in the built-in spellings.
- Moved the module to a src layout at `src/sdfascii/__init__.py`, and the
  block that used to sit under `if __name__ == "__main__":` at the foot of it
  to `src/sdfascii/__main__.py`. Under a package nothing would ever have
  reached that block; `python -m sdfascii` runs it now. `import sdfascii` and
  everything reached through it are unchanged.
- `python -m sdfascii ascii ...` is refused rather than accepted. `ascii` was
  a documented choice whose body was never written: a run named the file type,
  passed the arguments, wrote nothing, and exited 0. Naming the one implemented
  choice turns that silence into an argparse error.
- The version is written in `pyproject.toml` rather than in the module, and
  `sdfascii.__version__` now reads it back from the installed distribution
  metadata. Its value is unchanged and every caller keeps working. The version
  had to move for `uv version` to be able to read or bump it, which is what the
  release recipe is built on; uv refuses a project whose version is dynamic.
- List `369937+matthewrankin@users.noreply.github.com` as the author address in
  `pyproject.toml`, replacing a work address. It is what `Author-email` carries
  in the built metadata and what PyPI shows on the project page, so it changes
  there from the next release onward.
- The license is declared as an SPDX expression with `license-files`, which is
  what replaced the `License ::` classifier that used to carry it. It is also
  what puts `LICENSE.txt` into `dist-info/licenses/`.
- `.python-version` is tracked, so that a contributor's `uv sync` builds
  against the interpreter the release is built on rather than whatever uv
  happens to find.
- Every heading in this file carries an ISO date. The release workflow reads
  the section for the version it is publishing out of this file and matches on
  that shape, and half the headings were written `18-Aug-23`.
- Raised the minimum Python to 3.12 and numpy to 2.2, and dropped the 3.8
  through 3.11 classifiers.

### Removed

- `AUTHORS.md`, along with the pointer to it in the copyright notice. It listed
  one author, no maintainers, and no contributors, and it does not travel in
  the wheel: `license-files` carries `LICENSE.txt` into `dist-info/licenses/`
  and nothing carries the other. `git log` is the record.
- `invoke release --deploy`, which tagged, pushed, built, and uploaded from a
  laptop with whatever credentials were lying around, printing a checklist of
  questions to answer from memory first. The release workflow replaces it.
- `mypy.ini` and `unittest.cfg`, whose tools are gone.
- The Python 2 era `.pyc` files, `sdfascii.egg-info/`, and the stale
  `__pycache__` directories that had been sitting in the working tree. One of
  them, a `sdfascii.pyc` compiled by Python 3.4, shadowed the package and made
  the suite fail to import it.

## v0.8.2 - 2023-08-18
- Fixed the data type for y-data complex values (use >c8 not >c16).

## v0.8.1 - 2023-08-18
- Fixed the fix for y-data number of points with complex values.

## v0.8.0 - 2023-08-18
- Fixed error in number of y-data points, when the values are complex.

## v0.7.0 - 2023-08-18
- Fixed error parsing complex data.
- Added examples to tasks.

## v0.6.1 - 2023-08-18
- Fixed upload to PyPi issue.

## v0.6.0 - 2023-08-18
- Added mypy and removeed six and pandoc.
- Removed Python 3.4, 3.5, 3.6, and 3.7
- Added Python 3.10 and 3.11
- Add missing window types, measurement types, and data types.
- Fix trace correction factor.

## v0.5.4 - 2022-06-25
- Installed twine in order to upload to pypi.

## v0.5.3 - 2022-06-25
- Installed build in order to upload to pypi.

## v0.5.2 - 2022-06-25
- Use twine to upload to pypi.

## v0.5.1 - 2022-06-25
- Actually released to pypi.

## v0.5.0 - 2022-06-24
- Updated dependencies.

## v0.4.1 - 2017-11-16
- Remove Python 2.6 and 3.3 testing in Travis-CI.
- Remove OS X testing in Travis-CI.

## v0.4.0 - 2017-11-07
- Updated dependencies.
- Added Python 3.6 to travis.yml.

## v0.3.1 - 2015-08-20

### Added
- Invoke `inv test` task now checks for test coverage.

### Changed
- Migrated from Travis legacy to container-based infrastructure.
- Updated numpy from 1.8.1 to 1.9.2.
- Updated other pip requirements.

## v0.2.3 - 2014-08-08

### Enhancements
- Add license badge
- Renamed AUTHORS.txt to AUTHORS.md
- Updated README.md

## v0.2.2 - 2014-08-08

### Enhancements
- Changed to shields.io for badge service


## v0.2.1 - 2014-08-08

### Bugs
- Fixed unit tests in Python 2.6 [#6][]


## v0.2 - 2014-08-07

### Enhancements
- Made Python 3.3/3.4 compatible [#5][]


## v0.1 - 2014-08-07

### Enhancements
- Add Travis-CI testing [#1][]
- Create invoke tasks to automate PyPi deploy [#2][]
- Made PEP8 compliant [#3][], [#4][]

[#1]: https://github.com/questrail/sdfascii/issues/1
[#2]: https://github.com/questrail/sdfascii/issues/2
[#3]: https://github.com/questrail/sdfascii/issues/3
[#4]: https://github.com/questrail/sdfascii/issues/4
[#5]: https://github.com/questrail/sdfascii/issues/5
[#6]: https://github.com/questrail/sdfascii/issues/6
[invoke]: https://www.pyinvoke.org/
[just]: https://just.systems
[PEP 740]: https://peps.python.org/pep-0740/
[pyright]: https://microsoft.github.io/pyright/
[sdfascii]: https://github.com/questrail/sdfascii
[trusted publishing]: https://docs.pypi.org/trusted-publishers/
[uv]: https://docs.astral.sh/uv/
[zizmor]: https://docs.zizmor.sh/
