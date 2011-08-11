#! /usr/bin/env python

from slib.Objects import Object
from slib.Logs import LogBase, LogError
from slib.Calendars import Date
from slib.Calendars import DATE_TIME_FORMAT

class File(LogBase):
	"""The File class."""

	def __init__(self, level = 0, **kwargs):
		LogBase.__init__(self, level, **kwargs)
		self.logFile = None
		self.autoNewLine = True
	# End __init__

	def open(self, file, mode):
		if not Object.global_dry_run:
			self.logFile = open(file, mode)

	# End open

	def close(self):
		if self.logFile:
			self.logFile.close()

	# End close
	
	def __output_string(self, format, *args):
		date = Date(format=DATE_TIME_FORMAT)
		newformat = "%s: %s" % (str(date), str(format))
		return newformat % (args)

	# End __write
	
	
	def __call__(self, format, *args):
		if self.logFile:
			if self.logFile.closed:
				raise LogError("%s closed" % self.logFile.name)
			else:
				self.logFile.write(self.__output_string(format, *args))
				if self.autoNewLine:
					self.logFile.write("\n")
				self.logFile.flush()
		else:
			raise LogError("No associated log file, not yet opened")

	# End __call__
	
	
	def log(self,format,*args):
		if self.logFile:
			if self.logFile.closed:
				raise LogError("%s closed" % self.logFile.name)
			else:
				self.logFile.write(self.__output_string(format, *args))
				if self.autoNewLine:
					self.logFile.write("\n")
				self.logFile.flush()
		else:
			raise LogError("No associated log file, not yet opened")

	# End log


	def log_without_format(self, output):
		if self.logFile:
			if self.logFile.closed:
				raise LogError("%s closed" % self.logFile.name)
			else:
				date = Date(format=DATE_TIME_FORMAT)
				newoutput = "%s: %s" % (str(date),str(output))
				self.logFile.write(newoutput)
				if self.autoNewLine:
					self.logFile.write("\n")
				self.logFile.flush()
		else:
			raise LogError("No associated log file, not yet opened")

	# End log_without_format
	

	def log_with_level(self,level,format,*args):
		if level >= self.level:
			self.log(format,args)

	# End logWithLevel
	

# End File
