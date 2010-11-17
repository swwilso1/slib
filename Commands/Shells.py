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

	def execute(self,command):
		CommandBase.execute(self,command)

		if self.dry_run:
			return
		
		if self.capture_output:
			capture_output = PIPE
		else:
			capture_output = None
		
		process = Process(str(command),stdout=capture_output, stderr=PIPE)
		
		self.exit_code = process.wait()

		if process.stdout:
			data = process.stdout.readlines()
			errors = process.stderr.read()

			if self.exit_code != 0:
				raise CommandError("'%s' failed with error %d: %s" % (str(command), self.exit_code, errors))
			
			return data
		else:
			errors = process.stderr.read()
			
			if self.exit_code != 0:
				raise CommandError("'%s' failed with error %d" % (str(command), self.exit_code))
			
			return None

	# End execute


# End Shell

