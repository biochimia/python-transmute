# -*- coding: utf-8 -*-

from setuptools import Command, find_packages, setup
from setuptools.command.egg_info import egg_info

import datetime
import os.path
import subprocess


README = 'README.md'
VERSION_FILE = 'transmute/_version.py'


# We use README.md for GitHub's sake, generate README.rst for PyPI.
#
try:
    # Requires pandoc, the tool, and pypandoc, the python module
    import pypandoc
    long_description = pypandoc.convert(README, 'rst')
except:
    with open(README) as readme:
        long_description = readme.read()
else:
    with open('README.rst', 'w') as rst:
        rst.write(long_description)


# Generate project version number from git tags
#
try: execfile(VERSION_FILE)
except: __version__ = 'unknown'

_git_revision = None
def get_git_revision():
    """Fetch git revision for use as the package version."""

    global _git_revision
    if _git_revision is None:
        wd = os.path.dirname(__file__) or None
        revision = subprocess.check_output(
                [ 'git', 'describe', '--always', '--dirty=-patched' ], cwd=wd)
        _git_revision = revision.rstrip()
    return _git_revision

def update_version_file():
    version_file_content = '\n'.join([
        "# File generated by %s on %s" % (__file__, datetime.date.today()),
        "__version__ = '%s'" % get_git_revision(),
        "" # End of file line-break
    ])
    with open(VERSION_FILE, 'w') as version_file:
        version_file.write(version_file_content)


class UpdateVersion(Command):

    description = "update package version information from version control"
    user_options = []

    def initialize_options(self): pass
    def finalize_options(self): pass

    def run(self):
        git_revision = get_git_revision()
        if git_revision != __version__:
            update_version_file()
            print 'New package version: %s (was: %s)' \
                    % (git_revision, __version__)
            self.distribution.metadata.version = git_revision


class EggInfo(egg_info):
    def finalize_options(self):
        # Must update version before egg_info sets internal egg_version in
        # finalize_options.
        self.run_command('update_version')
        egg_info.finalize_options(self)


# Alright, let's make this setuptools thingie run!
#
project_metadata = {
    'name':         'transmute',
    'version':      __version__,
    'author':       'João Abecasis',
    'author_email': 'joao@comoyo.com',
    'url':          'https://github.com/comoyo/python-transmute',
    'description':  'Automatically update Python Eggs on application startup.',
    'classifiers':  [
                        "Programming Language :: Python",
                        "License :: OSI Approved :: Apache Software License",
                        "Operating System :: OS Independent",
                        "Development Status :: 3 - Alpha",
                        "Intended Audience :: Developers",
                        "Topic :: Software Development :: Libraries :: Python Modules",
                        "Topic :: System :: Installation/Setup",
                        "Topic :: System :: Software Distribution",
                    ],
    'long_description': long_description,
    'packages':     find_packages(exclude=[ 'tests*' ]),
    'cmdclass':     {
                        'egg_info': EggInfo,
                        'update_version': UpdateVersion,
                    },
}
# Go!
setup(**project_metadata)
