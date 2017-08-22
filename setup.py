#!/usr/bin/env python

from os import path, remove
from sys import version_info
from shutil import move
from codecs import open
from distutils.core import setup
from distutils.command.build import build as Build

# Project URL.
_URL = 'https://github.com/viotti/sh2py'

# Release version.
_VERSION = '0.1.0'

# Readme file.
_README = path.join(path.abspath(path.dirname(__file__)), 'README.md')

# On Python 3, build and install only "sh2py.py". On Python 2, build and
# install "sh2py_legacy.py" as "sh2py.py". Sadly, I did not found an easy way
# to accomplish this.
#
# The workaround is the following wrapper. It will intercept the "build"
# command and will either remove the unwanted "sh2py_legacy.py" from the "lib"
# directory, or rename it to "sh2py.py", according to the version of the Python
# interpreter in execution.
#
class _BuildWrapper(Build):
    def run(self):
        if version_info[0] >= 3:
            py2 = path.join(self.build_lib, 'sh2py_legacy.py')

            Build.run(self)

            remove(py2)

        else:
            old = path.join(self.build_lib, 'sh2py_legacy.py')
            new = path.join(self.build_lib, 'sh2py.py')

            Build.run(self)

            move(old, new)

with open(_README, encoding='UTF-8') as f:
    setup(
        name='sh2py',
        version=_VERSION,
        description='Python command line mapper',
        long_description=f.read(),
        license='MIT',
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Topic :: Software Development',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.5',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.0',
            'Programming Language :: Python :: 3.1',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7'
        ],
        author='Rafael Viotti',
        author_email='rviotti@gmail.com',
        url=_URL,
        download_url='%s/tarball/%s' % (_URL, _VERSION),
        py_modules=['sh2py', 'sh2py_legacy'],
        cmdclass={'build': _BuildWrapper}
    )
