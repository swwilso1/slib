#! /usr/bin/env python

import os
import re
import sys
import types
from slib.Objects import Object
from slib.BuildSystems import BuildSystemBaseObject, BuildSystemError
from slib.Commands.Shells import Shell
from slib.FileSystems import FileSystemBaseObject, REGULAR_FILE
from slib.FileSystems.Files import File
from slib.FileSystems.Directories import Directory


class CMakeParameter(Object):
	"""The CMakeParameter class."""

	def __init__(self, name, value):
		Object.__init__(self)
		self.name = name
		self.type = None
		self.value = value
		

	# End __init__

	@property
	def command_line_form(self):
		return str(self)

	# End command_line_form
	

	def __str__(self):
		return "-D" + str(self.name) + ":" + str(self.type) + "=" + str(self.value)
	# End __str__

	def __repr__(self):
		return self.__class__.__name__ + "(" + repr(self.name) + "," + repr(self.value) + ")"

	# End __repr__
	

# End CMakeParameter


class StringParameter(CMakeParameter):
	"""The StringParameter class."""

	def __init__(self, name, value):
		CMakeParameter.__init__(self, name, value)
		self.type = "STRING"

	# End __init__
	

# End StringParameter


class FilePathParameter(CMakeParameter):
	"""The FilePathParameter class."""

	def __init__(self, name, value):
		CMakeParameter.__init__(self, name, value)
		self.type="FILEPATH"

	# End __init__
	
	@property
	def fullpath(self):
		return File(self.value)

	# End fullpath
	
	@property
	def exists(self):
		f = File(self.value)
		return f.exists

	# End exists
	
	
	@property
	def remove(self):
		f = File(self.value)
		f.remove()

	# End remove
	

# End FilePathParameter


class PathParameter(CMakeParameter):
	"""The PathParameter class."""

	def __init__(self, name, value):
		CMakeParameter.__init__(self, name, value)
		self.type="PATH"

	# End __init__

	@property
	def fullpath(self):
		return Directory(self.value)

	# End fullpath
	
	
	@property
	def exists(self):
		d = Directory(self.value)
		return d.exists

	# End exists
	
	@property
	def remove(self):
		d = Directory(self.value)
		d.remove()

	# End remove
	
	

# End PathParameter


class BooleanParameter(CMakeParameter):
	"""The BooleanParameter class."""

	def __init__(self, name, value):
		if value == True:
			value = 'ON'
		else:
			value = 'OFF'
		
		CMakeParameter.__init__(self, name, value)
		self.type="BOOL"

	# End __init__

# End BooleanParameter


class InternalParameter(CMakeParameter):
	"""The InternalParameter class."""

	def __init__(self, name, value):
		CMakeParameter.__init__(self, name, value)
		self.type="INTERNAL"

	# End __init__

# End InternalParameter


class CMakeSystem(BuildSystemBaseObject):
	"""The CMakeSystem class."""

	def __init__(self, working_directory, source_tree_directory, build_parameters = None, **kwargs):
		BuildSystemBaseObject.__init__(self, working_directory, source_tree_directory, build_parameters)
		if kwargs.has_key("generator"):
			self.generator = kwargs['generator']
		else:
			self.generator = None
		self._path_sep_regex = re.compile(os.sep)
		self.active_processors = None
	# End __init__


	def configure(self):
		if not self.source_tree_directory.exists:
			raise BuildSystemError("Source tree %s does not exist" % (self.source_tree_directory.fullpath))
		
		shell = Shell()
		shell.capture_output = True
		shell.raise_error_on_shell_error = False

		self.working_directory.create()
		
		currentDirectory = os.getcwd()
		os.chdir(self.working_directory.fullpath)
		
		o = shell.execute(str(self))
		if shell.exit_code != 0:
			raise BuildSystemError("Error while configuration build system: " + o)
		

		# Now try for make ProcessorCount
		o = shell.execute(self.build_command + " ProcessorCount")
		if shell.exit_code == 0:
			if re.search(r'ACTIVE_PROCESSORS', o):
				lines = o.split("\n")
				for line in lines:
					match = re.search(r'^ACTIVE_PROCESSORS: (\d+)', line)
					if match:
						self.active_processors = match.group(1)
						break

		os.chdir(currentDirectory)

	# End configure
	


	def build(self,target=None,**kwargs):
		if self.working_directory.exists:
			shell = Shell()
			shell.capture_output = True
			shell.raise_error_on_shell_error = False

			currentDirectory = os.getcwd()
			os.chdir(self.working_directory.fullpath)
			

			command = self.build_command

			if kwargs.has_key('processors'):
				if kwargs['processors']:
					command += " -j " + str(kwargs['processors'])
			elif self.active_processors:
				command += " -j " + self.active_processors

			if target:
				command += " " + str(target)
			o = shell.execute(command)
			if shell.exit_code != 0:
				raise BuildSystemError("Error while building: " + o)
			
			os.chdir(currentDirectory)

	# End build


	def install(self):
		if self.working_directory.exists:
			shell = Shell()
			shell.capture_output = True
			currentDirectory = os.getcwd()
			os.chdir(self.working_directory.fullpath)

			command = self.build_command
			
			shell.execute(command + " install/fast")
			
			os.chdir(currentDirectory)

	# End install
	
	
	def remove(self):
		self.working_directory.remove()

	# End remove
	


	def __setitem__(self, key, value):
		if type(value) == types.StringType and self._path_sep_regex.search(value):
			o = FileSystemBaseObject(value)
			if o.exists:
				if o.type == slib.FileSystems.REGULAR_FILE:
					self._build_parameters[key] = FilePathParameter(key,value)
					return
			self._build_parameters[key] = PathParameter(key,value)
		elif type(value) == types.StringType:
			self._build_parameters[key] = StringParameter(key,value)
		elif type(value) == types.BooleanType:
			self._build_parameters[key] = BooleanParameter(key,value)
		else:
			self._build_parameters[key] = StringParameter(key,str(value))
	
	# End __setitem__


	def __str__(self):
		command = "cmake "
		for value in self._build_parameters.values():
			command += str(value) + " "
		
		if self.generator:
			command += "-G " + self.generator + " "
		else:
			if re.search(r'win32',sys.platform):
				command += "-G NMake Makefiles "
		
		command += str(self.source_tree_directory)
		
		return command

	# End __str__
	

	def __repr__(self):
		text =  self.__class__.__name__ + "('" + str(self.working_directory) + "', '" + str(self.source_tree_directory) + "'"
		if len(self._build_parameters.keys()) > 0:
			text += ", " + repr(self._build_parameters)
		
		if self.generator:
			text += ", generator=" + repr(self.generator)
		text += ")"
		
		return text
		

	# End __repr__

	
# End CMakeSystem
