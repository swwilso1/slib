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
from slib.Logs import LogBase
from slib.Calendars import Date
from slib.Calendars import DATE_TIME_FORMAT

class Console(LogBase):
	"""The Console class."""

	def __init__(self, level = 0, **kwargs):
		LogBase.__init__(self,level, **kwargs)

	# End __init__

	def __write(self, format, *args):
		date = Date(format=DATE_TIME_FORMAT)
		newformat = "%s: %s" % (str(date), str(format))
		print newformat % (args)

	# End __write


	def __call__(self, format, *args):
		self.__write(format, *args)

	# End __call__


	def log(self, format, *args):
		self.__write(format, *args)

	# End log

	def log_without_format(self, output):
		date = Date(format=DATE_TIME_FORMAT)
		newoutput = "%s: %s" % (str(date), str(output))
		print newoutput

	# End log_without_format


	def log_with_level(self, level, format, *args):
		if level >= self.level:
			self.__write(format, *args)

	# End logWithLevel

# End Console
