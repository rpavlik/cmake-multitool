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
		reKeys = 0
		regexStrings = filter(lambda (x, y): re.match("(_re)", x),
				cmakeparser.CMakeParser.__dict__.iteritems())
		for (varName, reStr) in regexStrings:
			re.compile(reStr)


## Requirement:
## Be able to parse a valid cmake command input line.
class ParseCompleteLine(unittest.TestCase):
	data = (	("",				("", "", "")),
				("func()",			("func", "", "")),
				("func(arg)",		("func", "arg", "")),
				("func(arg arg)",	("func", "arg arg", "")),
				("func() # cmnt",	("func", "", "# cmnt"))	)
	def testParseLine(self):
		parser = cmakeparser.CMakeParser(cmakeparser.ParseInput(""))
		for (line, expected) in self.data:
			func, args, comment, hasFullLine = parser.parse_line(line)
			self.assertTrue(hasFullLine)
			self.assertEqual((func, args, comment), expected)

## Requirement:
## Be able to parse a comment line
class ParseCommentLine(unittest.TestCase):
	data = (	"#",
				"# some comment going on here",
				"## a bit confusing",
				"#a#a#a#"	)

## Requirement:
## Notify on an incomplete cmake input line
class ParsePartialLine(unittest.TestCase):
	data = (	("",				("", "", "")),
				("func()",			("func", "", "")),
				("func(arg)",		("func", "arg", "")),
				("func(arg arg)",	("func", "arg arg", "")),
				("func() # cmnt",	("func", "", "# cmnt"))	)


## Requirement:
## A given source file has only valid one parse
class KnownValues(unittest.TestCase):
	def setUp(self):
		import glob
		cmakes = glob.glob('./testdata/KnownValues/*.cmake')
		cmakes.sort()
		parses = glob.glob('./testdata/KnownValues/*.parse')
		parses.sort()
		self.cases = []
		for cmakefn, parsefn in zip(cmakes, parses):
			cmakef = open(cmakefn, 'r')
			cmakedata = cmakef.read()
			cmakef.close()

			parsef = open(parsefn, 'r')
			parsedata = eval(parsef.read())
			parsef.close()
			self.cases.append( (cmakefn, cmakedata, parsedata) )

	def testToKnownParses(self):
		for cmakefn, instring, expected in self.cases:
			out = cmakeparser.parse_string(instring)
			self.assertEqual(str(out.parsetree), str(expected))
			self.assertEqual(out.parsetree, expected)

		for cmakefn, instring, expected in self.cases:
			out = cmakeparser.parse_file(cmakefn)
			self.assertEqual(str(out.parsetree), str(expected))
			self.assertEqual(out.parsetree, expected)

	def testToKnownParsesWhitespace(self):
		pass

## Requirement:
## Parsing invalid source trees should fail
if __name__=="__main__":
	## Run tests if executed directly
	regexStrings = filter(lambda (x, y): re.match("(_re)", x),
				cmakeparser.CMakeParser.__dict__.iteritems())
	for (varName, reStr) in regexStrings:
		print str(reStr)
	pass
