#! /usr/bin/env python

from slib.Commands import CommandBase, CommandError
from os import system
from commands import getstatusoutput

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
			self.exit_code,o = getstatusoutput(str(command))
			if self.raise_error_on_shell_error:
				if self.exit_code != 0:
					raise CommandError("'%s' failed with error %d: %s" % (str(command), self.exit_code, o))
			return o
		else:
			self.exit_code = system(str(command))
			if self.raise_error_on_shell_error:
				if self.exit_code != 0:
					raise CommandError("'%s' failed with error %d" % (str(command), self.exit_code))
			return None

	# End execute


# End Shell

