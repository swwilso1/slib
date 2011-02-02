#! /usr/bin/env python

import os
import re
import sys
import types
from slib.Objects import Object
from slib.Tools import ToolBaseObject, ToolError
from slib.Commands import CommandError
from slib.Commands.Shells import Shell
from slib.FileSystems.Directories import Directory


class ZipTool(ToolBaseObject):
	"""The ZipTool class."""

	def __init__(self, **kwargs):
		ToolBaseObject.__init__(self,**kwargs)

	# End __init__
	
	
	def zip_directory(self, directory, output_name):
		folder = Directory(str(directory))
		path = Directory(folder.path)
		current_working_directory = path.make_current_directory()
		
		self.execute("zip -R " + folder.name + " " + str(output_name))

		current_working_directory.make_current_directory()

	# End zip_directory
	

# End ZipTool
