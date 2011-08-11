#! /usr/bin/env python

import os
import re
import time
from slib.Objects import Object
from slib.SourceTrees import SourceTreeBaseObject, SourceTreeError
from slib.Commands.Shells import Shell
from slib.FileSystems import DIRECTORY
from slib.FileSystems.Directories import Directory

class CVSRepository(Object):
	"""The CVSRepository class."""

	# CVS repository strings have the following form:
	# [:method:][user[:password]@]hostname[:[port]]/path/to/repository

	def __init__(self, repository, **kwargs):
		Object.__init__(self, **kwargs)
		self.__repository = str(repository)

	# End __init__

	@property
	def method(self):
		# The method field always starts the repository string if it is present and will have the form:
		# :method:
		a = re.match(r':(.*?):',self.__repository)
		if a:
			return a.group(1)
		return None

	# End method
	

	@property
	def user(self):
		# The user field will always have the form [user[:password]@]hostname
		# Thus all the repository names with a user specification have to have a 
		# '@' character
		if not re.search(r'@',self.__repository):
			return None

		# This match catches the following case:
		# :method:user:password...
		a = re.match(r':.*?:([^@]*?):',self.__repository)
		if a:
			return a.group(1)
		
		# This match catches the following case:
		# :method:user@...
		a = re.match(r':.*?:(.*?)@',self.__repository)
		if a:
			return a.group(1)

		# This match catches the following case:
		# user:password@
		a = re.match(r'(.*?):.*?@', self.__repository)
		if a:
			return a.group(1)
		
		# This match catches the following case:
		# user@
		a = re.match(r'(.*?)@', self.__repository)
		if a:
			return a.group(1)

		return None

	# End user
	
	
	@property
	def password(self):
		# The password field is only present in the form: [user[:password]@]hostname
		# Thus if there is no '@' character, the repository string has no password field.
		if not re.search(r'@',self.__repository):
			return None

		# This match catches the following case:
		# :method:user:password@		
		a = re.match(r':.*?:.*?:(.*?)@',self.__repository)
		if a:
			return a.group(1)

		# This match catches the following case:
		# user:password@
		a = re.match(r'.*?:(.*?)@', self.__repository)
		if a:
			return a.group(1)

		return None

	# End password
	
	
	@property
	def hostname(self):
		# This search matches the following cases:
		# :method:user:password@hostname:
		# :method:user@hostname:
		# user:password@hostname:
		# user@hostname:
		a = re.search(r'@(.*?):',self.__repository)
		if a:
			return a.group(1)
			
		# This search matches the following case:
		# :method:hostname:port
		a = re.search(r':.*?:(.*?):\d{1,5}',self.__repository)
		if a:
			return a.group(1)
		
		# This search matches the following case:
		# hostname:port
		a = re.match(r'(.*?):\d{1,5}',self.__repository)
		if a:
			return a.group(1)
		
		# This search matches the following case:
		# :method:hostname:/path
		a = re.search(r':.*?:(.*?):\/.*',self.__repository)
		if a:
			return a.group(1)
		
		# This search matches the following case:
		# hostname:/path
		a = re.search(r'(.*?):\/.*', self.__repository)
		if a:
			return a.group(1)

		return None

	# End hostname
	
	
	@property
	def port(self):
		# This search matches the following cases:
		# :method:user:password@hostname:port
		# :method:user@hostname:port
		# user:password@hostname:port
		# user@hostname:port
		a = re.search(r'@.*?:(\d{1,5})',self.__repository)
		if a:
			return a.group(1)

		# This search matches the following case:
		# :method:hostname:port
		a = re.search(r':.*?:.*?:(\d{1,5})',self.__repository)
		if a:
			return a.group(1)

		# This search matches the following case:
		# hostname:port
		a = re.match(r'.*?:(\d{1,5})',self.__repository)
		if a:
			return a.group(1)

		return None

	# End port
	
	
	@property
	def path(self):
		# This search matches the following cases:
		# :method:user:password@hostname:port/path
		# :method:user@hostname:port/path
		# user:password@hostname:port/path
		# user@hostname:port/path
		a = re.search(r'@.*?:\d{1,5}(\/.*)',self.__repository)
		if a:
			return a.group(1)

		# This search matches the following cases:
		# :method:user:password@hostname:/path
		# :method:user@hostname:/path
		# user:password@hostname:/path
		# user@hostname:port/path
		a = re.search(r'@.*?:(\/.*)',self.__repository)
		if a:
			return a.group(1)

		# This search matches the following case:
		# :method:hostname:port/path
		a = re.search(r':.*?:.*?:\d{1,5}(\/.*)',self.__repository)
		if a:
			return a.group(1)

		# This search matches the following case:
		# :method:hostname:/path
		a = re.search(r':.*?:.*?:(\/.*)',self.__repository)
		if a:
			return a.group(1)

		# This search matches the following case:
		# hostname:port/path
		a = re.match(r'.*?:\d{1,5}(\/.*)',self.__repository)
		if a:
			return a.group(1)

		# This search matches the following case:
		# hostname:/path
		a = re.match(r'.*?:(\/.*)',self.__repository)
		if a:
			return a.group(1)

		return None

	# End path
	
	
	def __str__(self):
		return self.__repository

	# End __str__
	
	
	def __repr__(self):
		return self.__class__.__name__ + "(" + repr(self.__repository) + ")"

	# End __repr__
	

# End CVSRepository



class CVSFileData(Object):
	"""The CVSFileData class."""

	def __init__(self, name=None, ver=None, time=None, options=None, tag=None, modified=False, repository=None, filepath=None,**kwargs):
		Object.__init__(self,**kwargs)
		self.name = name
		self.version = ver
		self.time = time
		self.options = options
		self.tag = tag
		self.modified = modified
		self.repository = repository
		self.filepath = filepath
	# End __init__

	
	@property
	def fullpath(self):
		if self.filepath:
			return str(self.filepath) + "/" + str(self.name)
		else:
			return str(self.name)
	# End fullpath
	
	@property
	def cvslocation(self):
		if self.repository:
			return str(self.repository) + "/" + str(self.name)
		else:
			return str(self.name)
	# End cvslocation
	


	def __str__(self):
		return str(self.name)
	# End __str__
	
	def __repr__(self):
		rvalue = self.__class__.__name__ + "(" + repr(self.name) + ", " + repr(self.version) + ", "
		rvalue += repr(self.time) + ", " + repr(self.options) + ", "
		rvalue += repr(self.tag) + ", " + repr(self.modified) + "," 
		rvalue += repr(self.repository) + "," 
		rvalue += repr(self.filepath) + ")"
		return rvalue
	# End __repr__
		
# End CVSFileData


class CVSTreeData(Object):
	"""The CVSTreeData class."""

	month = {
		1  : "Jan",
		2  : "Feb",
		3  : "Mar",
		4  : "Apr",
		5  : "May",
		6  : "Jun",
		7  : "Jul",
		8  : "Aug",
		9  : "Sep",
		10 : "Oct",
		11 : "Nov",
		12 : "Dec"
	}

	day = {
		0 : "Mon",
		1 : "Tue",
		2 : "Wed",
		3 : "Thu",
		4 : "Fri",
		5 : "Sat",
		6 : "Sun"
	}


	def __init__(self, path, **kwargs):
		Object.__init__(self, **kwargs)
		self.path = path
		self.repository = None
		self.files = []
		self.directories = []
		self.__LoadCVSData()
		self.__filesIndex = -1 
		self.__filesLength = len(self.files)
	# End __init__


	def __NormalizeTimeComponent(self, value, normal):
		svalue = str(value)
		if len(svalue) < 2:
			svalue = normal + svalue
		return svalue
	# End __NormalizeTimeComponent
	

	def __PrepDate(self, path):
		statinfo = os.stat(path)
		lastaccesstime = time.gmtime(statinfo[8])
		newtime = self.day[lastaccesstime.tm_wday] + " " + self.month[lastaccesstime.tm_mon]
		newtime = newtime + " " + self.__NormalizeTimeComponent(lastaccesstime.tm_mday, " ")
		newtime = newtime + " " + self.__NormalizeTimeComponent(lastaccesstime.tm_hour, "0")
		newtime = newtime + ":" + self.__NormalizeTimeComponent(lastaccesstime.tm_min, "0")
		newtime = newtime + ":" + self.__NormalizeTimeComponent(lastaccesstime.tm_sec, "0")
		newtime = newtime + " " + str(lastaccesstime.tm_year)
		return newtime

	# End __PrepDate


	def __ParseData(self, path, entry, loglines):
		entrydata = entry.split('/')[1:]

		if re.search(r'^T', entrydata[4]):
			entrydata[4] = entrydata[4][1:-1]
		else:
			entrydata[4] = entrydata[4][:-1]

		quotedname = re.sub(r'([^A-Za-z_0-9])', r'\\\1', entrydata[0])
		
		if not os.path.exists(path + os.sep + entrydata[0]):
			return None

		cont = False

		for entry_log in loglines:
			if re.search(quotedname, entry_log):
				elog = entry_log.split(' ')[0]
				if elog == "R":
					return None

		modified = False
		if not os.path.isdir(path + "/" + entrydata[0]):
			newdate = self.__PrepDate(path + "/" + entrydata[0])

			if newdate != entrydata[2]:
				modified = True;

		
		return (entrydata[0], entrydata[1], entrydata[2], entrydata[3], entrydata[4], modified)

	# End __ParseData

	
	def __LoadFileData(self, path, data, loglines):
		result = self.__ParseData(path, data, loglines)
		if result == None:
			return

		self.files.append(CVSFileData(result[0],result[1],result[2],result[3],result[4],result[5],self.repository))
	# End __LoadFileData



	def __LoadTreeData(self, path, entry):
		entry = re.sub(r'^D(.*)', r'\1', entry)
		result = self.__ParseData(path, entry, [])
		if result == None:
			return
		self.directories.append(CVSTreeData(path + "/" + result[0]))
	# End __LoadTreeData
	

	def __LoadCVSData(self):
		if os.path.exists(self.path + "/CVS"):
			cvsdir = self.path + "/CVS"
			repofile = open(cvsdir + "/Repository")
			repodata = repofile.readlines()
			if len(repodata) > 1:
				raise BadRepositoryException()
			
			self.repository = repodata[0][:-1]
			
			entries_loglines = []

			if os.path.exists(cvsdir + "/Entries.log"):
				entries_logfile = open(cvsdir + "/Entries.log")
				entries_loglines = entries_logfile.readlines()

			entrieslines = []
			if os.path.exists(cvsdir + "/Entries"):
				entriesfile = open(cvsdir + "/Entries")
				entrieslines = entriesfile.readlines()
			
			for entry in entrieslines:
				if re.search(r'^D$',entry):
					continue
					
				if re.search(r'^\/', entry):
					self.__LoadFileData(self.path, entry, entries_loglines)
				elif re.search(r'^D',entry):
					self.__LoadTreeData(self.path, entry)

			for entry in entries_loglines:
				if re.search(r'^D$',entry):
					continue

				if not re.search(r'^A', entry):
					continue

				if re.search(r'^A \/.*', entry):
					newentry = re.sub(r'A (.*)', r'\1', entry)
					self.__LoadFileData(self.path, newentry, [])
				elif re.search(r'^A D(.*)', entry):
					newentry = re.sub(r'A D(.*)', r'\1', entry)
					self.__LoadTreeData(self.path, newentry)

	# End __LoadCVSData
		
	
	@property
	def all_files(self):
		files = []
		for f in self.files:
			f.filepath = self.path
			files.append(f)
		
		for d in self.directories:
			subfiles = d.all_files
			files.extend(subfiles)

		return files
	# End all_files	
	
	
	@property
	def modfiles(self):
		mods = []
		files = self.all_files
		for f in files:
			if f.modified:
				mods.append(f.fullpath)
		return mods
	# End modfiles
	
	
	@property
	def tags(self):
		tags = {}
		files = self.all_files
		for f in files:
			if f.tag:
				if not f.tag in tags:
					tags[f.tag] = 1
		
		return tags.keys()
	# End tags
	

	def __getitem__(self, key):
		foundobjs = []
		for f in self.files:
			if f.name == str(key):
				f.filepath = self.path
				foundobjs.append(f)
		
		for d in self.directories:
			objs = d[key]
			foundobjs.extend(objs)
		
		return foundobjs

	# End __getitem__


	def __iter__(self):
		self.__myfiles = self.all_files
		self.__myfilesIndex = 0
		return self
	# End __iter__
	
	
	def next(self):
		if self.__myfilesIndex == (len(self.__myfiles) - 1):
			raise StopIteration
		
		self.__myfilesIndex += 1
		return self.__myfiles[self.__myfilesIndex - 1]
	# End next
	


	def __str__(self):
		# return str(self.path)
		return str(self.files) + "\n" + str(self.path) + "\n" + str(self.directories)
	# End __str__
	

	def __repr__(self):
		return self.__class__.__name__ + "(" + repr(self.path)  + ")"
	# End __repr__
	
	

# End CVSTreeData


class CVSModulePath(Object):
	"""The CVSModulePath class."""

	def __init__(self, module):
		self.module = str(module)
	# End __init__

	@property
	def root(self):
		names = self.module.split(os.sep)
		return names[0]

	# End root
	

# End CVSModulePath



class CVSTree(SourceTreeBaseObject):
	"""The CVSTree class."""

	def __init__(self, repository, module, path, branch=None,  name=None, *args, **kwargs):
		SourceTreeBaseObject.__init__(self, repository, path, branch, args, **kwargs)
		self.__name = name
		self.__module = module
		self.__branch = branch
		
		if kwargs.has_key("date"):
			self.__date = kwargs["date"]
		else:
			self.__date = None

	# End __init__

	
	@property
	def name(self):
		if self.__name:
			return self.__name
		else:
			return self.__module
	# End name
	

	@property
	def branch(self):
		if not self.exists:
			return self.__branch

		cvstreedata = CVSTreeData(self.local_path.fullpath)
		
		tags = cvstreedata.tags

		if len(tags) == 0:
			return None
		else:
			return tags[0]

	# End branch
	


	@property
	def local_path(self):
		if self.path:
			if re.search(r'\/$', self.path):
				path = self.path[:-1]
			else:
				path = self.path
			directory = Directory(path + os.sep + self.name)
		else:
			directory = Directory(self.name)

		return directory

	# End local_path
	
	
	@property
	def date(self):
		return self.__date

	# End date
	

	@property
	def checkout_command(self):
		command = "cvs -d " + self.repository + " co"
		
		if self.__date:
			command += " -D " + self.__date
		
		if self.__name:
			command += " -d " + self.__name
		
		if self.branch:
			command += " -r " + self.branch
		
		command += " " + self.__module

		return command
	# End checkout_command
	
	
	@property
	def local_source_path(self):
		if self.__name:
			return self.__name
		else:
			return CVSModulePath(self.__module).root

	# End local_source_path
	
	

	def checkout(self):
		path = Directory(self.path)
		if not path.exists:
			path.create()
			
		currentDirectory = os.getcwd()
		
		try:
			Object.logIfDryRun(self,"cd " + path.fullpath)
			os.chdir(path.fullpath)
		except OSError as e:
			if not Object.global_dry_run:
				raise e

		self.shell.execute("rm -rf " + self.local_source_path)
		self.shell.execute(self.checkout_command)

		Object.logIfDryRun(self,"cd " + currentDirectory)
		os.chdir(currentDirectory)

	# End checkout


	@property
	def exists(self):
		return self.local_path.exists

	# End exists

	
	def update(self):
		if not Object.global_dry_run and not self.local_path.exists:
			return

		currentDirectory = os.getcwd()
		
		try:
			Object.logIfDryRun(self,"cd " + self.local_path.fullpath)
			os.chdir(self.local_path.fullpath)
		except OSError as e:
			if not Object.global_dry_run:
				raise e
		command = "cvs update -dP"

		self.shell.execute(command)
		
		Object.logIfDryRun(self,"cd " + currentDirectory)
		os.chdir(currentDirectory)

	# End update
	
	
	@property
	def root(self):
		cvsrepository = CVSRepository(self.repository)
		return cvsrepository.hostname + ":" + cvsrepository.path

	# End root
	
	
	def switch_to_branch(self, branch):
		if not Object.global_dry_run and not self.local_path.exists:
			return

		currentDirectory = os.getcwd()

		try:
			Object.logIfDryRun(self,"cd " + self.local_path.fullpath)
			os.chdir(self.local_path.fullpath)
		except OSError as e:
			if not Object.global_dry_run:
				raise e

		command = "cvs update "
		if str(branch) == "head":
			command += "-A"
		else:
			command += "-r " + str(branch)

		self.shell.execute(command)
		
		Object.logIfDryRun(self,currentDirectory)
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
		command = "cvs tag -b " + str(branch)

		self.shell.execute(command)
		
		Object.logIfDryRun(self,"cd " + currentDirectory)
		os.chdir(currentDirectory)

	# End make_new_branch
	

	def make_new_branch_and_switch(self, branch):
		self.make_new_branch(branch)
		self.switch_to_branch(branch)

	# End make_new_branch_and_switch
	

	# For CVS repositories, the branches method is problematic.  Branches are applied on a per/file basis
	# so getting a true list of all available branches requires traversing the tree and running cvs status -v
	# for every file encountered.  That of course means that this module has to query the CVS server for every
	# file in tree to retrieve the available branches.
	@property
	def branches(self):
		if not Object.global_dry_run and not self.local_path.exists:
			return []

		if Object.log_object:
			Object.log_object.log("Preparing branch information, this may take some time")

		branches = {}
		shell = Shell()
		for entry in self.local_path.all_entries:
			if not re.search(r'CVS', str(entry)) and not entry.type == DIRECTORY:
				currentDirectory = os.getcwd()

				try:
					Object.logIfDryRun(self,"cd " + entry.path)
					os.chdir(entry.path)
				except OSError as e:
					if not Object.global_dry_run:
						raise e

				shell.capture_output = True
				o = shell.execute("cvs status -v " + entry.name)
				data = o.split("\n")
				for line in data:
					if re.search(r'branch', line):
						a = re.search(r'\t(.*?) ',line)
						branch = a.group(1)
						if not branches.has_key(branch):
							branches[branch] = True
							
				Object.logIfDryRun(self,"cd " + currentDirectory)
				os.chdir(currentDirectory)
		return branches.keys()

	# End branches
	
	
	@property
	def tags(self):
		if not self.exists:
			return None

		cvstreedata = CVSTreeData(self.local_path.fullpath)

		tags = cvstreedata.tags

		if len(tags) == 0:
			return None
		else:
			return tags

	# End tags

	def remove(self):
		self.local_path.remove()

	# End remove

	def __repr__(self):
		
		text = self.__class__.__name__ + "(" + repr(self.repository) + "," + repr(self.__module) + "," + repr(self.path) + ","

		if self.branch != None:
			text += repr(self.branch)
		else:
			text += " " + str(None)
		
		if self.__name != None:
			text += "," + repr(self.__name)
		else:
			text += ", " + str(None)

		if len(self.args[0]) > 0:
			text += "," + repr(self.args)
		text += ")"
		return text			

	# End __repr__

# End CVSTree


def CVSTreeArgs(tree_data):
	if len(tree_data.tags) > 0:
		tag = tree_data.tags[0]
	else:
		tag = None
	
	repository = "cvs.wolfram.com:/cvs"
	module = tree_data.repository
	
	full_path = Directory(tree_data.path)

	if re.search(tree_data.repository, tree_data.path):
		path_parts = tree_data.path.split(tree_data.repository)
		local_path = path_parts[0]
		name = None
	else:
		full_path = Directory(tree_data.path)
		local_path = str(full_path.parent)
		name = full_path.name
		

	
	return (repository, module, local_path, tag, name)

# End CVSTreeArgs


def ConvertPathToCVSTree(path):
	tree_data = CVSTreeData(path)
	args = CVSTreeArgs(tree_data)
	return CVSTree(*args)

# End ConvertPathToCVSTree

