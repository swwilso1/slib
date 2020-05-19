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

import sys
import os
import re
from .. Objects import Object
from .. Commands import CommandError
from .. SourceTrees import SourceTreeBaseObject, SourceTreeError
from .. FileSystems.Directories import Directory
from .. Commands.Shells import Shell

class GitTree(SourceTreeBaseObject):
	"""The GitTree class."""

	def __init__(self, repository, path, branch=None,  name=None, *args, **kwargs):
		SourceTreeBaseObject.__init__(self, repository, path, branch, args, **kwargs)
		self.__name = name
	# End __init__


	@property
	def name(self):
		if self.__name:
			return str(self.__name)
		else:
			if re.search(r'.*\/.*\.git$', self.repository):
				self.__name = re.sub(r'.*\/(.*)\.git$',r'\1',self.repository)
				return self.__name

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
			directory = Directory(self.path + os.sep + self.name)
		else:
			directory = Directory(self.name)

		return directory

	# End local_path


	def checkout(self):
		if not self.local_path.parent.exists:
			self.local_path.parent.create()

		currentDirectory = os.getcwd()

		try:
			Object.logIfDryRun(self,"cd " + self.local_path.parent.fullpath)
			os.chdir(self.local_path.parent.fullpath)
		except OSError as e:
			if not Object.global_dry_run:
				raise e

		self.local_path.remove()

		orig_branch = self.branch

		command = "git clone " + self.repository + " " + self.name

		self.shell.execute(command)

		if orig_branch != "master" and orig_branch != None:
			try:
				Object.logIfDryRun(self,"cd " + self.local_path.fullpath)
				os.chdir(self.local_path.fullpath)
			except OSError as e:
				if not Object.global_dry_run:
					raise e
			command = "git checkout -b " + orig_branch + " origin/" + orig_branch
			try:
				self.shell.execute(command)
			except CommandError as e:
				print("Unable to switch to branch %s: %s" % (self.branch, e))

		Object.logIfDryRun(self,"cd " + currentDirectory)
		os.chdir(currentDirectory)

	# End checkout


	@property
	def exists(self):
		return self.local_path.exists
	# End exists


	def update(self, useRebase=False):
		if not Object.global_dry_run and not self.local_path.exists:
			return

		currentDirectory = os.getcwd()
		try:
			Object.logIfDryRun(self,"cd " + self.local_path.fullpath)
			os.chdir(self.local_path.fullpath)
		except OSError as e:
			if not Object.global_dry_run:
				raise e

		command = "git pull origin"

		if useRebase:
			command += " --rebase"

		# Get the current branch
		branch = self.branch

		if branch:
			command += " " + branch

		self.shell.execute(command)

		Object.logIfDryRun(self,"cd " + currentDirectory)
		os.chdir(currentDirectory)

	# End update


	def switch_to_branch(self,branch):
		if not Object.global_dry_run and not self.local_path.exists:
			return

		currentDirectory = os.getcwd()

		try:
			Object.logIfDryRun(self,"cd " + self.local_path.fullpath)
			os.chdir(self.local_path.fullpath)
		except OSError as e:
			if not Object.global_dry_run:
				raise e

		# First try just checkout out the branch:
		command = "git checkout " + str(branch)
		try:
			self.shell.execute(command)
		except CommandError as e:
			# Instead try getting the branch from the origin:
			command = "git checkout -b " + str(branch) + " origin/" + str(branch)
			self.shell.execute(command)

		self.__branch = str(branch)

		Object.logIfDryRun(self,"cd " + currentDirectory)
		os.chdir(currentDirectory)

	# End switch_to_branch


	def make_new_branch(self,branch):
		if not Object.global_dry_run and not self.local_path.exists:
			return

		currentDirectory = os.getcwd()

		try:
			Object.logIfDryRun(self,"cd " + self.local_path.fullpath)
			os.chdir(self.local_path.fullpath)
		except OSError as e:
			if not Object.global_dry_run:
				raise e

		command = "git branch " + str(branch)

		self.shell.execute(command)

		Object.logIfDryRun(self,"cd " + currentDirectory)
		os.chdir(currentDirectory)

	# End make_new_branch


	def make_new_branch_and_switch(self, branch):
		if not Object.global_dry_run and not self.local_path.exists:
			return

		currentDirectory = os.getcwd()

		try:
			Object.logIfDryRun(self,"cd " + self.local_path.fullpath)
			os.chdir(self.local_path.fullpath)
		except OSError as e:
			if not Object.global_dry_run:
				raise e

		command = "git checkout -b " + str(branch)
		self.shell.execute(command)

		self.__branch = str(branch)

		Object.logIfDryRun(self,"cd " + currentDirectory)
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
		if not Object.global_dry_run and not self.local_path.exists:
			return []

		currentDirectory = os.getcwd()

		try:
			Object.logIfDryRun(self,"cd " + self.local_path.fullpath)
			os.chdir(self.local_path.fullpath)
		except OSError as e:
			if not Object.global_dry_run:
				raise e

		command = "git branch -a"
		if not self.shell.capture_output:
			self.shell.capture_output = True

		o = self.shell.execute(command)

		Object.logIfDryRun(self,"cd " + currentDirectory)
		os.chdir(currentDirectory)
		branches = [ self.__massageBranchName(branch) for branch in o.split('\n') ]
		return [ branch for branch in branches if len(branch) > 0 ]

	# End branches


	@property
	def branch(self):
		if not Object.global_dry_run and not self.local_path.exists:
			return None

		currentDirectory = os.getcwd()

		try:
			Object.logIfDryRun(self,"cd " + self.local_path.fullpath)
			os.chdir(self.local_path.fullpath)
		except OSError as e:
			if not Object.global_dry_run:
				raise e

		command = "git branch"
		if not self.shell.capture_output:
			self.shell.capture_output = True

		o = self.shell.execute(command)

		Object.logIfDryRun(self,"cd " + currentDirectory)
		os.chdir(currentDirectory)
		if o:
			for branch in o.split('\n'):
				if re.match(r'^\*',branch):
					return self.__massageBranchName(branch)
		return None

	# End branch


	def make_new_branch_from_remote(self,branch,remote):
		if not Object.global_dry_run and not self.local_path.exists:
			return

		currentDirectory = os.getcwd()

		try:
			Object.logIfDryRun(self,"cd " + self.local_path.fullpath)
			os.chdir(self.local_path.fullpath)
		except OSError as e:
			if not Object.global_dry_run:
				raise e

		command = "git branch " + str(branch) + " " + str(remote) + "/" + str(branch)

		self.shell.execute(command)

		Object.logIfDryRun(self,"cd " + currentDirectory)
		os.chdir(currentDirectory)

	# End make_new_branch_from_remote


	def make_new_branch_from_remote_and_switch(self,branch,remote="origin"):
		if not Object.global_dry_run and not self.local_path.exists:
			return

		currentDirectory = os.getcwd()

		try:
			Object.logIfDryRun(self,"cd " + self.local_path.fullpath)
			os.chdir(self.local_path.fullpath)
		except OSError as e:
			if not Object.global_dry_run:
				raise e

		command = "git checkout -b " + str(branch) + " " + str(remote) + "/" + str(branch)
		self.shell.execute(command)

		self.__branch = str(branch)

		Object.logIfDryRun(self,"cd " + currentDirectory)
		os.chdir(currentDirectory)

	# End make_new_branch_from_remote_and_switch


	@property
	def tags(self):
		if not Object.global_dry_run and not self.local_path.exists:
			return []

		currentDirectory = os.getcwd()

		try:
			Object.logIfDryRun(self,"cd " + self.local_path.fullpath)
			os.chdir(self.local_path.fullpath)
		except OSError as e:
			if not Object.global_dry_run:
				raise e

		command = "git tag"
		if not self.shell.capture_output:
			self.shell.capture_output = True

		o = self.shell.execute(command)

		Object.logIfDryRun(self,"cd " + currentDirectory)
		os.chdir(currentDirectory)
		tags = [ tag for tag in o.split('\n') ]
		return [ tag for tag in tags if len(tag) > 0 ]

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


def ConvertPathToGITTree(path):
	currentDirectory = os.getcwd()
	os.chdir(str(path))
	shell = Shell()
	shell.capture_output = True
	# Calculate the repository
	command = 'git remote -v | grep origin | grep fetch'
	output = shell.execute(command)
	name_repo = output.split(' ')[0]
	repository = name_repo.split('\t')[1]

	# Calculate the branch
	command = 'git branch'
	output = shell.execute(command)
	branch = output.split(' ')[1]

	os.chdir(currentDirectory)

	# Calculate the path
	thePath = os.path.dirname(str(path))

	# Calculate the name
	name = os.path.basename(str(path))

	return GitTree(repository, thePath, branch, name)

# End ConvertPathToGITTree


