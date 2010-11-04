#! /usr/bin/env python

import os
import re
from slib.Commands import CommandError
from slib.SourceTrees import SourceTreeBaseObject, SourceTreeError
from slib.FileSystems.Directories import Directory

class GitTree(SourceTreeBaseObject):
	"""The GitTree class."""

	def __init__(self, repository, path, branch=None,  name=None, *args):
		SourceTreeBaseObject.__init__(self, repository, path, branch, args)
		self.__name = name
	# End __init__

	
	@property
	def name(self):
		if self.__name:
			return str(self.__name)
		else:
			if re.search(r':', self.repository):
				if re.match(r'://', self.repository):
					repository_directory = Directory(self.repository.split("://")[1])
				else:
					repository_directory = Directory(self.repository.split(":")[1])
				
				if re.search(r'\.', repository_directory.name):
					return repository_directory.name.split(".")[0]
				else:
					return repository_directory.name
			else:
				return os.path.basename(self.repository)

	# End name	

	
	@property
	def local_path(self):
		if self.path:
			directory = Directory(self.name, self.path)
		else:
			directory = Directory(self.name, ".")

		return directory

	# End local_path
	
	
	def checkout(self):
		self.local_path.parent.create()

		currentDirectory = os.getcwd()
		os.chdir(self.local_path.parent.fullpath)

		self.local_path.remove()

		command = "git clone " + self.repository + " " + self.name

		self.shell.execute(command)
		
		if self.branch != "master":
			os.chdir(self.local_path.fullpath)
			command = "git checkout -b " + self.branch + " origin/" + self.branch
			try:
				self.shell.execute(command)
			except CommandError, e:
				print "Unable to switch to branch %s: %s" % (self.branch, e)

		os.chdir(currentDirectory)

	# End checkout
	

	@property
	def exists(self):
		return self.local_path.exists
	# End exists


	def update(self):
		if self.exists:
			currentDirectory = os.getcwd()
			os.chdir(self.local_path.fullpath)
			command = "git pull origin"
			self.shell.execute(command)
			os.chdir(currentDirectory)
		
	# End update


	def switch_to_branch(self,branch):
		if self.local_path.exists:
			currentDirectory = os.getcwd()
			os.chdir(self.local_path.fullpath)

			# First try just checkout out the branch:
			command = "git checkout " + str(branch)
			try:
				self.shell.execute(command)
			except CommandError, e:
				# Instead try getting the branch from the origin:
				command = "git checkout -b " + str(branch) + " origin/" + str(branch)
				self.shell.execute(command)

			self.__branch = str(branch)
			os.chdir(currentDirectory)

	# End switch_to_branch
	

	def make_new_branch(self,branch):
		if self.local_path.exists:
			currentDirectory = os.getcwd()
			os.chdir(self.local_path.fullpath)
			
			command = "git branch " + str(branch)
			self.shell.execute(command)
			os.chdir(currentDirectory)

	# End make_new_branch


	def make_new_branch_and_switch(self, branch):
		if self.local_path.exists:
			currentDirectory = os.getcwd()
			os.chdir(self.local_path.fullpath)
			
			command = "git checkout -b " + str(branch)
			self.shell.execute(command)
			self.__branch = str(branch)
			os.chdir(currentDirectory)

	# End make_new_branch_and_switch


	def __massageBranchName(self,name):
		name = re.sub(r' ',r'',name)
		name = re.sub(r'\*',r'',name)
		name = re.sub(r'->.*',r'',name)
		return name

	# End __massageBranchName
	


	@property
	def branches(self):
		if self.local_path.exists:
			currentDirectory = os.getcwd()
			os.chdir(self.local_path.fullpath)
			
			command = "git branch -a"
			if not self.shell.capture_output:
				self.shell.capture_output = True
			o = self.shell.execute(command)
			os.chdir(currentDirectory)
			branches = [ self.__massageBranchName(branch) for branch in o.split('\n') ]
			return branches
		return []

	# End branches


	@property
	def branch(self):
		if self.local_path.exists:
			currentDirectory = os.getcwd()
			os.chdir(self.local_path.fullpath)
			
			command = "git branch"
			if not self.shell.capture_output:
				self.shell.capture_output = True
			o = self.shell.execute(command)
			os.chdir(currentDirectory)
			for branch in o.split('\n'):
				if re.match(r'^\*',branch):
					return self.__massageBranchName(branch)
		return None

	# End branch


	def make_new_branch_from_remote(self,branch,remote):
		if self.local_path.exists:
			currentDirectory = os.getcwd()
			os.chdir(self.local_path.fullpath)
			
			command = "git branch " + str(branch) + " " + str(remote) + "/" + str(branch)
			self.shell.execute(command)
			os.chdir(currentDirectory)

	# End make_new_branch_from_remote

	
	def make_new_branch_from_remote_and_switch(self,branch,remote="origin"):
		if self.local_path.exists:
			currentDirectory = os.getcwd()
			os.chdir(self.local_path.fullpath)
			
			command = "git checkout -b " + str(branch) + " " + str(remote) + "/" + str(branch)
			self.shell.execute(command)
			self.__branch = str(branch)
			os.chdir(currentDirectory)

	# End make_new_branch_from_remote_and_switch
	

	@property
	def tags(self):
		if self.local_path.exists:
			currentDirectory = os.getcwd()
			os.chdir(self.local_path.fullpath)
		
			command = "git tag"
			if not self.shell.capture_output:
				self.shell.capture_output = True
			o = self.shell.execute(command)
			os.chdir(currentDirectory)
			tags = [ tag for tag in o.split('\n') ]
			return tags
		return []

	# End tags


	def remove(self):
		self.local_path.remove()

	# End remove


	def __repr__(self):
		
		text = self.__class__.__name__ + "(" + repr(self.repository) + "," + repr(self.path) + ","
		if self.branch != None:
			text += repr(self.branch)
		else:
			text += " " + str(None)
		
		if self.name != None:
			text += "," + repr(self.name)
		else:
			text += ", " + str(None)

		if len(self.args[0]) > 0:
			text += "," + repr(self.args)
		text += ")"
		return text			

	# End __repr__
	
# End GitTree


