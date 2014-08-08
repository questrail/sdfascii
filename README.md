# sdfascii

[![Build Status][travis image]][travis link]
[![PyPi Version][pypi ver image]][pypi ver link]
[![Coverage Status][coveralls image]][coveralls link]

A Python (2.6+/3.3+) module for reading Standard Data Format (SDF) and
ASCII files saved by HP/Agilent Dynamic Signal Analyzers (DSA).

The HP/Agilent 35670A Dynamic Signal Analyzer has the ability to save
files as either SDF or ASCII format.

## HP/Agilent DSA ASCII Format

Four files are created when saving to the HP/Agilent DSA ASCII format:

1. `.HDR` contains SDF header information
2. `.TXT` contains the y-axis information, preserving the same units as
   displayed on the analyzer screen when the trace was saved
3. `.X` contains the x-axis information
4. `.Z` contains the z-axis information, if the trace contains waterfall
   data

Source: Agilent discussion forum question [When I save the trace in the
ASCII format, there are 4 files created with extensions of .txt, .hdr,
.x, and .z. What are the contents of these files?][1]

## Contributing

[sdfascii][] is developed using [Scott Chacon][]'s [GitHub Flow][]. To
contribute, fork [sdfascii][], create a feature branch, and then submit
a pull request.  [GitHub Flow][] is summarized as:

- Anything in the `master` branch is deployable
- To work on something new, create a descriptively named branch off of
  `master` (e.g., `new-oauth2-scopes`)
- Commit to that branch locally and regularly push your work to the same
  named branch on the server
- When you need feedback or help, or you think the branch is ready for
  merging, open a [pull request][].
- After someone else has reviewed and signed off on the feature, you can
  merge it into master.
- Once it is merged and pushed to `master`, you can and *should* deploy
  immediately.

## License

[sdfascii][] is released under the MIT license. Please see the
[LICENSE.txt][] file for more information.

[1]: http://www.home.agilent.com/agilent/editorial.jspx?ckey=628664&id=628664&nid=-536902471.0.00&lc=eng&cc=IN
[coveralls image]:http://img.shields.io/coveralls/questrail/sdfascii/master.svg
[coveralls link]: https://coveralls.io/r/questrail/sdfascii
[github flow]: http://scottchacon.com/2011/08/31/github-flow.html
[LICENSE.txt]: https://github.com/questrail/sdfascii/blob/master/LICENSE.txt
[numpy]: http://www.numpy.org
[pull request]: https://help.github.com/articles/using-pull-requests
[pypi ver image]: http://img.shields.io/pypi/v/sdfascii.svg
[pypi ver link]: https://pypi.python.org/pypi/sdfascii/
[scott chacon]: http://scottchacon.com/about.html
[sdfascii]: https://github.com/questrail/sdfascii
[travis image]: http://img.shields.io/travis/questrail/sdfascii/master.svg
[travis link]: https://travis-ci.org/questrail/sdfascii
