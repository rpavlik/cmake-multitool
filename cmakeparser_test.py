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

import cmakeparser

## Requirement:
## All regexes must be able to be compiled
class AllRegexesCompilable(unittest.TestCase):
	def testCompileRegexes(self):
		"""Compiling regex string attributes of the parser"""
		reKeys = 0
		regexStrings = filter(lambda (x, y): re.match("(_re)", x),
				cmakeparser.CMakeParser.__dict__.iteritems())
		for (varName, reStr) in regexStrings:
			re.compile(reStr)


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
		parser = cmakeparser.CMakeParser(cmakeparser.ParseInput(""))
		for (line, expected) in self.commandsOnly:
			self.subtest = line
			func, args, comment, hasFullLine = parser.parse_line(line)

			self.assertTrue(hasFullLine)

			self.assertEqual((func, args, comment), expected)

	def testParseLineComment(self):
		"""parse_line on a line with a comment only"""
		parser = cmakeparser.CMakeParser( cmakeparser.ParseInput("") )
		for commentstring in self.commentsOnly:
			self.subtest = commentstring
			func, args, comment, hasFullLine = parser.parse_line(commentstring)

			self.assertTrue(hasFullLine)

			self.assertEqual((func, args, comment), ("", None, commentstring))

	def testParseLineMixed(self):
		"""parse_line on a line with both a command and a comment"""
		parser = cmakeparser.CMakeParser( cmakeparser.ParseInput("") )
		for (line, expected) in self.mixed:
			self.subtest = line
			func, args, comment, hasFullLine = parser.parse_line(line)

			self.assertTrue(hasFullLine)

			self.assertEqual((func, args, comment), expected)

## Requirement:
## Notify on an incomplete cmake input line
class ParsePartialLine(unittest.TestCase):
	data = (	("",				("", None, None)),
				("func()",			("func", None, None)),
				("func(arg)",		("func", "arg", None)),
				("func(arg arg)",	("func", "arg arg", None)),
				("func() # cmnt",	("func", None, "# cmnt")),
				)


## Requirement:
## A given source file/string has only valid one parse
class KnownValues(unittest.TestCase):
	def setUp(self):
		import glob
		cmakes = glob.glob('./testdata/KnownValues/*.cmake')
		cmakes.sort()
		parses = glob.glob('./testdata/KnownValues/*.parse')
		parses.sort()

		self.strings = []
		self.files = []
		self.uppers = []
		self.lowers = []

		for cmakefn, parsefn in zip(cmakes, parses):
			cmakef = open(cmakefn, 'r')
			cmakestr = cmakef.read()
			cmakef.close()

			parsef = open(parsefn, 'r')
			parsestr = parsef.read()
			parsef.close()

			parsedata = eval(parsestr)
			parseupper = eval(parsestr.upper())
			parselower = eval(parsestr.lower())

			self.strings.append( (cmakestr, parsedata) )
			self.files.append( (cmakefn, parsedata) )
			self.uppers.append( (cmakestr.upper(), parseupper) )
			self.lowers.append( (cmakestr.lower(), parselower) )

	subtest = ""
	def _exc_info(self):
		print "Subtest info:"
		print self.subtest
		return unittest.TestCase._exc_info(self)

	def testFullParseKnownString(self):
		"""passing in a known-good string to the full parser"""
		for instring, expected in self.strings:
			self.subtest = instring
			out = cmakeparser.parse_string(instring)
			self.assertEqual(out.parsetree, expected)

	def testFullParseKnownFile(self):
		"""passing in a known-good input filename to the full parser"""
		for cmakefn, expected in self.files:
			self.subtest = cmakefn
			out = cmakeparser.parse_file(cmakefn)
			self.assertEqual(out.parsetree, expected)

	def testFullParseKnownUppercaseString(self):
		"""passing in a known-good uppercased string to the full parser"""
		for instring, expected in self.uppers:
			self.subtest = instring
			out = cmakeparser.parse_string(instring)
			self.assertEqual(out.parsetree, expected)

	def testFullParseKnownLowercaseString(self):
		"""passing in a known-good lowercased string to the full parser"""
		for instring, expected in self.lowers:
			self.subtest = instring
			out = cmakeparser.parse_string(instring)
			self.assertEqual(out.parsetree, expected)

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
