#! /usr/bin/env python

import sys

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

		if self.dry_run:
			return
		
		if self.capture_output:
			capture_output = PIPE
		else:
			capture_output = None
		
		process = Process(str(command),stdout=capture_output, stderr=PIPE)
		
		data = ""
		errors = ""
		while process.poll() == None:
			if process.stdout:
				data += process.stdout.read()
			errors += process.stderr.read()
			
		self.exit_code = process.wait()

		if self.exit_code != return_value:
			raise CommandError("'%s' failed with error %d: %s" % (str(command), self.exit_code, errors))
			

		if len(data) == 0:
			return None

		return data

	# End execute


# End Shell

