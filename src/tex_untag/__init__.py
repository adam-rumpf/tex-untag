"""A small script for removing markup tags from sets of TeX files.

This module includes two main public functions for removing markup tags from
TeX documents:
    untag_file -- removes tags from a file or list of files
    untag_folder -- recursively removes tags from all files in a directory

The removed tags are assumed to use the standard "\tag{...}" format, and the
functions that accept a tag string as an argument expect the exact text
falling between the "\" and the "{".
"""

from ._version import __author__, __version__
from .tex_untag import *
