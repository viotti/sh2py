# -*- coding: utf-8; -*-
#
# The MIT License (MIT)
#
# Copyright (c) 2015 Rafael Viotti
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

'''Example tool two, a fake suite.'''

from sys import exit, stderr

from sh2py import HALT, CommandLineMapper

_USAGE = '''Usage:

    python t2_fakesuite.py help
    python t2_fakesuite.py command1
    python t2_fakesuite.py command2 argument
    python t2_fakesuite.py command3 argument [option=1]
'''

def command1():
    print('First command executed.', file=stderr)

def command2(argument):
    print('Positional argument: "{}".'.format(argument), file=stderr)

    print('Second command executed.', file=stderr)

def command3(argument, option=1):
    print('Positional argument: "{}".'.format(argument), file=stderr)
    print('Command line option: "{}".'.format(option), file=stderr)

    print('Third command executed.', file=stderr)

if __name__ == '__main__':
    cli = CommandLineMapper(usage=_USAGE)

    cli.add(command1)
    cli.add(command2)
    cli.add(command3)

    if cli.run() is HALT:
        exit(1)
