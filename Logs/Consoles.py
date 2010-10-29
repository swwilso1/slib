#! /usr/bin/env python

import slib.Logs

class Console(slib.Logs.LogBase):
	"""The Console class."""

	def __init__(self, level = 0):
		slib.Logs.LogBase.__init__(self,level)

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
