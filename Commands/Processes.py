#! /usr/bin/env python

import sys
from slib.Objects import Object
from slib.Errors import Error

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
		if kwargs.has_key("stdout"):
			if kwargs["stdout"] == STDOUT:
				raise ProcessError("stdout keyword can only be PIPE or None")
			self._stdout = kwargs["stdout"]
		else:
			self._stdout = None
		
		if kwargs.has_key("stderr"):
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


if sys.version_info[0] >= 2 and sys.version_info[1] >= 6:
	import subprocess
	from shlex import split

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
	

	class Process(ProcessBaseObject):
		"""The Process class."""

		def __init__(self, args, **kwargs):
			ProcessBaseObject.__init__(self,args,**kwargs)
			
			self.shell = False
			if kwargs.has_key("shell"):
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

else:
	# We have a version of Python < 2.6
	import popen2
	from shlex import split
	
	class Process(ProcessBaseObject):
		"""The Process class."""

		def __init__(self, args, **kwargs):
			ProcessBaseObject.__init__(self, args, **kwargs)
			
			self.shell = True
			if kwargs.has_key("shell"):
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
					stdoutdata += self.__process.fromchild.read()
					if self.__process.childerr != None:
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
	
	

