#! /usr/bin/env python

import slib.Objects
import slib.Errors

class LogError(slib.Errors.Error):
	"""The LogError class."""

	def __init__(self, value):
		slib.Errors.Error.__init__(self, value)
	# End __init__

# End LogError


class LogBase(slib.Objects.Object):
	"""The LogBase class."""

	def __init__(self, level = 0):
		slib.Objects.Object.__init__(self)
		self.level = level

	# End __init__


	def __call__(self, format, *args):
		pass

	# End __call__
	


	def log(self, format,*args):
		pass

	# End log

	def logWithLevel(self, level, format, *args):
		pass

	# End logWithLevel

	def close(self):
		pass

	# End close
	

# End LogBase


