#! /usr/bin/env python

import slib.FileSystems


class SymbolicLink(slib.FileSystems.FileSystemBaseObject):
	"""The SymbolicLink class."""

	def __init__(self, name, path=None):
		slib.FileSystems.FileSystemBaseObject.__init__(self,name,path)		

	# End __init__

# End SymbolicLink
