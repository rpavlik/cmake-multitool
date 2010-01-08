#!/usr/bin/env python
"""
Main application to use the CMakeScript packages to output cleaner code.

Original Author:
2010 Ryan Pavlik <rpavlik@iastate.edu> <abiryan@ryand.net>
http://academic.cleardefinition.com
Iowa State University HCI Graduate Program/VRAC
"""

###
# standard packages
import os
import re
from optparse import OptionParser

###
# third-party packages
# - none

###
# internal packages
import cmakescript

def recursive_listdir(dir):
	files = []
	for item in os.listdir(dir):
		
		# Skip hidden files/directories
		if item[0] == ".":
			continue
		
		current = os.path.join(dir, item)
		
		if os.path.isfile(current):
			files.append(current)
		else:
			files.extend(recursive_listdir(current))

	return files

def find_cmake_scripts():
	
	reCMakeLists = r"(?ix)^(CMakeLists\.txt)$"
	reCMakeModule = r"(?ix)(\.cmake)$"
	isScript = re.compile(r"(" + reCMakeLists + r"|" + reCMakeModule + r")")
	
	# remove the current directory and its trailing slash - make a
	# relative path out of it.
	striplen = len(os.getcwd()) + 1
	
	allfiles = [	path
			for path
			in recursive_listdir(os.getcwd())
			if isScript.search( path[striplen:] )	]
	
	return allfiles
	
###
# __main__

if __name__ == "__main__":
	## Can be used as a tool when executed directly
	parser = OptionParser()

	parser.add_option("-d", "--diff",
						action="store_true",
						dest="run_diff",
						default=False,
						help="open a diff/merge app for each file processed")

	parser.add_option("-q", "--quiet",
					action="store_false", dest="verbose", default=True,
					help="don't print status messages to stdout")

	(options, args) = parser.parse_args()

	if len(args) >= 1:
		inputfiles = args[:]
	else:
		inputfiles = find_cmake_scripts()

	diffmerge = ["open",
			"/Applications/DiffMerge.app",
			"-t1='Decrufted'",
			"-t2='Result'",
			"-t3='Original'",
			"{cleaned}",
			"{result}",
			"{orig}"	]
	for infile in inputfiles:
		
		parser = cmakescript.parse_file(infile)
		formatter = cmakescript.CMakeFormatter(parser.parsetree)
		output = formatter.output_as_cmake()
		print "------------------------"
		print infile
		print
		print output