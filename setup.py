import os
import os.path

PKG = "aliasdir"
VERSION_PY = os.path.join(PKG, "version.py")

try:
    from ez_setup import use_setuptools
except ImportError:
    pass
else:
    use_setuptools(download_delay=0)

from setuptools import setup, find_packages
from distutils.core import setup, Command
from distutils.command.sdist import sdist as _sdist

rel_file = lambda *args: os.path.join(os.path.dirname(os.path.abspath(__file__)), *args)

def get_readme():
    return open(rel_file('README.mkd')).read()

def get_requirements():
    data = open(rel_file('pipfile')).read()
    lines = map(lambda s: s.strip(), data.splitlines())
    return filter(None, lines)

def update_version_py():
    if not os.path.isdir(".git"):
        print "This does not appear to be a Git repository."
        return
    try:
        p = subprocess.Popen(["git", "describe", "--dirty", "--always"],
                             stdout=subprocess.PIPE)
    except EnvironmentError:
        print "unable to run git describe"
        return
    if p.returncode != 0:
        print "unable to run git"
        return
    result = p.communicate()[0]
    with open(VERSION_PY, "w") as v:
        with open(VERSION_PY+".template") as t:
            v.write(t.read() % result)
    print "set %s to '%s'" % (VERSION_PY, ver)

def get_version():
    try:
        with open(VERSION_PY) as f:
            for line in f.readlines():
                mo = re.match("__version__ = '([^']+)'", line)
                if mo:
                    ver = mo.group(1)
                    return ver
    except EnvironmentError:
        pass
    return None

class Version(Command):
    description = "update version.py from Git repo"
    user_options = []
    boolean_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        update_version_py()
        print "Version is now", get_version()

class sdist(_sdist):
    def run(self):
        update_version_py()
        self.distribution.metadata.version = get_version()
        return _sdist.run(self)

setup_options = dict(
    name              = PKG,
    version           = get_version(),
    author            = "Kyle Gibson",
    author_email      = "kyle.gibson@frozenonline.com",
    description       = "Easy way to save your directories",
    license           = "MIT",
    url               = "http://github.com/kylegibson/python-aliasdir",
    packages          = find_packages(),
    long_description  = get_readme(),
    install_requires  = get_requirements(),
    entry_points      = {
        'console_scripts': 
            ['aliasdir = aliasdir.cli:main']
    },
    classifiers       = [
		"Environment :: Console",
		"Operating System :: Unix",
		"Programming Language :: Python",
		"Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    zip_safe=False,
)

setup(**setup_options)
