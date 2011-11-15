import os
from setuptools import setup, find_packages

import aliasdir

rel_file = lambda *args: os.path.join(os.path.dirname(os.path.abspath(__file__)), *args)

def get_readme():
    return open(rel_file('README.mkd')).read()

def get_requirements():
    data = open(rel_file('pipfile')).read()
    lines = map(lambda s: s.strip(), data.splitlines())
    return filter(None, lines)

setup_options = dict(
    name              = "aliasdir",
    version           = aliasdir.VERSION,
    author            = "Kyle Gibson",
    author_email      = "kyle.gibson@frozenonline.com",
    description       = "Easy way to save your directories",
    license           = "MIT",
    url               = "http://github.com/kylegibson/python-aliasdir",
    packages          = find_packages(),
    long_description  = get_readme(),
    install_requires  = get_requirements(),
    entry_points      = {'console_scripts': ['aliasdir = aliasdir.cli:main']},
    classifiers       = [
		"Environment :: Console",
		"Operating System :: Unix",
		"Programming Language :: Python",
		"Programming Language :: Python :: 2",
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)

setup(*setup_options)
