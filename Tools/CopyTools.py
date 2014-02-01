#! /usr/bin/env python

import os
import re
import sys
import types
from slib.Objects import Object
from slib.Tools import ToolBaseObject, ToolError
from slib.Commands import CommandError
from slib.Commands.Shells import Shell


class CopyTool(ToolBaseObject):
	"""The CopyTool class."""

	def __init__(self, **kwargs):
		ToolBaseObject.__init__(self,**kwargs)

		if re.search(r'win32', sys.platform):
			self.copy_command = 'copy'
		else:
			self.copy_command = 'cp'

		if kwargs.has_key("use_cmake"):
			if kwargs["use_cmake"]:
				self.copy_command = 'cmake -E copy'

	# End __init__


	def __escapeDifficultCharacters(self, value):

		value = re.sub(r' ', r'\ ', value)
		value = re.sub(r"'", r"\'", value)
		value = re.sub(r'\?', r'\\?', value)
		value = re.sub(r'\&', r'\\&', value)

		return value

	# End __escapeDifficultCharacters


	
	def copy(self, source, destination, options = []):
		shell = Shell()

		command = self.copy_command
		for opt in options:
			command += " " + str(opt)

		source = self.__escapeDifficultCharacters(source)		
		destination = self.__escapeDifficultCharacters(destination)

		command += " " + str(source) + " " + str(destination)
		self.execute(command)

	# End copy


	def copy_multiple(self, sources, destination):
		if type(sources) != types.ListType and type(sources) != types.TupleType:
			raise ToolError("First argument of copy_multiple method must be a list or tuple object.")
		shell = Shell()
		source_list = ""
		for source in sources:
			source = self.__escapeDifficultCharacters(source)
			source_list += str(source) + " "
		
		destination = self.__escapeDifficultCharacters(destination)

		command = self.copy_command + " " + source_list + str(destination)		
		self.execute(command)

	# End copy_multiple
	
	
	def copy_recursively(self, source, destination, options=[]):
		if re.search(r'win32', sys.platform):
			copy_command = 'xcopy'
		else:
			copy_command = 'cp -R'
		
		if re.search(r'cmake',self.copy_command):
			copy_command = self.copy_command
		
		command = copy_command
		for opt in options:
			command += " " + str(opt)

		source = self.__escapeDifficultCharacters(source)
		destination = self.__escapeDifficultCharacters(destination)
		
		command += " " + str(source) + " " + str(destination)
		self.execute(command)

	# End copy_recursively
	
	

# End CopyTool
