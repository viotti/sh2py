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

from sys import argv, stderr
from inspect import trace, getmodule
from textwrap import dedent

HALT = object()

class CommandLineMapper(object):
    def __init__(self, usage=None):
        self._funcs = []
        self._usage = usage
        self._default = None

    def add(self, function):
        self._funcs.append(function)

        if len(self._funcs) == 1:
            self._default = function

        return function

    def _parse(self):
        if len(self._funcs) >= 1:
            fun, args, kwargs = None, [], {}

            if len(argv) == 1:
                fun = self._funcs[0]

            elif len(self._funcs) == 1:
                fun = self._funcs[0]

            else:
                gen = (x for x in self._funcs if x.__name__ == argv[1])
                fun = next(gen, None)

            if not fun:
                fun = self._default

            if fun:
                cmd = []

                if len(argv) >= 2:
                    if argv[1] != fun.__name__:
                        cmd = argv[1:]

                    else:
                        cmd = argv[2:]

                for opt in cmd:
                    if u'=' in opt:
                        key, val = opt.split(u'=', 1)

                        kwargs[key] = val

                    else:
                        args.append(opt)

            return fun, args, kwargs

        else:
            raise Exception()

    def run(self):
        fun, args, kwargs = self._parse()

        if fun:
            try:
                return fun(*args, **kwargs)

            except TypeError:
                mod = getmodule(trace()[-1][0])

                if mod and mod.__name__ == __name__:
                    if fun.__doc__:
                        print >> stderr, dedent(fun.__doc__)

                else:
                    raise

        elif self._usage:
            print >> stderr, self._usage

        return HALT
