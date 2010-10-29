#! /usr/bin/env python

import slib.FileSystems

class CharacterDevice(slib.FileSystems.FileSystemBaseObject):
	"""The CharacterDevice class."""

	def __init__(self, name, path=None):
		slib.FileSystems.FileSystemBaseObject.__init__(self,name,path)

	# End __init__

# End CharacterDevice
