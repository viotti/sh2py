# sh2py

sh2py is a shell to Python command line mapper. In other words, it is the
easiest way to expose Python functions to the shell. Main features:

* Very small code size. A single Python module. About a hundred lines of code.
* The public API consists of a Python class, `CommandLineMapper`; plus two
  methods: `add` and `run`.
* No external dependencies.
* Support for Python 2 and 3.

## Installation

    pip install sh2py

## Basic Use

Expose a single Python function. Consider the snippet below.

```python
from sh2py import CommandLineMapper

def myfunc(arg1, arg2, arg3='val'):
    print(arg1)
    print(arg2)
    print(arg3)

if __name__ == '__main__':
    cli = CommandLineMapper()

    cli.add(myfunc)

    cli.run()
```

The last three instructions demonstrate the basic operation of the API.

1. Instantiate the `CommandLineMapper`.

2. Register the function you want to expose, using the `CommandLineMapper.add`
method.

3. Call `CommandLineMapper.run`. It will process the command line,
``sys.argv``, and invoke the matching function.

Suppose the snippet above is saved as `myscript.py`.

    $ python myscript.py val1 val2 arg3=val3
    val1
    val2
    val3

The output reveals that the shell command above actually called
`myfunc('val1', 'val2', arg3='val3')`. A couple of notes.

1. Only one function was exposed via `CommandLineMapper.add`, so its name could
be omitted from the command line. If exposing more than one function, it is
recommended to pass its name as the first program argument, otherwise the first
exposed function will be called. See next section.

2. There is no type validation/coercion. The **run** method will only pass
strings on actual function calls.

## Multiple Commands

If your script is large, you can organize it as a suite of sub-commands. Create
one function for each command you expect to handle and register all of them
with `CommandLineMapper.add`. Consider the code below.

```python
from sh2py import CommandLineMapper

def subcommand1(*args1, **kwargs1):
    pass

def subcommand2(*args2, **kwargs2):
    pass

if __name__ == '__main__':
    cli = CommandLineMapper()

    cli.add(subcommand1)
    cli.add(subcommand2)

    cli.run()
```

You can then specify which function to run via command line. For example, to
invoke `subcommand2` with arguments `val1` and `val2`, type the following.

    python mysuite.py subcommand2 val1 val2

Notice that the `subcommand2` entry itself is extracted from the argument
line. The remainder of the line is processed as usual. In this case, `args2`
is `['val1', 'val2']`.

## Complete example

Here is a complete example.

```python
from sys import exit, stderr
from time import sleep
from random import sample

from sh2py import HALT, CommandLineMapper

def hello(case='', shuffle='no', pace='0'):
    '''
    Emits a "Hello, world!" greeting message on standard error.

    Usage:

        python hello.py help
        python hello.py [case=upper/lower] [shuffle=yes/no] [pace=0]

    Arguments:

        help,              print this usage help and exit;
        case=upper/lower,  convert the message to uppercase, or lowercase;
        shuffle=yes/no,    shuffle the letters of the message;
        pace=0,            pace at which the letters are shown, in miliseconds.

    By default, there is no case conversion and no shuffling. Also, the pace is
    zero, so the entire message is shown immediately on standard error.
    '''

    if case in ['', 'upper', 'lower'] and shuffle in ['yes', 'no']:
        if pace.isdigit():
            greet = ['Hello', 'world']
            delay = int(pace)

            if shuffle == 'yes':
                greet[0] = ''.join(sample(greet[0], len(greet[0])))
                greet[1] = ''.join(sample(greet[1], len(greet[1])))

            greet = '{}, {}!'.format(*greet)

            if case == 'upper':
                greet = greet.upper()

            elif case == 'lower':
                greet = greet.lower()

            if delay == 0:
                print(greet, file=stderr)

            else:
                for x in greet:
                    stderr.write(x)

                    stderr.flush()

                    sleep(delay / 1000.0)

                print(file=stderr)

        else:
            return HALT

    else:
        return HALT

if __name__ == '__main__':
    cli = CommandLineMapper()

    cli.add(hello)

    if cli.run() is HALT:
        print(hello.__doc__, file=stderr)

        exit(1)
```

Observe that the `hello` function does not have a `help` argument, but the
**docstring** says different. The `help` argument is automatically recognized
and, when used, will print the **docstring** of the default, `hello`, function.
A default help text will be printed if a function does not supply a
**docstring**.

The call to `CommandLineMapper.run` will return `HALT` if a command is
invoked with an invalid syntax. Your functions can also use it to signal error
conditions. This allows the program to exit with a non-zero status, or trigger
some error handling function.

## Q&A

Q. I want POSIX arguments.

A. Wrong tool. There are plenty of Python command line parsing utilities
supporting POSIX. Try one of them.

* Argparse/Optparse/Getopt. Built into Python. Complex.
* [Compago](https://github.com/jmohr/compago). Very nice, but
  unmaintained. Also, does not run on Python 3.
* [Docopt](http://docopt.org/).
* [Clint](https://github.com/kennethreitz/clint).
* [Click](http://click.pocoo.org/3/).

Q. I need type coercion.

A. Implement it yourself, or use some third party library.

Q. I can use Python itself as a command line interpreter. Why all of this?

A. Yes you can. In this case all of this becomes irrelevant. I prefer not to,
that is one of the reasons I wrote this tool. Another is that everything else
is too complex. YMMV.

Q. Why not use `sys.argv` directly.

A. Good question. I do this a lot of times. Actually, if your script is small
enough and requires zero, one, or maybe two positional parameters, there is no
need for command line processing tools. Write a couple of conditionals and
print a simple help message in case of errors.

