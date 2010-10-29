#! /usr/bin/env python

import slib.FileSystems

class BlockDevice(slib.FileSystems.FileSystemBaseObject):
	"""The BlockDevice class."""

	def __init__(self, name, path=None):
		slib.FileSystems.FileSystemBaseObject.__init__(self,name,path)		

	# End __init__

# End BlockDevice
