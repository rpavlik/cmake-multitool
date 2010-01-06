#!/usr/bin/env python
"""
Module for parsing a CMake source file

Original Author:
2010 Ryan Pavlik <rpavlik@iastate.edu> <abiryan@ryand.net>
http://academic.cleardefinition.com
Iowa State University HCI Graduate Program/VRAC
"""

import re

def parse_string(instr):
	parser = CMakeParser(ParseInput(instr))
	parser.parse()
	return parser

class ParseInput():
	def __init__(self, strdata):
		self.input = strdata.splitlines()
		self.lineindex = 0
		self.alldone = False
		self.gotline = False

	def __iter__(self):
		"""Be usable as an iterator."""
		return self

	def next(self):
		"""Return the current line each time we are iterated.
		We don't go to the next line unless we've been accepted."""

		# Will always hit this condition if all works well
		if self.lineindex == len(self.lineindex):
			self.alldone = true
			raise StopIteration

		# If we break, break big
		assert self.lineindex < len(self.lineindex)

		# OK, we can actually return the data now
		self.gotline = true
		return self.input[self.lineindex]

	def line(self):
		"""A more intuitive alias for next() - get the current line"""
		return self.next()

	def accept(self):
		"""Signal that we've processed this line and should go to the next"""

		# We shouldn't accept a line we haven't even seen
		assert self.gotline == true
		self.lineindex = self.lineindex + 1
		self.gotline = False

class CMakeParser():
	# There are all the important regexes at the bottom of the class

	def __init__(self, parseinput):
		self.input = parseinput
		self.parsetree = []

	def parse(self):
		pass

	def parse_block_children(self, startTag):
		endblock = self.reBlockEndings[startTag]
		for line in self.input:
			func, args, comment, complete = self.parse_line(line)

	def parse_line(self, line):
		m = self.reFullLine.match(line)
		valid, func, args, comment = m.group("fullLine",
											"funcName",
											"args", # todo change to argsCareful
											"comment")
		return (func, args, comment, (valid is not None))

	####
	## Strings of sub-regexes to compile later - all are re.VERBOSE

	## all the functions that permit parens in their args
	_parenArgFuncs = (r"(?ix)" # case-insensitive and verbose
		+ "(?P<parenArgFunc>"
		+ "|".join(
			"""
			if
			else
			elseif
			endif

			while
			endwhile

			math
			""".split())
		+ r")")

	## A possible function name
	_funcName = r"(?x)(?P<funcName> [\w\d]+)"

	## Extremely general "non-empty arguments," no leading or trailing whitespc
	_args = r"(?x)(?P<args> (?\S(?\S|\s\S)* )?"

	## Standard command args: no parens
	_argsStd = r"(?x)(?P<argsStd> (?[\S-(?\S|\s\S)* )?"

	## A comment: everything after # as long as it's not preceded by a \
	_comment = r"""(?x)(?P<comment> (?<!\\)\#.*$"""

	## The start of a command, up until the arguments
	_commandStart = r"\s*" + _funcName + r"\s*\("

	## The end of a command
	_commandEnd = r"\)"
	##
	####

	## Regex matching all the functions that permit parens in their args
	reParenArgFuncs = re.compile("^" + _parenArgFuncs + "$",
		re.IGNORECASE | re.VERBOSE)

	## Regex matching the beginning of a command



#	reCommandStart = re.compile(r"""^\s*
#									(?			# start optional command group
#										# function name
#									\s*
#									\(					# open paren
#									\s*
#
#									)?			# end optional command group
#									$
#									""", re.VERBOSE)

	## A tuple containing all functions that start a block
	_blockBeginnings ="""	foreach
							function
							if
							elseif
							else
							macro
							while	""".split()

	## A compiled regex that matches exactly the functions that start a block
	reBlockBeginnings = re.compile(r"^(" + "|".join(_blockBeginnings) + r")$",
		re.IGNORECASE)

	## A dictionary where blockEndings[blockBeginFunc]=(blockEndFunc1,...),
	## all datatypes are strings.  Size is one more than blockBeginnings
	## because we match the empty string opening function (dummy for start
	## of file) with a dummy EOF string as an end tag
	_blockEndings = {'' : ('_CMAKE_PARSER_EOF_FLAG_',),

					'foreach'	: ('endforeach',),

					'function'	: ('endfunction',),

					'if'		: ('elseif', 'else', 'endif'),
					'elseif'	: ('elseif', 'else', 'endif'),
					'else'		: ('endif',),

					'macro'	: ('endmacro',),

					'while'	: ('endwhile',)}

	# Catch any "developer failed to add new function to both lists" bugs
	assert len(_blockEndings) - 1 == len(_blockBeginnings)

	## A big list comprehension that makes a dictionary with pairs (start, end)
	## where start is a start tag string from blockEndings and end is a
	## compiled regex that only exactly matches any corresponding ending
	reBlockEndings = dict([  # Make a dict from list comprehension of pairs
		# the dictionary key is just the start tag
		( beginning,
		# the value is a compiled regex matching any of the end tags
		re.compile(r"^(" + "|".join(ends) + r")$", re.IGNORECASE) )

		# for every key-value pair in the non-compiled dictionary
		for beginning, ends in _blockEndings.iteritems() ])

	# sanity check the comprehension above
	assert len(_blockEndings) == len(reBlockEndings)
