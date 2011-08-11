#! /usr/bin/env python

import os
import re
import sys
import types
from slib.Objects import Object
from slib.Tools import ToolBaseObject, ToolError
from slib.Commands import CommandError
from slib.Commands.Shells import Shell


class LibTool(ToolBaseObject):
	"""The LibTool class."""

	def __init__(self, **kwargs):
		ToolBaseObject.__init__(self,**kwargs)
		
	# End __init__

	
	def __make_command(self, output, input):
		command = "libtool -o " + str(output)
		for ifile in input:
			command += " " + str(ifile)
		
		return command

	# End __make_command	


	def join(self, output_file, input_files):
		if type(input_files) != types.ListType and type(input_files) != types.TupleType:
			raise ToolError("2nd argument must be a list or tuple of file names")

		command = self.__make_command(output_file,input_files)
		self.execute(command)

	# End join
	
# End LibTool

