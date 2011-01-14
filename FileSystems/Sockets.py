#! /usr/bin/env python

from slib.Objects import Object
from slib.FileSystems import FileSystemBaseObject

class Socket(FileSystemBaseObject):
	"""The Socket class."""

	def __init__(self, name, path=None, **kwargs):
		FileSystemBaseObject.__init__(self,name,path,**kwargs)

	# End __init__

# End Socket
