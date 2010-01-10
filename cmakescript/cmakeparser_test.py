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
import glob

###
# third-party packages
# - none

###
# internal packages
import cmakeparser

# format for each:
# key is the filename - extension
# value is whatever the variable name suggests
inputfiles = dict()
inputstrings = dict()
inputuppers = dict()
inputlowers = dict()

parsedfiles = dict()
parsedstrings = dict()

parseduppers = dict()
parsedlowers = dict()

def setUp():
	cmakes = glob.glob(os.path.split(__file__)[0] + '/testdata/KnownValues/*.cmake')
	cmakes.sort()
	parses = glob.glob(os.path.split(__file__)[0] + '/testdata/KnownValues/*.parse')
	parses.sort()

	assert len(parses) == len(cmakes)
	assert len(parses) == 10



	for cmakefn, parsefn in zip(cmakes, parses):
		cbase = os.path.splitext(cmakefn)[0]
		pbase = os.path.splitext(parsefn)[0]
		assert cbase == pbase

		cmakef = open(cmakefn, 'r')
		cmakestr = cmakef.read()
		cmakef.close()

		parsef = open(parsefn, 'r')
		parsestr = parsef.read()
		parsef.close()

		parsedata = eval(parsestr)

		# case-change our known parses, but don't touch "None" because it's
		#
		applyExceptToNone = lambda userfunc, string, untouchable:	untouchable.join(
			[	userfunc(chunk)
				for chunk
				in string.split(untouchable)	]	)

		safeUpper = lambda input: applyExceptToNone(lambda x: x.upper(), input, "None")
		safeLower = lambda input: applyExceptToNone(lambda x: x.lower(), input, "None")

		parseupper = safeUpper(parsestr)
		parselower = safeLower(parsestr)

		inputfiles[cbase] = cmakefn
		inputstrings[cbase] = cmakestr
		inputuppers[cbase] = safeUpper(cmakestr)
		inputlowers[cbase] = safeLower(cmakestr)

		parsedfiles[cbase] = parsedata
		parsedstrings[cbase] = parsedata

		parseduppers[cbase] = parseupper
		parsedlowers[cbase] = parselower

	dataKeys = inputfiles.keys()


## Requirement:
## A given source file/string has only valid one parse
class KnownValues(unittest.TestCase):

	subtest = ""

	if "nose" in dir():
		def _exc_info(self):
			print "Subtest info:"
			print self.subtest
			return super(KnownParses, self)._exc_info()

	def testFullParseKnownString(self):
		"""passing in a known-good string to the full parser"""
		for key in parsedstrings.keys():
			instring = inputstrings[key]
			expected = parsedstrings[key]
			self.subtest = instring
			out = cmakeparser.parse_string(instring)
			self.assertEqual(out.parsetree, expected)

	def testFullParseKnownFile(self):
		"""passing in a known-good input filename to the full parser"""
		for key in inputfiles.keys():
			cmakefn = inputfiles[key]
			expected = parsedfiles[key]
			self.subtest = key
			out = cmakeparser.parse_file(cmakefn)
			self.assertEqual(out.parsetree, expected)

	def testFullParseKnownUppercaseString(self):
		"""passing in a known-good uppercased string to the full parser"""
		for key in inputuppers.keys():
			instring = inputuppers[key]
			expected = parseduppers[key]
			self.subtest = instring
			out = cmakeparser.parse_string(instring)
			self.assertEqual(out.parsetree, expected)

	def testFullParseKnownLowercaseString(self):
		"""passing in a known-good lowercased string to the full parser"""
		for key in inputlowers.keys():
			instring = inputlowers[key]
			expected = parsedlowers[key]
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
