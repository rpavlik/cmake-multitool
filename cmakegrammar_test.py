#!/usr/bin/env python
"""
Tests for parsing CMake source files

Original Author:
2010 Ryan Pavlik <rpavlik@iastate.edu> <abiryan@ryand.net>
http://academic.cleardefinition.com
Iowa State University HCI Graduate Program/VRAC
"""

import unittest
import re

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
			self.assertTrue(re.match(cmakegrammar._reFuncName + "$", line))

	def testRejectInvalidFunctionNames(self):
		"""test the function name regex with just invalid function names"""
		data = (	"func(",
				"FuNc{",
				"FUNC-",
				"the_func!",
				"the_1_FUNC\""	)
		for line in data:
			self.subtest = line
			self.assertFalse(re.match(cmakegrammar._reFuncName + "$", line))

	def testExtractFunctionNames(self):
		"""extracting valid function names using regex"""
		data = (	("func(", "func"),
					(" FuNc ", "FuNc"),
					("\tFUNC\n", "FUNC")	)
		for line, expected in data:
			self.subtest = line
			self.assertTrue(re.match(cmakegrammar._reFuncName, line))

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
			func, args, comment, hasFullLine = cmakegrammar.parse_line(line)

			self.assertTrue(hasFullLine)

			self.assertEqual((func, args, comment), expected)

	def testParseLineComment(self):
		"""parse_line on a line with a comment only"""
		for commentstring in self.commentsOnly:
			self.subtest = commentstring
			func, args, comment, hasFullLine = cmakegrammar.parse_line(commentstring)

			self.assertTrue(hasFullLine)

			self.assertEqual((func, args, comment), ("", None, commentstring))

	def testParseLineMixed(self):
		"""parse_line on a line with both a command and a comment"""
		for (line, expected) in self.mixed:
			self.subtest = line
			func, args, comment, hasFullLine = cmakegrammar.parse_line(line)

			self.assertTrue(hasFullLine)

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
							  cmakegrammar.parse_line(line))


### Requirement:
### A given source file/string has only valid one parse
#class KnownValues(unittest.TestCase):
#	def setUp(self):
#		import glob
#		cmakes = glob.glob('./testdata/KnownValues/*.cmake')
#		cmakes.sort()
#		parses = glob.glob('./testdata/KnownValues/*.parse')
#		parses.sort()
#
#		assert len(parses) == len(cmakes)
#
#		self.strings = []
#		self.files = []
#		self.uppers = []
#		self.lowers = []
#
#		for cmakefn, parsefn in zip(cmakes, parses):
#			cmakef = open(cmakefn, 'r')
#			cmakestr = cmakef.read()
#			cmakef.close()
#
#			parsef = open(parsefn, 'r')
#			parsestr = parsef.read()
#			parsef.close()
#
#			parsedata = eval(parsestr)
#			parseupper = eval("None".join([x.upper() for x in parsestr.split("None")]))
#			parselower = eval("None".join([x.lower() for x in parsestr.split("None")]))
#
#			self.strings.append( (cmakestr, parsedata) )
#			self.files.append( (cmakefn, parsedata) )
#			self.uppers.append( (cmakestr.upper(), parseupper) )
#			self.lowers.append( (cmakestr.lower(), parselower) )
#
#	subtest = ""
#	def _exc_info(self):
#		print "Subtest info:"
#		print self.subtest
#		return unittest.TestCase._exc_info(self)
#
#	def testFullParseKnownString(self):
#		"""passing in a known-good string to the full parser"""
#		for instring, expected in self.strings:
#			self.subtest = instring
#			out = cmakeparser.parse_string(instring)
#			self.assertEqual(out.parsetree, expected)
#
#	def testFullParseKnownFile(self):
#		"""passing in a known-good input filename to the full parser"""
#		for cmakefn, expected in self.files:
#			self.subtest = cmakefn
#			out = cmakeparser.parse_file(cmakefn)
#			self.assertEqual(out.parsetree, expected)
#
#	def testFullParseKnownUppercaseString(self):
#		"""passing in a known-good uppercased string to the full parser"""
#		for instring, expected in self.uppers:
#			self.subtest = instring
#			out = cmakeparser.parse_string(instring)
#			self.assertEqual(out.parsetree, expected)
#
#	def testFullParseKnownLowercaseString(self):
#		"""passing in a known-good lowercased string to the full parser"""
#		for instring, expected in self.lowers:
#			self.subtest = instring
#			out = cmakeparser.parse_string(instring)
#			self.assertEqual(out.parsetree, expected)

	## TODO
	#def testToKnownParsesWhitespace(self):
	#	pass

## Requirement:
## Parsing invalid source trees should fail
# TODO

if __name__=="__main__":
	## Run tests if executed directly
	try:
		import nose
		nose.main()
	except (ImportError):
		unittest.main()
