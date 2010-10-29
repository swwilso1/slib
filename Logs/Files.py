#! /usr/bin/env python

import slib.Logs

class File(slib.Logs.LogBase):
	"""The File class."""

	def __init__(self, level = 0):
		slib.Logs.LogBase.__init__(self, level)
		self.logFile = None
		self.autoNewLine = True
	# End __init__

	def open(self, file, mode):
		self.logFile = open(file, mode)

	# End open

	def close(self):
		self.logFile.close()

	# End close
	
	def __call__(self, format, *args):
		if self.logFile:
			if self.logFile.closed:
				raise slib.Logs.LogError("%s closed" % self.logFile.name)
			else:
				self.logFile.write(format % (args))
				if self.autoNewLine:
					self.logFile.write("\n")
				self.logFile.flush()
		else:
			raise slib.Logs.LogError("No associated log file, not yet opened")

	# End __call__
	
	
	def log(self,format,*args):
		if self.logFile:
			if self.logFile.closed:
				raise slib.Logs.LogError("%s closed" % self.logFile.name)
			else:
				self.logFile.write(format % (args))
				if self.autoNewLine:
					self.logFile.write("\n")
				self.logFile.flush()
		else:
			raise slib.Logs.LogError("No associated log file, not yet opened")

	# End log
	
	def logWithLevel(self,level,format,*args):
		if level >= self.level:
			self.log(format,args)

	# End logWithLevel
	

# End File
