#! /usr/bin/env python

import sys, re

from slib.Objects import Object
from slib.Commands import CommandBase, CommandError
from slib.Commands.Processes import Process, PIPE, STDOUT


class Shell(CommandBase):
	"""The Shell class."""

	def __init__(self, **kwargs):
		CommandBase.__init__(self, **kwargs)
		if kwargs.has_key("raise_error_on_shell_error"):
			self.raise_error_on_shell_error = kwargs["raise_error_on_shell_error"]
		else:
			self.raise_error_on_shell_error = True
	# End __init__

	def execute(self,command,return_value=0):
		CommandBase.execute(self,command)
		
		if self.dry_run or Object.global_dry_run:
			return
		
		if self.capture_output or Object.getClassVerbose(self):
			capture_output = PIPE
		else:
			capture_output = None
		
		process = Process(str(command),stdout=capture_output, stderr=PIPE,shell=True)
		
		data,errors = process.communicate()
			
		self.exit_code = process.wait()

		if self.exit_code != return_value:
			raise CommandError("'%s' failed with error %d: %s" % (str(command), self.exit_code, errors))
			

		rvalue = data

		if data != None:
			if len(data) == 0:
				rvalue = None
		
		if(rvalue != None and len(rvalue) > 0):
			rvalue = re.sub(r'%','\\%',rvalue)
		
		Object.logIfVerbose(self,rvalue)
		
		return rvalue

	# End execute	


# End Shell

