#! /usr/bin/env python

################################################################################
#
# Tectiform Open Source License (TOS)
#
# Copyright (c) 2015 Tectiform Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
################################################################################

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

__all__ = ["Shells", "CommandError"]

import Shells