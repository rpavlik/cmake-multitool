#!/usr/bin/env python
"""
Tests for parsing CMake source files

Original Author:
2010 Ryan Pavlik <rpavlik@iastate.edu> <abiryan@ryand.net>
http://academic.cleardefinition.com
Iowa State University HCI Graduate Program/VRAC
"""

import unittest
import cmakeparser

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
			
			
	def testToKnownParses(self):
		pass
	def testToKnownParsesWhitespace(self):
		pass

## Requirement:
## Parsing invalid source trees should fail
if __name__=="__main__":
	## Run tests if executed directly
	pass
