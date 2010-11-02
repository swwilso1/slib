#! /usr/bin/env python

import slib.Objects
import slib.Errors
import slib.Logs.Consoles
import slib.Logs.Files

class CommandError(slib.Errors.Error):
	"""The CommandError class."""

	def __init__(self, value):
		slib.Errors.Error.__init__(self,value)
	# End __init__

# End CommandError


class CommandBase(slib.Objects.Object):
	"""The CommandBase class."""

	def __init__(self, **kwargs):
		slib.Objects.Object.__init__(self)

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

		if kwargs.has_key("log"):
			self.log = kwargs["log"]
		else:
			self.log = None

		self.exit_code = 0
	# End __init__


	def execute(self,command):
		if self.log:
			self.log(command)
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
