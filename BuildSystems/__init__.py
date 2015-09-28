#! /usr/bin/env python

import re
import sys
import types

__all__ = ["CMake"]

from slib.Objects import Object
from slib.Errors import Error, ArgumentError
from slib.FileSystems.Directories import Directory

class BuildSystemError(Error):
	"""The BuildSystemError class."""

	def __init__(self, value, **kwargs):
		Error.__init__(self,value, **kwargs)

	# End __init__

# End BuildSystemError


class BuildSystemBaseObject(Object):
	"""The BuildSystemBaseObject class."""

	def __init__(self, working_directory, source_tree_directory, build_parameters = None, **kwargs):
		Object.__init__(self, **kwargs)
		self.working_directory = Directory(str(working_directory))
		self.source_tree_directory = Directory(str(source_tree_directory))
		if build_parameters:
			if type(build_parameters) != types.DictType:
				raise ArgumentError("Third argument must be a dictionary")
			self._build_parameters = build_parameters
		else:
			self._build_parameters = {}

		if kwargs.has_key("command_line_flags"):
			if type(kwargs['command_line_flags']) != types.ListType:
				raise TypeError("command_line_flags must be a List")
			self._commandLineFlags = kwargs['command_line_flags']
		else:
			self._commandLineFlags = []

		self._output_path = None

	# End __init__


	def configure(self):
		pass

	# End configure



	def build(self,target=None):
		pass

	# End build

	def install(self):
		pass

	# End install


	def package(self):
		pass

	# End package



	def remove(self):
		pass

	# End remove


	def add_commandline_flag(self, flag):
		self._commandLineFlags.append(flag)

	# End add_commandline_flag



	@property
	def exists(self):
		return False

	# End exists


	@property
	def build_command(self):
		if re.search(r'win32', sys.platform):
			return "nmake"
		else:
			return "make"

	# End build_command

	@property
	def installer_extension(self):
		if re.search(r'win32', sys.platform):
			return "exe"
		else:
			return "sh"

	# End installer_extension


	@property
	def package_extension(self):
		if re.search(r'win32', sys.platform):
			return "zip"
		else:
			return "tar.gz"

	# End package_extension



	@property
	def output_path(self):
		if self._output_path:
			return self._output_path.fullpath
		return None

	# End output_path

	@output_path.setter
	def output_path(self,value):
		self._output_path = Directory(str(value))

	# End output_path

	def __contains__(self, obj):
		return self.has_key(obj)

	# End __contains__


	def __getitem__(self, key):
		return self._build_parameters[key]

	# End __getitem__


	def __setitem__(self, key, value):
		self._build_parameters[key] = value

	# End __setitem__


	def has_key(self, key):
		return self._build_parameters.has_key(key)

	# End has_key


	def __str__(self):
		pass

	# End __str__


	def __repr__(self):
		text =  self.__class__.__name__ + "('" + str(self.working_directory) + "', '" + str(self.source_tree_directory) + "'"
		if len(self._build_parameters.keys()) > 0:
			text += ", " + repr(self._build_parameters)

		text += ")"

		return text


	# End __repr__


# End BuildSystemBaseObject

import CMake
