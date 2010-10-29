#! /usr/bin/env python

import os
import re
import slib.SourceTrees
import slib.FileSystems.Directories

class GitTree(slib.SourceTrees.SourceTreeBaseObject):
	"""The GitTree class."""

	def __init__(self, repository, path, branch=None,  name=None, *args):
		slib.SourceTrees.SourceTreeBaseObject.__init__(self, repository, path, branch, args)
		self.__name = name
	# End __init__

	
	@property
	def name(self):
		if self.__name:
			return str(self.__name)
		else:
			if re.search(r':', self.repository):
				if re.match(r'://', self.repository):
					repository_directory = slib.FileSystems.Directories.Directory(self.repository.split("://")[1])
				else:
					repository_directory = slib.FileSystems.Directories.Directory(self.repository.split(":")[1])
				
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
			directory = slib.FileSystems.Directories.Directory(self.name, self.path)
		else:
			directory = slib.FileSystems.Directories.Directory(self.name, ".")

		return directory

	# End local_path
	
	
	def checkout(self):
		localParentDir = self.local_path.parent

		if not localParentDir.exists:
			os.makedirs(localParentDir.fullpath)

		currentDirectory = os.getcwd()
		os.chdir(localParentDir.fullpath)

		if self.local_path.exists:
			slib.FileSystems.Directories.RemoveDirectory(self.local_path.fullpath)

		command = "git clone " + self.repository + " " + self.name

		self.shell.execute(command)

		if self.branch != "master":
			os.chdir(self.local_path.fullpath)
			command = "git checkout -b " + self.branch + " origin/" + self.branch
			self.shell.execute(command)
		
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


	def switchToBranch(self,branch):
		if self.local_path.exists:
			currentDirectory = os.getcwd()
			os.chdir(self.local_path.fullpath)

			# First try just checkout out the branch:
			command = "git checkout " + str(branch)
			try:
				self.shell.execute(command)
			except slib.Commands.CommandError, e:
				# Instead try getting the branch from the origin:
				command = "git checkout -b " + str(branch) + " origin/" + str(branch)
				self.shell.execute(command)

			self.__branch = str(branch)
			os.chdir(currentDirectory)

	# End switchToBranch
	

	def makeNewBranch(self,branch):
		if self.local_path.exists:
			currentDirectory = os.getcwd()
			os.chdir(self.local_path.fullpath)
			
			command = "git branch " + str(branch)
			self.shell.execute(command)
			os.chdir(currentDirectory)

	# End makeNewBranch


	def makeNewBranchAndSwitch(self, branch):
		if self.local_path.exists:
			currentDirectory = os.getcwd()
			os.chdir(self.local_path.fullpath)
			
			command = "git checkout -b " + str(branch)
			self.shell.execute(command)
			self.__branch = str(branch)
			os.chdir(currentDirectory)

	# End makeNewBranchAndSwitch


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
			self.shell.captureOutput = True
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
			self.shell.captureOutput = True
			o = self.shell.execute(command)
			os.chdir(currentDirectory)
			for branch in o.split('\n'):
				if re.match(r'^\*',branch):
					return self.__massageBranchName(branch)
		return None

	# End branch


	def makeNewBranchFromRemote(self,branch,remote):
		if self.local_path.exists:
			currentDirectory = os.getcwd()
			os.chdir(self.local_path.fullpath)
			
			command = "git branch " + str(branch) + " " + str(remote) + "/" + str(branch)
			self.shell.execute(command)
			os.chdir(currentDirectory)

	# End makeNewBranchFromRemote

	
	def makeNewBranchFromRemoteAndSwitch(self,branch,remote):
		if self.local_path.exists:
			currentDirectory = os.getcwd()
			os.chdir(self.local_path.fullpath)
			
			command = "git checkout -b " + str(branch) + " " + str(remote) + "/" + str(branch)
			self.shell.execute(command)
			self.__branch = str(branch)
			os.chdir(currentDirectory)

	# End makeNewBranchFromRemoteAndSwitch
	

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


