#! /usr/bin/env python

import re
from slib.Objects import Object
from slib.FileSystems import FileSystemBaseObject

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
	
	

# End File
