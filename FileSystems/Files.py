#! /usr/bin/env python

import slib.FileSystems

class File(slib.FileSystems.FileSystemBaseObject):
	"""The File class."""

	def __init__(self, name, path=None):
		slib.FileSystems.FileSystemBaseObject.__init__(self,name,path)

	# End __init__

	@property
	def contents(self):
		if not self.regular:
			raise slib.FileSystems.FileSystemException("%s not a regular file, no contents available" % (str(self.fullpath)))
		if self.canRead:
			if self.regular:
				f = open(self.fullpath,"r")
				return f.readlines()
			else:
				raise slib.FileSystems.FileSystemException("%s not a regular file, contents not available" % (str(self.fullpath)))
		else:
			raise slib.FileSystems.FileSystemException("Current user does not have read permissions for %s" % (str(self.fullpath)))
	# End contents

# End File
