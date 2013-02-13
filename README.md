# sdfascii

A Python module for reading Standard Data Format (SDF) and ASCII files
saved by HP/Agilent Dynamic Signal Analyzers (DSA).

The HP/Agilent 35670A Dynamic Signal Analyzer has the ability to save
files as either SDF or ASCII format.

## HP/Agilent DSA ASCII Format

Four files are created when saving to the HP/Agilent DSA ASCII format:

1. `.HDR` contains SDF header information
2. `.TXT` contains the y-axis information, preserving the same units as
   displayed on the analyzer screen when the trace was saved
3. `.X` contains the x-axis information
4. `.Z` contines the z-axis information, if the trace contains waterfall
   data 

Source: Agilent discussion forum question [When I save the trace in the
ASCII format, there are 4 files created with extensions of .txt, .hdr,
.x, and .z. What are the contents of these files?][1]

[1]:
http://www.home.agilent.com/agilent/editorial.jspx?ckey=628664&id=628664&nid=-536902471.0.00&lc=eng&cc=IN
