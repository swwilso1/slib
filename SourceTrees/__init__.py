#! /usr/bin/env python

from slib.Objects import Object
from slib.Errors import Error
from slib.Commands.Shells import Shell

__all__ = ["CVS", "Git", "Mercurial"]

class SourceTreeError(Error):
	"""The SourceTreeError class."""

	def __init__(self, value, **kwargs):
		Error.__init__(self,value,**kwargs)

	# End __init__

# End SourceTreeError


class SourceTreeBaseObject(Object):
	"""The SourceTreeBaseObject class."""

	def __init__(self, repository, path, branch=None, *args, **kwargs):
		Object.__init__(self, **kwargs)
		self.repository = str(repository)
		if branch:
			self.__branch = str(branch)
		else:
			self.__branch = branch

		self.path = str(path)
		self.shell = Shell()
		self.shell.capture_output = True

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


	def switch_to_branch(self, branch):
		pass

	# End switch_to_branch


	def make_new_branch(self,branch):
		pass

	# End make_new_branch


	def make_new_branch_and_switch(self, branch):
		pass

	# End make_new_branch_and_switch


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


import CVS
import Git
import Mercurial
