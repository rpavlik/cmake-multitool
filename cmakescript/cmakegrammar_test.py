#!/usr/bin/env python
"""
Tests for the cmakescript.cmakegrammar module

Original Author:
2010 Ryan Pavlik <rpavlik@iastate.edu> <abiryan@ryand.net>
http://academic.cleardefinition.com
Iowa State University HCI Graduate Program/VRAC
"""

###
# standard packages
import unittest
import re

###
# third-party packages
# - none

###
# internal packages
import cmakegrammar




## Requirement:
## All regexes must be able to be compiled
class AllRegexesCompilable(unittest.TestCase):
	def testCompileRegexes(self):
		"""Compiling regex string attributes of the grammar"""
		reKeys = 0
		regexStrings = filter(lambda (x, y): re.match("(_re)", x),
				cmakegrammar.__dict__.iteritems())
		for (varName, reStr) in regexStrings:
			re.compile(reStr)


## Requirement:
## Accept only possible command names
class AcceptRejectReFuncNames(unittest.TestCase):

	subtest = ""
	def _exc_info(self):
		print "Subtest info:"
		print self.subtest
		return unittest.TestCase._exc_info(self)

	def testAcceptValidFunctionNames(self):
		"""test the function name regex with just valid function names"""
		data = (	"func",
				"FuNc",
				"FUNC",
				"the_func",
				"the_1_FUNC"	)
		for line in data:
			self.subtest = line
			self.assertTrue(re.search(cmakegrammar._reFuncName + "$", line))

	def testRejectInvalidFunctionNames(self):
		"""test the function name regex with just invalid function names"""
		data = (	"func(",
					"FuNc{",
					"FUNC-",
					"the_func!",
					"the_1_FUNC\"",
					"#comment"	)
		for line in data:
			self.subtest = line
			self.assertFalse(re.search(cmakegrammar._reFuncName + "$", line))

	def testExtractFunctionNames(self):
		"""extracting valid function names using regex"""
		data = (	("func(", "func"),
					(" FuNc ", "FuNc"),
					("\tFUNC\n", "FUNC")	)
		for line, expected in data:
			self.subtest = line
			self.assertTrue(re.search(cmakegrammar._reFuncName, line))

## Requirement:
## Accept only valid comments
class AcceptRejectReComment(unittest.TestCase):

	subtest = ""
	def _exc_info(self):
		print "Subtest info:"
		print self.subtest
		return unittest.TestCase._exc_info(self)

	def testAcceptValidComments(self):
		"""test the function name regex with just valid comments"""
		data = (	"#",
					"#Comment",
					"# Comment",
					"## Comment",
					"###"	)
		for line in data:
			self.subtest = line
			self.assertTrue(re.search("^" + cmakegrammar._reComment + "$", line))

	def testRejectInvalidComments(self):
		"""test the function name regex with just invalid comments"""
		data = (	"",
					"func(",
					"\#notacomment"	)
		for line in data:
			self.subtest = line
			self.assertFalse(re.search("^" + cmakegrammar._reComment + "$", line))

	def testStripCommentWS(self):
		"""ensure leading and trailing whitespace is stripped from comments"""
		data = (	" # ",
					" # not exact comment"	)
		for line in data:
			self.subtest = line
			self.assertFalse(re.search("^" + cmakegrammar._reComment + "$", line))
			self.assertEqual(re.search(cmakegrammar._reComment, line)["Comment"], line.trim())

	def testExtractFunctionNames(self):
		"""extracting valid function names using regex"""
		data = (	("func(", "func"),
					(" FuNc ", "FuNc"),
					("\tFUNC\n", "FUNC")	)
		for line, expected in data:
			self.subtest = line
			self.assertEqual(re.search(cmakegrammar._reFuncName, line), expected)

## Requirement:
## Be able to parse a valid cmake command input line.
class ParseCompleteLine(unittest.TestCase):
	commandsOnly = (	("",				("", None, None)),
					("func()",			("func", None, None)),
					("func(arg)",		("func", "arg", None)),
					("func(arg arg)",	("func", "arg arg", None)),
					("func( arg arg )",	("func", "arg arg", None)),
					("func( arg  ar )",	("func", "arg  ar", None)),
					(r"func(\#notcmnt)",("func", r"\#notcmnt", None))	)

	commentsOnly = (	"#",
				"# comment",
				"#comment",
				"## comment",
				"##comment",
				"#a#a#a#"	)

	mixed = (	("func() # cmnt",	("func", None, "# cmnt")),
				(r"func(\#notcmnt) #iscmnt",("func", r"\#notcmnt", "#iscmnt"))	)

	subtest = ""
	def _exc_info(self):
		print "Subtest info:"
		print self.subtest
		return unittest.TestCase._exc_info(self)

	def testParseLineCommand(self):
		"""parse_line on a line with a command only"""
		for (line, expected) in self.commandsOnly:
			self.subtest = line
			func, args, comment = cmakegrammar.parse_line(line)


			self.assertEqual((func, args, comment), expected)

	def testParseLineComment(self):
		"""parse_line on a line with a comment only"""
		for commentstring in self.commentsOnly:
			self.subtest = commentstring
			func, args, comment = cmakegrammar.parse_line(commentstring)

			self.assertEqual((func, args, comment), ("", None, commentstring))

	def testParseLineMixed(self):
		"""parse_line on a line with both a command and a comment"""
		for (line, expected) in self.mixed:
			self.subtest = line
			func, args, comment = cmakegrammar.parse_line(line)

			self.assertEqual((func, args, comment), expected)

## Requirement:
## Notify on an incomplete cmake input line
class ParsePartialLine(unittest.TestCase):
	data = (	"func(",
				"func(arg",
				"func(arg ",
				"func ( arg ",
				"func(arg arg"	)


	subtest = ""
	def _exc_info(self):
		print "Subtest info:"
		print self.subtest
		return unittest.TestCase._exc_info(self)

	def testParseIncompleteStatement(self):
		"""parse_line on an incomplete line with a command only"""
		for line in self.data:
			self.subtest = line
			self.assertRaises(cmakegrammar.IncompleteStatementError,
							cmakegrammar.parse_line, line)


if __name__=="__main__":
	## Run tests if executed directly
	try:
		import nose
		nose.main()
	except (ImportError):
		unittest.main()
