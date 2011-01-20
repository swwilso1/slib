#! /usr/bin/env python

__all__ = ["Shells"]

from slib.Objects import Object
from slib.Errors import Error

class CommandError(Error):
	"""The CommandError class."""

	def __init__(self, value, **kwargs):
		Error.__init__(self,value, **kwargs)
	# End __init__

# End CommandError


class CommandBase(Object):
	"""The CommandBase class."""


	def __init__(self, **kwargs):
		Object.__init__(self, **kwargs)

		for key in kwargs:
			self.__dict__[key] = kwargs[key]

		if kwargs.has_key("dry_run"):
			self.dry_run = kwargs["dry_run"]
		else:
			self.dry_run = False

		if kwargs.has_key("capture_output"):
			self.capture_output = kwargs["capture_output"]
		else:
			self.capture_output = False

		self.exit_code = 0
	# End __init__


	def execute(self,command):
		if Object.log_object:
			Object.log_object(command)
		return ""
	# End execute


	def __repr__(self):
		text = self.__class__.__name__ + "("
		
		keys = self.__dict__.keys()
		length = len(keys)
		for i in range(0,length):
			text += str(keys[i]) + "=" + repr(self.__dict__[keys[i]])
			if i < (length - 1):
				text += ", "
		text += ")"
		return text

	# End __repr__
	

# End CommandBase

import Shells