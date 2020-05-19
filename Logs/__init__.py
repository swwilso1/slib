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

from .. Objects import Object
from .. Errors import Error

__all__ = ["Consoles", "Files"]

class LogError(Error):
	"""The LogError class."""

	def __init__(self, value,**kwargs):
		Error.__init__(self, value, **kwargs)
	# End __init__

# End LogError


class LogBase(Object):
	"""The LogBase class."""

	def __init__(self, level = 0, **kwargs):
		Object.__init__(self, **kwargs)
		self.level = level

	# End __init__


	def __call__(self, format, *args):
		pass

	# End __call__



	def log(self, format,*args):
		pass

	# End log

	def log_without_format(self, output):
		pass

	# End log_without_format


	def log_with_level(self, level, format, *args):
		pass

	# End logWithLevel

	def close(self):
		pass

	# End close


# End LogBase

from . import Consoles, Files

