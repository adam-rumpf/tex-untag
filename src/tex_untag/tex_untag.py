"""Defines the main TeX file processing scripts."""

from ._version import __author__, __version__, _author_email, _copyright_year

import argparse
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
        \textit{...}
    tag, pass the argument 'textit'.

    It is assumed that any instances of the given tag begin and end on the
    same line.
    """

    # Define \tag{...} head regex pattern
    head = "\\" + tag + "{"

    # Do nothing if tag is absent
    if head not in s:
        return (s, 0)
    
    # Otherwise find the first tag head
    start = s.find(head) # position of first tag head
    out = s[:start] # take beginning of string
    count = 1 # number of tag removals made
    
    # Look for closing brackets to match tag head
    i = start + len(head) # current position within string segment
    depth = 1 # bracket depth
    while i < len(s) - 1 and depth > 0:
        i += 1
        if s[i] == "{" and s[i-1:i+1] != "\{":
            depth += 1
        elif s[i] == "}" and s[i-1:i+1] != "\}":
            depth -= 1

    if depth <= 0:
        # If a closing bracket was found, take everything around it
        out += s[start+len(head):i] + s[i+1:]
    else:
        # Otherwise take the entire tail of the string
        out += s[start+len(head):]
    
    # Recursively remove tags from remainder
    (out, rcount) = _untag_string(out, tag)
    count += rcount
    
    return (out, count)

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
        raise TypeError("input must be a file or list of files")

    # Process all files
    for f in fname:

        # Get file path
        if os.path.exists(f) == False:
            raise FileNotFoundError("input path does not exist")
        path = os.path.abspath(f)
        if os.path.isfile(path) == False:
            raise FileNotFoundError("input path is not a file name")

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

def untag_folder(folder, tag, ext="tex", comment=False):
    """Removes all of a given tag from every TeX file in a given folder.

    Positional arguments:
    folder -- directory to recursively process
    tag -- tag to be removed

    Keyword arguments:
    ext -- case-insensitive string or list of strings specifying file types to
        process (default "tex"); using the string "*" converts all files
        regardless of extension
    comment -- True to process comment lines, False otherwise (default False)

    Returns:
    (int, int) tuple with number of tag removals made and number of files
        processed

    The 'tag' argument should include only the letters that make up the name
    of the tag. For example, to remove all instances of the
        \textit{...}
    tag, pass the argument 'textit'.

    It is assumed that any instances of the given tag begin and end on the
    same line.
    """

    # Convert extension list to tuple
    if isinstance(ext, str) == True:
        ext = [ext]
    elif isinstance(ext, tuple) == True:
        ext = list(ext)
    elif isinstance(ext, list) == False:
        raise TypeError("file extensions must be a string or list of strings")

    # Convert extensions into a lowercase tuple
    for i in range(len(ext)):
        ext[i] = ext[i].lower()
    ext = tuple(ext)

    # Get directory path
    path = os.path.abspath(folder)
    if os.path.exists(path) == False:
        raise NotADirectoryError("input path does not exist")
    if os.path.isdir(path) == False:
        raise NotADirectoryError("input path is not a directory name")

    # Generate file list
    flist = [] # list of files to process
    for root, _, files in os.walk(path):
        for f in files:

            # Skip excluded file types
            if "*" not in ext and f.lower().endswith(ext) == False:
                continue

            # Collect remaining files in list
            flist.append(os.path.join(root, f))

    # Process all selected files
    return (untag_file(flist, tag=tag, comment=comment), len(flist))

#-----------------------------------------------------------------------------

def main():
    """Main driver for command line usage of the tag remover.

    Reads command line arguments to attempt to process a file or files.
    """

    # Define documentation strings
    desc = "A script for removing markup tags from a set of TeX files."
    vers = ("TeX Untag v" + __version__ + "\nCopyright (c) " + _copyright_year
            + " " + __author__ + "\n" + _author_email)
    epil = """
    This script removes a given TeX markup tag from a given file or set of
    files. The tag is assumed to use the form "\\tag{...}". The given tag
    should include the full text that falls between the '\\' and '{'
    characters.

    The file (-f) argument can include a single file, a list of files, or a
    directory, in which case the recursive (-r) flag should be used.

    The extension (-e) argument is optional, and if absent only 'tex' files
    will be processed. Otherwise it can include either a list of file
    extensions or the '*' character, in which case all files will be included.
    """

    # Define argument parser
    parser = argparse.ArgumentParser(description=desc, epilog=epil,
                         formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-v", "--version", action="version", version=vers)
    parser.add_argument("-f", "--file", nargs="*", dest="files",
                        help="file, list of files, or directory to process " +
                        "(if blank and --recursive, uses current working" +
                        " directory)")
    parser.add_argument("-t", "--tag", required=True, dest="tag",
                        help="tag to remove from files")
    parser.add_argument("-e", "--extension", nargs="*", dest="extensions",
                        default=["tex"],
                        help="file extensions to process (default only tex)")
    parser.add_argument("-q", "--quiet", action="store_true", dest="quiet",
                        help="silence result message")
    parser.add_argument("-r", "--recursive", action="store_true",
                        dest="recursive",
                        help="recursively process all files in the given "+
                             "directory")
    parser.add_argument("-c", "--comments", action="store_true",
                        dest="comment",
                        help="removes tags even in comments")

    # Parse arguments
    args = parser.parse_args()

    # Handle empty file list
    if isinstance(args.files, list) == False or len(args.files) == 0:
        if args.recursive == True:
            # If no folder given, default to current working directory
            args.files = os.getcwd()
        else:
            # Otherwise quit
            raise SyntaxError("must supply at least one file name")

    # Determine behavior depending on arguments
    if args.recursive == True:
        # Recursive processing
        (rm, fl) = untag_folder(args.files, args.tag, ext=args.extensions,
                                comment=args.comment)
        if args.quiet == False:
            print("A total of " + str(rm) + " '" + args.tag + "' tags were " +
                  "removed from " + str(fl) + " file(s).")

    else:
        # File or file list processing
        rm = untag_file(args.files, args.tag, comment=args.comment)
        if args.quiet == False:
            if len(args.files) > 1:
                print("A total of " + str(rm) + " '" + args.tag +
                      "' tags were removed from " + str(len(args.quiet)) +
                      " files.")
            else:
                print("A total of " + str(rm) + " '" + args.tag +
                      "' tags were removed.")

#-----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
