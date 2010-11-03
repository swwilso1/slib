#! /usr/bin/env python

from slib.FileSystems import FileSystemBaseObject

class CharacterDevice(FileSystemBaseObject):
	"""The CharacterDevice class."""

	def __init__(self, name, path=None):
		FileSystemBaseObject.__init__(self,name,path)

	# End __init__

# End CharacterDevice
