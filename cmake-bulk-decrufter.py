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
import sys
import os
import re
import subprocess
from optparse import OptionParser

###
# third-party packages
# - none

###
# internal packages
import cmakescript

def recursive_listdir(dir):
	"""
	Return a list of all regular, non-hidden files, recursing directories

	Warning: if you run this on a directory with a lot of files, it may
	end up producing some enormous lists!  Use the iterator version instead
	in those cases, as the input to a "filter" expression.

	This returns the full absolute path to the files, and in no particular
	order (whatever order they are received from os.listdir, when recursing
	depth-first into sub-directories)
	"""
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

def recursive_listdir_iter(dir):
	"""
	An iterator over all regular, non-hidden files in dir and below.

	To best handle directories with many children, use a filter expression
	with recursive_listdir_iter(yourdir) as the "sequence" argument.

	This returns the full absolute path to the files, and in no particular
	order (whatever order they are received from os.listdir, when recursing
	depth-first into sub-directories)
	"""
	for item in os.listdir(dir):
		if item[0] == ".":
			continue

		current = os.path.join(dir, item)
		if os.path.isfile(current):
			yield current
		else:
			for recursive_item in recursive_listdir_iter(current):
				yield recursive_item

def find_cmake_scripts(startPath):

	# Get the path the way we want it.
	startPath = os.path.abspath(startPath)

	if os.path.isfile(startPath):
		# Any file directly passed in is assumed to be a script, no matter its name
		return [startPath]


	# Build a regex to find CMakeLists.txt or *.cmake, case insensitive
	# A match against the filename (not including the path!) means that
	# this is probably a valid input file.
	reCMakeLists = r"(?ix)^(CMakeLists\.txt)$"
	reCMakeModule = r"(?ix)(\.cmake)$"
	isScript = re.compile(r"(" + reCMakeLists + r"|" + reCMakeModule + r")")

	# A little function to use with filter - so we only apply the regex
	# to the file's basename, not the full path
	isPathScript = lambda filepath: isScript.search(os.path.basename(filepath))

	# Now, actually do it.
	# Use our regex to filter the recursive list of files returned
	cmakeScripts = filter(isPathScript, recursive_listdir_iter(startPath))

	return cmakeScripts

class MergeTool:
	mergetools = {	"diffmergemac" :	[
						"open",
						"/Applications/DiffMerge.app",
						"-t1='Decrufted'",
						"-t2='Result'",
						"-t3='Original'",
						"{L}",
						"{C}",
						"{R}"],
					"meld"	:	[
						"meld",
						"--diff",
						"{L}",
						"{C}",
						"{R}"] }

	def __init__(self, tool):
		self.tool = self.mergetools[tool]

	def run(self, left, center, right):
		args = [	arg.format(L=left, R=right, C=center)
					for arg in self.tool	]
		return subprocess.call(args)

class App:
	def __init__(self, args_in=sys.argv[1:]):
		self.args_in = args_in
		self.mergetool = None

	def main(self):
		parser = OptionParser(usage="usage: %prog [options] [[file|dir]...]",
							  version="%prog 0.5, part of the cmakescript tools")

		parser.add_option("-m", "--merge",
							type="choice",
							choices=MergeTool.mergetools.keys(),
							metavar="APPNAME",
							dest="mergetool",
							default=None,
							help="open a diff/merge app APPNAME for each file "
								 "processed.  Supported APPNAME options are: " +
								 " ".join(MergeTool.mergetools.keys())
							)

		parser.add_option("-q", "--quiet",
						action="store_false", dest="verbose", default=True,
						help="don't print status messages to stdout")

		(self.options, args) = parser.parse_args(self.args_in)

		if len(args) == 0:
			args.append(os.getcwd())

		inputfiles = []

		for arg in args:
			inputfiles.extend(find_cmake_scripts(arg))

		for infile in inputfiles:
			print "------------------------"
			print infile
			print "------------------------"

			output = self.processFile(infile)
			print output
			if output is not None:
				# A trailing newline
				output = output + "\n"
				self.runMergeTool(infile, output)


	def processFile(self, filename):
		try:
			parser = cmakescript.parse_file(filename)
		except (cmakescript.IncompleteStatementError,
			   cmakescript.UnclosedChildBlockError):
			return None

		formatter = cmakescript.CMakeFormatter(parser.parsetree)
		return formatter.output_as_cmake()

	def runMergeTool(self, filename, formatted):
		if self.mergetool is None and self.options.mergetool is not None:
			self.mergetool = MergeTool(self.options.mergetool)

		if self.mergetool is not None:
			orig = open(filename, 'r')
			originalscript = orig.read()
			orig.close()

			if originalscript == formatted:
				return

			t1 = subprocess.Popen(["mktemp", "/tmp/Decrufted.XXXXXXXXXX"], stdout=subprocess.PIPE)
			tempclean = t1.communicate()[0]
			t2 = subprocess.Popen(["mktemp", "/tmp/Original.XXXXXXXXXX"], stdout=subprocess.PIPE)
			temporig = t2.communicate()[0]

			temporigfile = open(temporig, 'w', False)
			temporigfile.write(originalscript)
			temporigfile.close()

			tempcleanfile = open(tempclean, 'w', False)
			tempcleanfile.write(formatted)
			tempcleanfile.close()

			self.mergetool.run(tempclean, filename, temporig)

###
# __main__

if __name__ == "__main__":
## Can be used as a tool when executed directly
	app = App()
	app.main()