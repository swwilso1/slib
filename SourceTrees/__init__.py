#! /usr/bin/env python

import slib.Objects
import slib.Errors
import slib.Commands.Shells

class SourceTreeError(slib.Errors.Error):
	"""The SourceTreeError class."""

	def __init__(self, value):
		slib.Errors.Error.__init__(self,value)

	# End __init__

# End SourceTreeError


class SourceTreeBaseObject(slib.Objects.Object):
	"""The SourceTreeBaseObject class."""

	def __init__(self, repository, path, branch=None, *args):
		slib.Objects.Object.__init__(self)
		self.repository = str(repository)
		if branch:
			self.__branch = str(branch)
		else:
			self.__branch = branch

		self.path = str(path)
		self.shell = slib.Commands.Shells.Shell()
		self.args = args

	# End __init__

	@property
	def branch(arg):
		return self.__branch

	# End branch
	


	@property
	def local_path(self):
		pass

	# End local_path
	


	def checkout(self):
		pass

	# End checkout


	@property
	def exists(self):
		pass

	# End exists

	
	def update(self):
		pass

	# End update
	
	
	@property
	def root(self):
		return self.repository

	# End root
	
	
	def switchToBranch(self, branch):
		pass

	# End switchToBranch
	

	def makeNewBranch(self,branch):
		pass

	# End makeNewBranch
	

	def makeNewBranchAndSwitch(self, branch):
		pass

	# End makeNewBranchAndSwitch
	

	@property
	def branches(self):
		pass

	# End branches
	
	
	@property
	def tags(self):
		pass

	# End tags

	def remove(self):
		pass

	# End remove
	
	

	def __str__(self):
		return str(self.local_path)

	# End __str__
	
	
	def __repr__(self):
		
		text = self.__class__.__name__ + "(" + repr(self.repository) + "," + repr(self.path) + ","
		if self.branch != None:
			text += repr(self.branch)
		else:
			text += " " + str(None)

		if len(self.args[0]) > 0:
			text += "," + repr(self.args)
		text += ")"
		return text			

	# End __repr__
	

# End SourceTreeBaseObject
