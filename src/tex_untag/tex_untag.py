"""Defines the main TeX file processing script."""

from ._version import __author__, __version__

import os
import re

#-----------------------------------------------------------------------------

def _untag_string(s, tag):
    """Removes all of a given tag from a given string.

    Positional arguments:
    s -- string to be edited
    tag -- tag to be removed

    Returns:
    (string, int) tuple including the edited string and the number of removals
    made

    The 'tag' argument should include only the letters that make up the name
    of the tag. For example, to remove all instances of the
        \\textit{...}
    tag, pass the argument 'textit'.
    """

    ###
    return (s, 0)

#-----------------------------------------------------------------------------

def untag_file(fname, tag, comment=False):
    """Removes all of a given tag from a given TeX file.

    Positional arguments:
    fname -- file path of file to be edited
    tag -- tag to be removed

    Keyword arguments:
    comment -- True to process comment lines, False otherwise (default False)

    Returns:
    number of tag removals made

    The 'tag' argument should include only the letters that make up the name
    of the tag. For example, to remove all instances of the
        \\textit{...}
    tag, pass the argument 'textit'.
    """

    count = 0 # number of replacements made

    # Get file directory
    path = os.path.abspath(fname)
    outfile = path + ".tmp"

    # Write edits to a temporary file
    with open(fname, mode='r') as fin:
        with open(outfile, mode='w') as fout:

            for line in fin:

                # Split line at comment
                parts = re.split("(?<!\\\\)%", line)

                # Remove the tag from the pre-comment string
                lcount = 0 # number of replacements made in this line
                (parts[0], lcount) = _untag_string(parts[0], tag)
                count += lcount

                # Write edited line to temporary file
                print("%".join(parts), file=fout, end="")

    # Replace original file with temporary file
    os.remove(path)
    os.rename(outfile, path)

    return count
