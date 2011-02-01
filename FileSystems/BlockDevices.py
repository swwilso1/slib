#! /usr/bin/env python

from slib.Objects import Object
from slib.FileSystems import FileSystemBaseObject

class BlockDevice(FileSystemBaseObject):
	"""The BlockDevice class."""

	def __init__(self, name, **kwargs):
		FileSystemBaseObject.__init__(self,name,**kwargs)

	# End __init__

# End BlockDevice
