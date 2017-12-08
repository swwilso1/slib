#! /usr/bin/env python

import re
import sys
import types

__all__ = ["CopyTools", "LibTools", "ZipTools"]

from slib.Objects import Object
from slib.Errors import Error, ArgumentError
from slib.Commands import CommandError
from slib.Commands.Shells import Shell

class ToolError(Error):
	"""The ToolError class."""

	def __init__(self, value, **kwargs):
		Error.__init__(self,value,**kwargs)

	# End __init__

# End ToolError


class ToolBaseObject(Object):
	"""The ToolBaseObject class."""

	def __init__(self, **kwargs):
		Object.__init__(self, **kwargs)

	# End __init__


	def execute(self, command):
		shell = Shell()
		try:
			shell.execute(command)
		except CommandError as e:
			message = str(e)
			raise ToolError(message)

	# End execute


	def __str__(self):
		return ""

	# End __str__


	def __repr__(self):
		return self.__class__.__name__ + "()"
	# End __repr__


# End ToolBaseObject

__all__ = [
	"CopyTools",
	"LibTools",
	"ZipTools",
	"ToolError"
]

import CopyTools
import LibTools
import ZipTools


