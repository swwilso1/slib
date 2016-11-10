import types

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

class Object(object):
	"""The Object class."""

	log_object = None
	global_dry_run = False

	def __init__(self, **kwargs):
		if kwargs.has_key("log"):
			Object.log_object = kwargs["log"]

		if kwargs.has_key("verbose"):
			if type(kwargs["verbose"]) != types.BooleanType:
				raise TypeError("verbose keyword value must be Boolean")
			Object.verbose = kwargs["verbose"]


	# End __init__


	def setClassVerbose(self, arg):
		if type(arg) != types.BooleanType:
			raise TypeError("Argument must be boolean")
		Object.verbose = arg

	# End setClassVerbose


	def getClassVerbose(self):
		if Object.__dict__.has_key("verbose"):
			return Object.verbose
		return False

	# End getClassVerbose


	def setClassLog(self, log):
		Object.log_object = log

	# End set_class_log

	def enableGlobalDryRun(self):
		Object.global_dry_run = True

	# End enableGlobalDryRun

	def logIfVerbose(self, arg, **keyargs):
		if Object.log_object and Object.getClassVerbose(self) and arg != None:
			needs_format = True
			if keyargs.has_key("no_format"):
				if type(keyargs["no_format"]) != types.BooleanType:
					raise TypeError("no_format must be Boolean")
				if keyargs["no_format"]:
					Object.log_object.log_without_format(str(arg))
					needs_format = False

			if needs_format:
				Object.log_object.log(str(arg))

	# End logIfVerbose

	def logIfDryRun(self, arg):
		if Object.log_object and Object.global_dry_run and arg != None:
			Object.log_object.log(str(arg))

	# End logIfDryRun



# End Object
