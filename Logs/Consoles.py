#! /usr/bin/env python

from slib.Objects import Object
from slib.Logs import LogBase
from slib.Calendars import Date
from slib.Calendars import DATE_TIME_FORMAT

class Console(LogBase):
	"""The Console class."""

	def __init__(self, level = 0, **kwargs):
		LogBase.__init__(self,level, **kwargs)

	# End __init__
	
	def __write(self, format, *args):
		date = Date(format=DATE_TIME_FORMAT)
		newformat = "%s: %s" % (str(date), str(format))
		print newformat % (args)

	# End __write
	

	def __call__(self, format, *args):
		self.__write(format, *args)

	# End __call__
	

	def log(self, format, *args):
		self.__write(format, *args)

	# End log

	def log_with_level(self, level, format, *args):
		if level >= self.level:
			self.__write(format, *args)

	# End logWithLevel	

# End Console
