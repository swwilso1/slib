#! /usr/bin/env python

import os
import re
import sys
import types
from .. Objects import Object
from .. Tools import ToolBaseObject, ToolError
from .. Commands import CommandError
from .. Commands.Shells import Shell
from .. FileSystems.Directories import Directory


class ZipTool(ToolBaseObject):
	"""The ZipTool class."""

	def __init__(self, **kwargs):
		ToolBaseObject.__init__(self,**kwargs)

	# End __init__


	def zip_directory(self, directory, output_name):
		folder = Directory(str(directory))
		path = Directory(folder.path)
		current_working_directory = path.make_current_directory()

		command = "zip -q -r " + str(output_name) + " " + folder.name
		self.execute(command)

		current_working_directory.make_current_directory()

	# End zip_directory


# End ZipTool
