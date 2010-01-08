#!/usr/bin/env python
"""
Tests for the cmakescripts.cmakeparser module

Original Author:
2010 Ryan Pavlik <rpavlik@iastate.edu> <abiryan@ryand.net>
http://academic.cleardefinition.com
Iowa State University HCI Graduate Program/VRAC
"""

###
# standard packages
import unittest
import re
import os

###
# third-party packages
# - none

###
# internal packages
import cmakeparser

## Requirement:
## A given source file/string has only valid one parse
class KnownValues(unittest.TestCase):
	def setUp(self):
		import glob
		cmakes = glob.glob(os.path.split(__file__)[0] + '/testdata/KnownValues/*.cmake')
		cmakes.sort()
		parses = glob.glob(os.path.split(__file__)[0] + '/testdata/KnownValues/*.parse')
		parses.sort()

		assert len(parses) == len(cmakes)
		assert len(parses) == 9

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
			parseupper = eval("None".join([x.upper() for x in parsestr.split("None")]))
			parselower = eval("None".join([x.lower() for x in parsestr.split("None")]))

			self.strings.append( (cmakestr, parsedata) )
			self.files.append( (cmakefn, parsedata) )
			self.uppers.append( (cmakestr.upper(), parseupper) )
			self.lowers.append( (cmakestr.lower(), parselower) )


	if "nose" in dir():
		subtest = ""
		def _exc_info(self):
			print "Subtest info:"
			print self.subtest
			return super(KnownParses, self)._exc_info()

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
		start = nose.main
	except (ImportError):
		start = unittest.main

	start()
