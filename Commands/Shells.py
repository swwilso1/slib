#! /usr/bin/env python

import slib.Commands
from os import system
from commands import getstatusoutput

class Shell(slib.Commands.CommandBase):
	"""The Shell class."""

	def __init__(self):
		slib.Commands.CommandBase.__init__(self)

	# End __init__

	def execute(self,command):
		slib.Commands.CommandBase.execute(self,command)

		if self.dryRun:
			return
		
		if self.captureOutput:
			s,o = getstatusoutput(str(command))
			if s != 0:
				raise slib.Commands.CommandError("'%s' failed with error %d: %s" % (str(command), s, o))
			return o
		else:
			s = system(str(command))
			if s != 0:
				raise slib.Commands.CommandError("'%s' failed with error %d" % (str(command), s))

	# End execute
	

# End Shell

