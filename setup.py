import setuptools
import codecs
import os.path

# Get metadata from version file (additional metadata defined in setup.cfg)

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_attr(rel_path, attr):
    for line in read("src/tex_untag/" + rel_path).splitlines():
        if line.startswith(attr):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find '" + attr + "' string.")

setuptools.setup(author=get_attr("_version.py", "__author__"),
                 version=get_attr("_version.py", "__version__"),
                 author_email=get_attr("_version.py", "_author_email"))
