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

	
	def copy(self, source, destination, options = []):
		shell = Shell()

		command = self.copy_command
		for opt in options:
			command += " " + str(opt)
		
		command += " " + str(source) + " " + str(destination)

		Object.logIfVerbose(command)
		o = self.execute(command)
		Object.logIfVerbose(o)

	# End copy


	def copy_multiple(self, sources, destination):
		if type(sources) != types.ListType and type(sources) != types.TupleType:
			raise ToolError("First argument of copy_multiple method must be a list or tuple object.")
		shell = Shell()
		source_list = ""
		for source in sources:
			source_list += str(source) + " "
		
		command = self.copy_command + " " + source_list + str(destination)
		
		Object.logIfVerbose(command)
		o = self.execute(command)
		Object.logIfVerbose(o)

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
		
		command += " " + str(source) + " " + str(destination)

		Object.logIfVerbose(command)
		o = self.execute(command)
		Object.logIfVerbose(o)

	# End copy_recursively
	
	

# End CopyTool
