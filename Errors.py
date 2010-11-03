#! /usr/bin/env python

from slib.Objects import Object
import exceptions


class Error(Object,exceptions.Exception):
	"""The Error class."""

	def __init__(self, value):
		Object.__init__(self)
		self.note = value
	# End __init__


	def __str__(self):
		return "%s: %s" % (self.__class__.__name__, self.note)
	# End __str__
	
	
	def __repr__(self):
		return "%s(%s)" % (self.__class__.__name__, str(self.note))
	# End __repr__
	
	
# End Error


class ArgumentError(Error):
	"""The ArgumentError class."""

	def __init__(self, value):
		Error.__init__(self,value)

	# End __init__

# End ArgumentError

