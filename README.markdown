CMake Multi-Tool
==================
<https://github.com/rpavlik/cmake-multitool>

Rylie Pavlik

## Project Status

This worked to some degree when I last used it.
However, I have moved on, no longer use this, and have no capacity to meaningfully maintain it.

cmakelang/cmake-format is a better option.

**Unmaintained**

Introduction
------------

This is both a group of Python modules for working with CMake files, and
a number of utilities built on those modules for maintaining a tidy CMake
build system.

CMake Bulk Decrufter
--------------------

The `cmake-bulk-decrufter.py` tool is an automated CMake code cleaner and
re-formatter. Call it with the name of a single CMake build file, or a
directory to recursively find all `CMakeLists.txt` and `*.cmake` files.
Pass `-m meld` (or other merge tool instead of meld - see `mergetool.py`)
to open a merge tool for each cleaned file so you can selectively apply
the cleanup suggestions that it makes.

License
-------

> Copyright Iowa State University 2010
>
> Distributed under the Boost Software License, Version 1.0.
>
> (See accompanying file `LICENSE_1_0.txt` or copy at
> <http://www.boost.org/LICENSE_1_0.txt>)

