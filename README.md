# TeX Untag

<a href="https://pypi.org/project/tex-untag"><img src="https://img.shields.io/pypi/v/tex-untag?logo=pypi&logoColor=white"/></a> <a href="https://github.com/adam-rumpf/tex-untag"><img src="https://img.shields.io/github/v/tag/adam-rumpf/tex-untag?logo=github"></a> <a href="https://pypi.org/project/tex-untag/#history"><img src="https://img.shields.io/pypi/status/tex-untag"/></a> <a href="https://www.python.org/"><img src="https://img.shields.io/pypi/pyversions/tex-untag?logo=python&logoColor=white"></a> <a href="https://github.com/adam-rumpf/tex-untag/blob/main/LICENSE"><img src="https://img.shields.io/github/license/adam-rumpf/tex-untag"/></a> <a href="https://github.com/adam-rumpf/tex-untag/commits/main"><img src="https://img.shields.io/maintenance/yes/2021"/></a>

A script for removing all of a given markup tag from a set of TeX files.

## Description

This is a small script for removing markup tags of the form `\tag{...}` from a [TeX file](https://www.latex-project.org/) or set of TeX files. It can be imported using
```python
import tex_untag
```
The user can specify the exact tag name string that they want removed, and all instances within the specified file or files will be removed. For example, executing the function
```python
untag_file("report.tex", "textit")
```
would remove all italic text tags of the form `\textit{...}` from the document `report.tex`, while
```python
untag_file("report.tex", "textcolor{red}")
```
would remove all red text tags of the form `\textcolor{red}{...}`. Comments are (optionally) ignored during this process.

Note that, since this process involves overwriting existing files, it is recommended that you back up your data before attempting to use it.

## Functions

This module defines two main public functions:
* `tex_untag.untag_file(fname, tag[, comment])`: Removes the given `tag` from a single file or a list of files called `fname`. The optional `comment` boolean specifies whether to remove tags from comments (default `False`). Returns the total number of tag removals made.
* `tex_untag.untag_folder(folder, tag[, ext][, comment])`: Removes the given `tag` recursively from every file within the given `folder` and its subfolders. The optional `ext` argument is a string or list of strings specifying which file extensions to include (default `tex`), while the optional `comment` boolean specifies whether to remove tags from comments (default `False`). Returns the total number of tag removals made and the total number of files processed.

## Command Line Usage

This package defines a console script `tex-untag` which can be used as follows:
```
usage: tex-untag [-h] [-v] [-f [FILES ...]] -t TAG [-e [EXTENSIONS ...]] [-q] [-r] [-c]

A script for removing markup tags from a set of TeX files.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -f [FILES ...], --file [FILES ...]
                        file, list of files, or directory to process (if blank and
                        --recursive, uses current working directory)
  -t TAG, --tag TAG     tag to remove from files
  -e [EXTENSIONS ...], --extension [EXTENSIONS ...]
                        file extensions to process (default only tex)
  -q, --quiet           silence result message
  -r, --recursive       recursively process all files in the given directory
  -c, --comments        removes tags even in comments

This script removes a given TeX markup tag from a given file or set of files. The tag is
assumed to use the form "\tag{...}". The given tag should include the full text that falls
between the '\' and '{' characters.

The file (-f) argument can include a single file, a list of files, or a directory, in which
case the recursive (-r) flag should be used.

The extension (-e) argument is optional, and if absent only 'tex' files will be processed.
Otherwise it can include either a list of file extensions or the '*' character, in which
case all files will be included.
```

For example,
```
$ tex-untag -f introduction.tex results.tex conclusion.tex -t textit -c
```
would remove all italic `\textit{...}` tags from the three local files `introduction.tex`, `results.tex`, and `conclusion.tex`, including those located inside comments, while
```
$ tex-untag -f report -t textcolor{red} -e tex bbl --recursive
```
would remove all red text `\textcolor{red}{...}` tags from every `.tex` or `.bbl` file within the local directory `report/`.
