#! /usr/bin/env python

import os
import re
import sys
import types
from .. Objects import Object
from .. Tools import ToolBaseObject, ToolError
from .. Commands import CommandError
from .. Commands.Shells import Shell


class CopyTool(ToolBaseObject):
	"""The CopyTool class."""

	def __init__(self, **kwargs):
		ToolBaseObject.__init__(self,**kwargs)

		if re.search(r'win32', sys.platform):
			self.copy_command = 'copy'
		else:
			self.copy_command = 'cp'

		if 'use_cmake' in kwargs:
			if kwargs["use_cmake"]:
				self.copy_command = 'cmake -E copy'

		self.use_escaped_characters = True

	# End __init__


	def __escapeDifficultCharacters(self, value):

		value = re.sub(r' ', r'\ ', value)
		value = re.sub(r"'", r"\'", value)
		value = re.sub(r'\?', r'\\?', value)
		value = re.sub(r'\&', r'\\&', value)
		value = re.sub(r'\(', r"\(", value)
		value = re.sub(r'\)', r"\)", value)

		return value

	# End __escapeDifficultCharacters



	def copy(self, source, destination, options = []):
		shell = Shell()

		command = self.copy_command
		for opt in options:
			command += " " + str(opt)

		if self.use_escaped_characters:
			source = self.__escapeDifficultCharacters(str(source))
			destination = self.__escapeDifficultCharacters(str(destination))

		command += " " + str(source) + " " + str(destination)
		self.execute(command)

	# End copy


	def copy_multiple(self, sources, destination):
		if type(sources) != types.ListType and type(sources) != types.TupleType:
			raise ToolError("First argument of copy_multiple method must be a list or tuple object.")
		shell = Shell()
		source_list = ""
		for source in sources:
			if self.use_escaped_characters:
				source = self.__escapeDifficultCharacters(str(source))
			source_list += str(source) + " "

		if self.use_escaped_characters:
			destination = self.__escapeDifficultCharacters(str(destination))

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

		if self.use_escaped_characters:
			source = self.__escapeDifficultCharacters(str(source))
			destination = self.__escapeDifficultCharacters(str(destination))

		command += " " + str(source) + " " + str(destination)
		self.execute(command)

	# End copy_recursively



# End CopyTool
