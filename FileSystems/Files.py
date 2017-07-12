#! /usr/bin/env python

################################################################################
#
# Tectiform Open Source License (TOS)
#
# Copyright (c) 2015 Tectiform Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
################################################################################

import re
from slib.Objects import Object
from slib.FileSystems import FileSystemBaseObject
from slib.FileSystems import FileSystemError

class File(FileSystemBaseObject):
	"""The File class."""

	def __init__(self, name, **kwargs):
		FileSystemBaseObject.__init__(self,name,**kwargs)

	# End __init__

	@property
	def contents(self):
		if not self.regular:
			raise FileSystemError("%s not a regular file, no contents available" % (str(self.fullpath)))
		if self.canRead:
			if self.regular:
				f = open(self.fullpath,"r")
				return f.readlines()
			else:
				raise FileSystemError("%s not a regular file, contents not available" % (str(self.fullpath)))
		else:
			raise FileSystemError("Current user does not have read permissions for %s" % (str(self.fullpath)))
	# End contents



	@property
	def contentsAsString(self):
		if not self.regular:
			raise FileSystemError("%s not a regular file, no contents available" % (str(self.fullpath)))
		if self.canRead:
			f = open(self.fullpath, "r")
			return f.read()
		else:
			raise FileSystemError("Current user does not have read permissions for %s" % (str(self.fullpath)))
	# End contentsAsString


	@property
	def extension(self):
		if self.name.count('.') > 0:
			match = re.search(r'.*\.(.*)$', self.name)
			if match:
				return match.group(1)
		return None

	# End extension


	@property
	def lineEndings(self):
		unix = False
		windows = False
		for line in self.contents:
			if line[-2:] == '\r\n':
				windows = True
			elif line[-1] == '\n':
				unix = True

		if unix and windows:
			return ("Unix", "Windows")
		elif unix:
			return "Unix"
		elif windows:
			return "Windows"
		return None

	# End lineEndings


	def convertLineEndings(self, platform = None):
		newlines = []
		if platform == "Unix":
			for line in self.contents:
				modLine = line
				if line[-2:] == '\r\n':
					modLine = line[:-2] + '\n'
				newlines.append(modLine)

		elif platform == "Windows":
			for line in self.contents:
				modLine = line
				if line[-1:] == '\n' and (not line[-2:] == '\r\n'):
					modLine = line[:-1] + '\r\n'
				newlines.append(modLine)

		else:
			for line in self.contents:
				modLine = line
				if re.search(r'\r\n$', line):
					modLine = re.sub(r'\r\n$','\n', line)
				elif re.search(r'\n$', line):
					modLine = re.sub(r'\n$', r'\r\n', line)
				newlines.append(modLine)


		try:
			f = open(self.fullpath,"w")
		except IOError as e:
			raise FileSystemError("Cannot write to file %s: %s" % (str(self.fullpath), str(e)))

		f.writelines(newlines)
		f.close()

	# End convertLineEndings


	def updateContents(self, newlines=[]):
		if not self.regular:
			raise FileSystemError("%s not a regular file, cannot change file" % (str(self.fullpath)))
		if self.canRead:
			if self.regular:
				f = open(self.fullpath,"w")
				return f.writelines(newlines)
			else:
				raise FileSystemError("%s not a regular file, cannot change file" % (str(self.fullpath)))
		else:
			raise FileSystemError("Current user does not have write permissions for %s" % (str(self.fullpath)))
	# End updateContents


	def create(self):
		if not self.exists:
			try:
				f = open(self.fullpath, "w")
			except IOError as e:
				raise FileSystemError("Cannot open file %s for writing: %s" % (str(self.fullpath), str(e)))
			f.writelines([" "])


	def openForReading(self):
		try:
			f = open(self.fullpath, "r")
		except IOError as e:
			raise FileSystemError("Cannot open file %s for reading: %s" % (str(self.fullpath), str(e)))

		return f
	# End openForReading


	def openForWriting(self):
		try:
			f = open(self.fullpath, "w")
		except IOError as e:
			raise FileSystemError("Cannot open file %s for writing: %s" % (str(self.fullpath), str(e)))

		return f
	# End openForWriting


	def openForAppending(self):
		try:
			f = open(self.fullpath, "a")
		except IOError as e:
			raise FileSystemError("Cannot open file %s for appending: %s" % (str(self.fullpath), str(e)))

		return f
	# End openForAppending

# End File
