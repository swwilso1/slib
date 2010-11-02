#! /usr/bin/env python

import re
import sys
import types
import slib.Objects
import slib.Errors
import slib.FileSystems.Directories

class BuildSystemError(slib.Errors.Error):
	"""The BuildSystemError class."""

	def __init__(self, value):
		slib.Errors.Error.__init__(self,value)

	# End __init__

# End BuildSystemError


class BuildSystemBaseObject(slib.Objects.Object):
	"""The BuildSystemBaseObject class."""

	def __init__(self, working_directory, source_tree_directory, build_parameters = None):
		slib.Objects.Object.__init__(self)
		self.working_directory = slib.FileSystems.Directories.Directory(working_directory)
		self.source_tree_directory = slib.FileSystems.Directories.Directory(source_tree_directory)
		if build_parameters:
			if type(build_parameters) != types.DictType:
				raise slib.Errors.ArgumentError("Third argument must be a dictionary")
			self._build_parameters = build_parameters
		else:
			self._build_parameters = {}

	# End __init__


	def configure(self):
		pass

	# End configure
	


	def build(self,target=None):
		pass

	# End build
	
	def install(self):
		pass

	# End install
	
	
	def remove(self):
		pass

	# End remove

	
	@property
	def build_command(self):
		if re.search(r'win32', sys.platform):
			return "nmake"
		else:
			return "make"

	# End build_command
	
	
	
	def __contains__(self, obj):
		return self.has_key(obj)

	# End __contains__
	
	
	def __getitem__(self, key):
		return self._build_parameters[key]

	# End __getitem__
	
	
	def __setitem__(self, key, value):
		self._build_parameters[key] = value
	
	# End __setitem__
	

	def has_key(self, key):
		return self._build_parameters.has_key(key)

	# End has_key
	

	def __str__(self):
		pass

	# End __str__
	
	
	def __repr__(self):
		text =  self.__class__.__name__ + "('" + str(self.working_directory) + "', '" + str(self.source_tree_directory) + "'"
		if len(self._build_parameters.keys()) > 0:
			text += ", " + repr(self._build_parameters)
		
		text += ")"
		
		return text
		

	# End __repr__
	

# End BuildSystemBaseObject

