#!/usr/bin/env python
"""
Module for modifying a parsed CMake source file

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
import cmakegrammar

grammar = cmakegrammar

class CMakeBlock():
	def __init__(self, block):
		self.data = [CMakeStatement(x) for x in block]

	def __repr__(self):
		return repr([repr(x) for x in self.data])

	def get(self):
		return [x.get() for x in self.data]

	def accept(self, visitor):
		visitor.visit_block(self)
		for x in self.data:
			x.accept(visitor)

class CMakeStatement():
	def __init__(self, statement):
		self.func, self.args, self.comment, children = statement
		if children is not None:
			self.children = CMakeBlock(children)
		else:
			self.children = None

	def __repr__(self):
		return repr( (self.func, self.args, self.comment, repr(self.children) ))

	def get(self):
		if self.children is None:
			return (self.func, self.args, self.comment, None )
		else:
			return (self.func, self.args, self.comment, self.children.get() )
	def accept(self, visitor):
		visitor.visit_statement(self)
		if self.children is not None:
			self.children.accept(visitor)


class CMakeVisitor:

	def visit_block(self, block):
		pass

	def visit_statement(self, statement):
		pass


class VisitorRemoveRedundantConditions(CMakeVisitor):
	funcs = ["else", "endif", "endmacro", "endfunction", "endforeach", "endwhile"]
	_reFuncs = (r"(?ix)" +		# case-insensitive and verbose
						r"(?P<RedundantConditionFuncs>" +
						"|".join(funcs) +
						r")$")
	reFuncs = re.compile(_reFuncs)
	def visit_statement(self, statement):
		if self.reFuncs.match(statement.func):
			statement.args = None



#if __name__ == "__main__":
#	pass
