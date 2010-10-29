#! /usr/bin/env python

import slib.FileSystems

class Socket(slib.FileSystems.FileSystemBaseObject):
	"""The Socket class."""

	def __init__(self, name, path=None):
		slib.FileSystems.FileSystemBaseObject.__init__(self,name,path)

	# End __init__

# End Socket
