#! /usr/bin/env python

import slib.Objects
import slib.Errors
import slib.Logs.Consoles
import slib.Logs.Files

class CommandError(slib.Errors.Error):
	"""The CommandError class."""

	def __init__(self, value):
		slib.Errors.Error.__init__(self,value)
	# End __init__

# End CommandError


class CommandBase(slib.Objects.Object):
	"""The CommandBase class."""

	def __init__(self):
		slib.Objects.Object.__init__(self)
		self.dryRun = False
		self.captureOutput = False
		self.log = None
		self.exit_code = 0
	# End __init__


	def execute(self,command):
		if self.log:
			self.log(command)
		return ""
	# End execute
		

# End CommandBase
