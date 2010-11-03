#! /usr/bin/env python

from slib.Logs import LogBase

class Console(LogBase):
	"""The Console class."""

	def __init__(self, level = 0):
		LogBase.__init__(self,level)

	# End __init__

	def __call__(self, format, *args):
		print format % (args)

	# End __call__
	

	def log(self, format, *args):
		print format % (args)

	# End log

	def logWithLevel(self, level, format, *args):
		if level >= self.level:
			print format % (args)

	# End logWithLevel	

# End Console
