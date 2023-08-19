# sdfascii

[![PyPi Version][pypi ver image]][pypi ver link]
[![Build Status][travis image]][travis link]
[![Coverage Status][coveralls image]][coveralls link]
[![License Badge][license image]][LICENSE.txt]

[sdfascii][] is a Python (3.8+) module for reading the HP/Agilent Standard Data
Format (SDF) binary files and the ASCII files saved by HP/Agilent Dynamic Signal
Analyzers (DSA). A few examples of using [sdfascii][] can be found at [this
example repository][examples].

The HP/Agilent 35670A Dynamic Signal Analyzer has the ability to save
files as either SDF or ASCII format.

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

## Contributing

Contributions are welcome! To contribute please:

1. Fork the repository
2. Create a feature branch
3. Add code and tests
4. Pass lint and tests
5. Submit a [pull request][]

## Development Setup

### Development Setup Using pyenv

Use the following commands to create a Python 3.9.9 virtualenv using [pyenv][]
and [pyenv-virtualenv][], install the requirements in the virtualenv named
`sdfascii`, and list the available [Invoke][] tasks.

```bash
$ pyenv virtualenv 3.11 sdfascii
$ pyenv activate sdfascii
$ pip install --upgrade pip
$ pip install -r requirements.txt
$ inv -l
```

## License

[sdfascii][] is released under the MIT license. Please see the
[LICENSE.txt][] file for more information.

[coveralls image]:https://img.shields.io/coveralls/questrail/sdfascii/master.svg
[coveralls link]: https://coveralls.io/r/questrail/sdfascii
[examples]: https://github.com/matthewrankin/sdfascii-examples
[invoke]: https://www.pyinvoke.org/
[LICENSE.txt]: https://github.com/questrail/sdfascii/blob/master/LICENSE.txt
[license image]: http://img.shields.io/pypi/l/sdfascii.svg
[numpy]: http://www.numpy.org
[pull request]: https://help.github.com/articles/using-pull-requests
[pyenv]: https://github.com/pyenv/pyenv
[pyenv-install]: https://github.com/pyenv/pyenv#installation
[pyenv-virtualenv]: https://github.com/pyenv/pyenv-virtualenv
[pypi ver image]: https://img.shields.io/pypi/v/sdfascii.svg
[pypi ver link]: https://pypi.python.org/pypi/sdfascii/
[sdf guide]: https://www.keysight.com/us/en/assets/9018-05246/user-manuals/9018-05246.pdf
[sdfascii]: https://github.com/questrail/sdfascii
[travis image]: http://img.shields.io/travis/questrail/sdfascii/master.svg
[travis link]: https://travis-ci.org/questrail/sdfascii
