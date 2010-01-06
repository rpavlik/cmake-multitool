#!/usr/bin/env python
"""
Module for parsing a CMake source file

Original Author:
2010 Ryan Pavlik <rpavlik@iastate.edu> <abiryan@ryand.net>
http://academic.cleardefinition.com
Iowa State University HCI Graduate Program/VRAC
"""

import re

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
	## A tuple containing all functions that start a block
	blockBeginnings = ('foreach',
					'function',
					'if',
					'elseif',
					'else',
					'macro',
					'while')

	## A compiled regex that matches exactly the functions that start a block
	reBlockBeginnings = re.compile(r"^(" + "|".join(blockBeginnings) + r")$",
		re.IGNORECASE)

	## A dictionary where blockEndings[blockBeginFunc]=(blockEndFunc1,...),
	## all datatypes are strings.  Size is one more than blockBeginnings
	## because we match the empty string opening function (dummy for start
	## of file) with a dummy EOF string as an end tag
	blockEndings = {'' : ('_CMAKE_PARSER_EOF_FLAG_',),

					'foreach'	: ('endforeach',),

					'function'	: ('endfunction',),

					'if'		: ('elseif', 'else', 'endif'),
					'elseif'	: ('elseif', 'else', 'endif'),
					'else'		: ('endif',),

					'macro'	: ('endmacro',),

					'while'	: ('endwhile',)}

	# Catch any "developer failed to add new function to both lists" bugs
	assert len(blockEndings) - 1 == len(blockBeginnings)

	## A big list comprehension that makes a dictionary with pairs (start, end)
	## where start is a start tag string from blockEndings and end is a
	## compiled regex that only exactly matches any corresponding ending
	reBlockEndings = dict([  # Make a dict from list comprehension of pairs
		# the dictionary key is just the start tag
		( beginning,
		# the value is a compiled regex matching any of the end tags
		re.compile(r"^(" + "|".join(ends) + r")$", re.IGNORECASE) )

		# for every key-value pair in the non-compiled dictionary
		for beginning, ends in blockEndings.iteritems() ])

	# sanity check the comprehension above
	assert len(blockEndings) == len(reBlockEndings)

	def __init__(self, parseinput):
		self.input = parseinput
		self.parsetree = []

	def parse(self):
		pass

	def parse_block_children(self, startTag):
		endblock = self.reBlockEndings[startTag]
		for line in self.input:
			func, args, comment = self.parse_line(line)

def parse_string(instr):
	parser = CMakeParser(ParseInput(instr))
	parser.parse()
	return parser
