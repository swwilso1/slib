#! /usr/bin/env python

from slib.Objects import Object
from slib.FileSystems import FileSystemBaseObject

class Fifo(FileSystemBaseObject):
	"""The Fifo class."""

	def __init__(self, name, **kwargs):
		FileSystemBaseObject.__init__(self,name, **kwargs)

	# End __init__

# End Fifo
