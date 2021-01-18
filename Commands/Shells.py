#! /usr/bin/env python

################################################################################
#
# Tectiform Open Source License (TOS)
#
# Copyright (c) 2015 Tectiform Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
################################################################################

import sys, re

from .. Objects import Object
from .. Commands import CommandBase, CommandError
from .. Commands.Processes import Process, PIPE, STDOUT


class Shell(CommandBase):
	"""The Shell class."""

	def __init__(self, **kwargs):
		CommandBase.__init__(self, **kwargs)
		if 'raise_error_on_shell_error' in kwargs:
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

		if errors != None and len(errors) > 0:
			if rvalue != None:
				final_output = str(rvalue) + "\n" + str(errors)
			else:
				final_output = errors
		else:
			final_output = rvalue

		Object.logIfVerbose(self,final_output,no_format=True)

		return rvalue

	# End execute


# End Shell

