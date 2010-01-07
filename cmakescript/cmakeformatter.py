#!/usr/bin/env python
"""
Module for formatting a parsed CMake source file

Original Author:
2010 Ryan Pavlik <rpavlik@iastate.edu> <abiryan@ryand.net>
http://academic.cleardefinition.com
Iowa State University HCI Graduate Program/VRAC
"""

###
# standard packages
import re

###
# third-party packages
# - none

###
# internal packages
# - none



class CMakeFormatter():

	def __init__(self, parsetree):
		self.parsetree = parsetree

	def output_as_cmake(self):
		return "\n".join(self.output_block(self.parsetree, 0))

	def output_block(self, block, level):
		lines = []
		if block is None:
			return lines
		for statement in block:
			lines.extend(self.output_statement(statement, level))
		return lines

	def output_statement(self, statement, level):

		func, args, comment, children = statement

		if args is None:
			args = ""

		if func == "" and comment is None:
			thisline = ""
		else:
			thisline = "\t" * level

		if func != "":
			thisline = thisline + func.lower() + "(" + args + ")"
			if comment is not None:
				thisline = thisline + "\t"

		if comment is not None:
			thisline = thisline + comment

		output = [thisline]
		# Recurse into children
		output.extend(self.output_block(children, level + 1))
		return output


#if __name__ == "__main__":
#	pass
