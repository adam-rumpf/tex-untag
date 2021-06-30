"""Defines the main TeX file processing script."""

###
if __name__ != "__main__":
    from ._version import __author__, __version__

import os
import re
import sys

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

    It is assumed that any instances of the given tag begin and end on the
    same line.
    """

    count = 0 # number of removals made
    out = "" # output string

    # Define \tag{...} head regex pattern
    head = "\\\\" + tag + "\\{"

    # Split string at tag heads
    parts = re.split(head, s)
    out = parts[0]

    # Look for closing brackets to match to tag heads
    overflow = False # whether the line ends with an open bracket
    i = 0 # current line part
    while i < len(parts) - 1:
        i += 1
        depth = 1 # bracket depth
        j = 0 # position within string segment

        while depth > 0 and j < len(parts[i]) - 1:
            j += 1
            if parts[i][j] == "{" and parts[i][j-1:j+1] != "\{":
                depth += 1
            elif parts[i][j] == "}" and parts[i][j-1:j+1] != "\}":
                depth -= 1

        if depth == 0:
            # If closing bracket was found, remove it
            count += 1
            out += parts[i][:j] + parts[i][j+1:]
        else:
            # Otherwise keep the full string and break
            overflow = True
            break

    # If the line oveflowed, include the remainder unaltered
    if overflow == True:
        head = "\\" + tag + "{"
        out += head + head.join(parts[i:])

    return (out, count)

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

    It is assumed that any instances of the given tag begin and end on the
    same line.
    """

    count = 0 # number of removals made

    # Get file directory
    path = os.path.abspath(fname)
    if os.path.isfile(path) == False:
        sys.exit("Input path is not a file name.")
    if os.path.exists(path) == False:
        sys.exit("Input path does not exist.")

    # Initialize output file
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

#-----------------------------------------------------------------------------

if __name__ == "__main__":
    ###
    ### Add a -r argument to process a directory.
    #print(_untag_string("This is a \\textit{t\\textbf{e}st}.", "textit"))
    #print(_untag_string("This is a \\textit{test}.", "textit"))
    print(_untag_string("This is a \\textit{test.", "textit"))
