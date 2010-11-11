#! /usr/bin/env python

from slib.FileSystems import FileSystemBaseObject

class File(FileSystemBaseObject):
	"""The File class."""

	def __init__(self, name, path=None, **kwargs):
		FileSystemBaseObject.__init__(self,name,path, **kwargs)

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

# End File
