#! /usr/bin/env python

from slib.Objects import Object
from slib.Errors import Error

__all__ = ["Consoles", "Files"]

class LogError(Error):
	"""The LogError class."""

	def __init__(self, value):
		Error.__init__(self, value)
	# End __init__

# End LogError


class LogBase(Object):
	"""The LogBase class."""

	def __init__(self, level = 0):
		Object.__init__(self)
		self.level = level

	# End __init__


	def __call__(self, format, *args):
		pass

	# End __call__
	


	def log(self, format,*args):
		pass

	# End log

	def log_with_level(self, level, format, *args):
		pass

	# End logWithLevel

	def close(self):
		pass

	# End close
	

# End LogBase

import Consoles
import Files


