#! /usr/bin/env python

import slib.FileSystems

class Fifo(slib.FileSystems.FileSystemBaseObject):
	"""The Fifo class."""

	def __init__(self, name, path=None):
		slib.FileSystems.FileSystemBaseObject.__init__(self,name,path)		

	# End __init__

# End Fifo
