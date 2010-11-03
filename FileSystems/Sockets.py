#! /usr/bin/env python

from slib.FileSystems import FileSystemBaseObject

class Socket(FileSystemBaseObject):
	"""The Socket class."""

	def __init__(self, name, path=None):
		FileSystemBaseObject.__init__(self,name,path)

	# End __init__

# End Socket
