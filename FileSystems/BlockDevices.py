#! /usr/bin/env python

from slib.FileSystems import FileSystemBaseObject

class BlockDevice(FileSystemBaseObject):
	"""The BlockDevice class."""

	def __init__(self, name, path=None, **kwargs):
		FileSystemBaseObject.__init__(self,name,path, **kwargs)

	# End __init__

# End BlockDevice
