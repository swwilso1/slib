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

import sys
from .. Objects import Object
from .. Errors import Error

class ProcessError(Error):
	"""The ProcessError class."""

	def __init__(self, value):
		Error.__init__(self,value)

	# End __init__

# End ProcessError


class ProcessCommandBase(Object):
	"""The ProcessCommandBase class."""

	def __init__(self, command):
		Object.__init__(self)
		self.command = command

	# End __init__


	@property
	def process_form(self):
		return self.command

	# End process_form



	def __repr__(self):
		return self.__class__.__name__ + "(" + self.command + ")"

	# End __repr__


# End ProcessCommandBase


PIPE = 1
STDOUT = 2

class ProcessBaseObject(Object):
	"""The ProcessBaseObject class."""

	def __init__(self, args, **kwargs):
		self.args = args
		if 'stdout' in kwargs:
			if kwargs["stdout"] == STDOUT:
				raise ProcessError("stdout keyword can only be PIPE or None")
			self._stdout = kwargs["stdout"]
		else:
			self._stdout = None

		if 'stderr' in kwargs:
			self._stderr = kwargs["stderr"]
		else:
			self._stderr = None

	# End __init__


	def wait(self):
		return 0

	# End wait


	def poll(self):
		return 0

	# End poll


	@property
	def stdout(self):
		pass

	# End stdout


	@property
	def stderr(self):
		pass

	# End stderr


	@property
	def stdin(self):
		pass

	# End stdin


	@property
	def pid(self):
		pass

	# End pid


	def __repr__(self):
		value = self.__class__.__name__ + "(" + repr(self.args)
		if self._stdout == PIPE:
			value += ", stdout=PIPE"

		if self._stderr == PIPE:
			value += ", stderr=PIPE"
		elif self._stderr == STDOUT:
			value += ", stderr=STDOUT"

		value += ")"

		return value

	# End __repr__


# End ProcessBaseObject

class ProcessCommand(ProcessCommandBase):
	"""The ProcessCommand class."""

	def __init__(self, command):
		ProcessCommandBase.__init__(self,command)

	# End __init__

	@property
	def process_form(self):
		return split(self.command)

	# End process_form

# End ProcessCommand


useSubprocess = False
usePopen2 = False

try:
	import subprocess
	useSubprocess = True
except ImportError as e:
	import popen2
	import select
	usePopen2 = True


if useSubprocess:
	from shlex import split

	class Process(ProcessBaseObject):
		"""The Process class."""

		def __init__(self, args, **kwargs):
			ProcessBaseObject.__init__(self,args,**kwargs)

			self.shell = False
			if 'shell' in kwargs:
				if kwargs["shell"] == True:
					self.shell = True

			else:
				command = ProcessCommand(self.args)
				self.args = command.process_form

			if self._stdout == PIPE:
				stdout_value = subprocess.PIPE
			else:
				stdout_value = None

			if self._stderr == PIPE:
				stderr_value = subprocess.PIPE
			elif self._stderr == STDOUT:
				stderr_value = subprocess.STDOUT
			else:
				stderr_value = None

			if not Object.global_dry_run:
				self.__process = subprocess.Popen(self.args,stdin=subprocess.PIPE,stdout=stdout_value,stderr=stderr_value,shell=self.shell)
			else:
				self.__process = None

		# End __init__


		def wait(self):
			if self.__process:
				return self.__process.wait()

			return 0

		# End wait


		def poll(self):
			if self.__process:
				return self.__process.poll()

			return None

		# End poll


		def communicate(self, input=None):
			if self.__process:
				return self.__process.communicate(input)

			return ("","")

		# End communicate



		@property
		def stdout(self):
			if self.__process:
				return self.__process.stdout

			return None

		# End stdout


		@property
		def stderr(self):
			if self.__process:
				return self.__process.stderr

			return None

		# End stderr


		@property
		def stdin(self):
			if self.__process:
				return self.__process.stdin

			return None

		# End stdin


		@property
		def pid(self):
			if self.__process:
				return self.__process.pid

			return 0

		# End pid

	# End Process

elif usePopen2:
	from shlex import split

	class Process(ProcessBaseObject):
		"""The Process class."""

		def __init__(self, args, **kwargs):
			ProcessBaseObject.__init__(self, args, **kwargs)

			self.shell = True
			if 'shell' in kwargs:
				if kwargs["shell"] == False:
					self.shell = False
					self.args = split(self.args)

			if self._stderr == PIPE:
				stderr_value = True
			else:
				stderr_value = False

			command = ProcessCommand(self.args)
			self.args = command.process_form

			if not Object.global_dry_run:
				self.__process = popen2.Popen3(self.args, capturestderr=stderr_value)
			else:
				self.__process = None

		# End __init__


		def wait(self):
			if self.__process:
				return self.__process.wait()

			return 0

		# End wait


		def poll(self):
			if self.__process:
				result = self.__process.poll()
				if result == -1:
					return None
				return result

			return None

		# End poll


		def communicate(self, input=None):
			if self.__process:
				stdoutdata = ""
				stderrdata = ""
				while self.__process.poll() == -1:
					result = select.select([self.__process.fromchild],[],[],0)
					if len(result[0]) > 0:
						stdoutdata += self.__process.fromchild.read()
					if self.__process.childerr != None:
						result = select.select([self.__process.childerr],[],[],0)
						if len(result[0]) > 0:
							stderrdata += self.__process.childerr.read()

				return (stdoutdata, stderrdata)

			return ("", "")

		# End communicate



		@property
		def stdout(self):
			if self.__process:
				return self.__process.fromchild

			return None

		# End stdout


		@property
		def stderr(self):
			if self.__process:
				return self.__process.childerr

			return None

		# End stderr


		@property
		def stdin(self):
			if self.__process:
				return self.__process.tochild

			return None

		# End stdin


		@property
		def pid(self):
			if self.__process:
				return self.__process.pid

			return 0

		# End pid

	# End Process



