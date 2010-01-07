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
from optparse import OptionParser

###
# third-party packages
# - none

###
# internal packages
# - none



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
		inputfiles = "hostlist.xml"
