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
        \textit{...}
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
    """Removes all of a given tag from a given TeX file or list of files.

    Positional arguments:
    fname -- file path of file to be edited, or list of file paths
    tag -- tag to be removed

    Keyword arguments:
    comment -- True to process comment lines, False otherwise (default False)

    Returns:
    number of tag removals made

    The 'tag' argument should include only the letters that make up the name
    of the tag. For example, to remove all instances of the
        \textit{...}
    tag, pass the argument 'textit'.

    It is assumed that any instances of the given tag begin and end on the
    same line.
    """

    count = 0 # number of removals made

    # Convert input to a file list if needed
    if isinstance(fname, str) == True:
        fname = [fname]
    elif (isinstance(fname, list) or isinstance(fname, tuple)) == False:
        sys.exit("Input must be a file or list of files.")

    # Process all files
    for f in fname:

        # Get file path
        if os.path.exists(f) == False:
            sys.exit("Input path does not exist.")
        path = os.path.abspath(f)
        if os.path.isfile(path) == False:
            sys.exit("Input path is not a file name.")

        # Initialize output file
        outfile = path + ".tmp"

        # Write edits to a temporary file
        with open(f, mode='r') as fin:
            with open(outfile, mode='w') as fout:

                for line in fin:

                    # Split line at comment
                    if comment == True:
                        parts = re.split("(?<!\\\\)%", line)
                    else:
                        parts = [line]

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

def untag_folder(fname, tag, ext="tex", comment=False):
    """Removes all of a given tag from every TeX file in a given folder.

    Positional arguments:
    fname -- file path of the folder whose contents will be recursively edited
    tag -- tag to be removed

    Keyword arguments:
    ext -- string or list of strings specifying file types to process
        (default "tex")
    comment -- True to process comment lines, False otherwise (default False)

    Returns:
    number of tag removals made

    The 'tag' argument should include only the letters that make up the name
    of the tag. For example, to remove all instances of the
        \textit{...}
    tag, pass the argument 'textit'.

    It is assumed that any instances of the given tag begin and end on the
    same line.
    """

    count = 0 # number of removals made

    # Get directory path
    if os.path.exists(fname) == False:
        sys.exit("Input path does not exist.")
    path = os.path.absname(fname)
    if os.path.isdir(path) == False:
        sys.exit("Input path is not a directory name.")

    ###

#-----------------------------------------------------------------------------

if __name__ == "__main__":
    ###
    ### Add a -r argument to process a directory.
    #print(_untag_string("This is a \\textit{t\\textbf{e}st}.", "textit"))
    #print(_untag_string("This is a \\textit{test}.", "textit"))
    print(_untag_string("This is a \\textit{test.", "textit"))
