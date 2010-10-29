#! /usr/bin/env python

import sys
import os
import re
import time
import stat
import slib.Objects
import slib.Errors
import slib.FileSystems
import slib.Commands.Shells

def FindFullDirectory(directory):
	currentdirectory = os.getcwd()
	if re.search(r'^\.\/', directory):
		parts = directory.split("./")
		newdirectory = currentdirectory + "/" + parts[1]
		return newdirectory
	if re.search(r'^[^\/]', directory):
		newdirectory = currentdirectory + "/" + directory
		return newdirectory
	return directory
# End FindFullDirectory


class FileSystemException(slib.Errors.Error):
	"""The FileSystemException class."""

	def __init__(self, value):
		slib.Errors.Error.__init__(self,value)
	# End __init__

# End FSObjectException



DIRECTORY = 1
CHARACTER_DEVICE = 2
BLOCK_DEVICE = 3
REGULAR_FILE = 4
FIFO = 5
SYMBOLIC_LINK = 6
SOCKET = 7
NO_TYPE = 99

class FileSystemBaseObject(slib.Objects.Object):
	"""The FileSystemBaseObject class."""
	
	def __init__(self, name, path=None):
		slib.Objects.Object.__init__(self)
		if name.count(os.path.sep) > 0:
			directory = os.path.dirname(name)
			basename = os.path.basename(name)
			self.name = basename
			if path:
				self._path = directory + os.path.sep + path
			else:
				self._path = directory
		else:
			self.name = name
			self._path = path
	# End __init__

	@property
	def path(self):
		if self._path:
			return self._path
		return "."
	# End path
	
			
	@property
	def fullpath(self):
		if re.match(r'^/$', self.path):
			return self.path + self.name
		else:
			return self.path + os.path.sep + self.name
	# End fullpath

	@property
	def st_mode(self):
		fsdata = os.stat(self.fullpath)
		return fsdata.st_mode
	# End st_mode
	
	@property
	def st_ino(self):
		fsdata = os.stat(self.fullpath)
		return fsdata.st_ino
	# End st_ino

	@property
	def st_dev(self):
		fsdata = os.stat(self.fullpath)
		return fsdata.st_dev
	# End st_dev
	
	@property
	def st_nlink(self):
		fsdata = os.stat(self.fullpath)
		return fsdata.st_nlink
	# End st_nlink

	@property
	def st_uid(self):
		fsdata = os.stat(self.fullpath)
		return fsdata.st_uid
	# End st_uid

	@property
	def st_gid(self):
		fsdata = os.stat(self.fullpath)
		return fsdata.st_gid
	# End st_gid

	@property
	def st_size(self):
		fsdata = os.stat(self.fullpath)
		return fsdata.st_size
	# End st_size

	@property
	def st_atime(self):
		fsdata = os.stat(self.fullpath)
		return fsdata.st_atime
	# End st_atime

	@property
	def st_mtime(self):
		fsdata = os.stat(self.fullpath)
		return fsdata.st_mtime
	# End st_ino

	@property
	def st_ctime(self):
		fsdata = os.stat(self.fullpath)
		return fsdata.st_ctime
	# End st_ctime

	@property
	def directory(self):
		return stat.S_ISDIR(self.st_mode)
	# End directory

	@property
	def characterSpecialDevice(self):
		return stat.S_ISCHR(self.st_mode)
	# End characterSpecialDevice
	
	@property
	def blockSpecialDevice(self):
		return stat.S_ISBLK(self.st_mode)
	# End blockSpecialDevice
	
	@property
	def regular(self):
		return stat.S_ISREG(self.st_mode)
	# End regular

	@property
	def fifo(self):
		return stat.S_ISFIFO(self.st_mode)
	# End fifo
	
	@property
	def symbolicLink(self):
		return stat.S_ISLNK(self.st_mode)
	# End symbolicLink

	@property
	def socket(self):
		return stat.S_ISSOCK(self.st_mode)
	# End socket
	
	@property
	def type(self):
		if self.directory:
			return DIRECTORY
		if self.characterSpecialDevice:
			return CHARACTER_DEVICE
		if self.blockSpecialDevice:
			return BLOCK_DEVICE
		if self.regular:
			return REGULAR_FILE
		if self.fifo:
			return FIFO
		if self.symbolicLink:
			return SYMBOLIC_LINK
		if self.socket:
			return SOCKET
		return NO_TYPE
	# End type

	@property
	def exists(self):
		return os.path.exists(self.fullpath)
	# End exists

	@property
	def ownerHasReadPermission(self):
		if stat.S_IMODE(self.st_mode) & stat.S_IRUSR:
			return True
		return False
	# End ownerHasReadPermission
	
	@property
	def ownerHasWritePermission(self):
		if stat.S_IMODE(self.st_mode) & stat.S_IWUSR:
			return True
		return False
	# End ownerHasWritePermission

	@property
	def ownerHasExecutePermission(self):
		if stat.S_IMODE(self.st_mode) & stat.S_IXUSR:
			return True
		return False
	# End ownerHasExecutePermission
	
	@property
	def groupReadPermission(self):
		if stat.S_IMODE(self.st_mode) & stat.S_IRGRP:
			return True
		return False
	# End groupReadPermission

	@property
	def groupWritePermission(self):
		if stat.S_IMODE(self.st_mode) & stat.S_IWGRP:
			return True
		return False
	# End groupWritePermission

	@property
	def groupExecutePermission(self):
		if stat.S_IMODE(self.st_mode) & stat.S_IXGRP:
			return True
		return False
	# End groupExecutePermission

	@property
	def otherReadPermission(self):
		if stat.S_IMODE(self.st_mode) & stat.S_IROTH:
			return True
		return False
	# End otherReadPermission

	@property
	def otherWritePermission(self):
		if stat.S_IMODE(self.st_mode) & stat.S_IWOTH:
			return True
		return False
	# End otherWritePermission

	@property
	def otherExecutePermission(self):
		if stat.S_IMODE(self.st_mode) & stat.S_IXOTH:
			return True
		return False
	# End otherExecutePermission
	

	@property
	def canRead(self):
		if os.getuid() == self.st_uid and self.ownerHasReadPermission:
			return True
		if os.getgid() == self.st_gid and self.groupReadPermission:
			return True
		if self.otherReadPermission:
			return True
		return False
	# End canRead
	
	@property
	def canWrite(self):
		if os.getuid() == self.st_uid and self.ownerHasWritePermission:
			return True
		if os.getgid() == self.st_gid and self.groupWritePermission:
			return True
		if self.otherWritePermission:
			return True
		return False
	# End canWrite
	
	@property
	def canExecute(self):
		if os.getuid() == self.st_uid and self.ownerHasExecutePermission:
			return True
		if os.getgid() == self.st_gid and self.groupExecutePermission:
			return True
		if self.otherExecutePermission:
			return True
		return False
	# End canExecute
	
	
	def Difference(self,other):
		if not type(other) == FileSystemBaseObject:
			raise FileSystemException("%s not a FileSystemBaseObject" % (str(other)))
		shell = slib.Commands.Shells.Shell()
		shell.captureOutput = True
		o = shell.execute("diff " + self.fullpath + " " + other.fullpath)
		return o
	# End Difference
	

	def ContentsSameQ(self,other):
		if not type(other) == FileSystemBaseObject:
			raise FileSystemException("%s not a FileSystemBaseObject" % (str(other)))
		shell = slib.Commands.Shells.Shell()
		shell.captureOutput = True
		try:
			o = shell.execute("diff " + self.fullpath + " " + other.fullpath)
		except libs.Commands.CommandError, e:
			return False
		return True

	# End ContentsSameQ
	
	def ContentsDifferentQ(self,other):
		if not self.ContentsSameQ(other):
			return True
		return False
	# End ContentsDifferentQ
	
	def __eq__(self, other):
		if not type(self) == type(other):
			return False
		if self.name == other.name and self.path == other.path:
			return True
		return False
	# End __eq__
	
	
	def __str__(self):
		return self.fullpath
	# End __str__
	
	def __repr__(self):
		if self.path != ".":
			return self.__class__.__name__ + "(" + self.name + "," + self.path + ")"
		else:
			return self.__class__.__name__ + "(" + self.name + ")"
	# End __repr__

# End FileSystemBaseObject


def ContentsSameQ(a,b):
	if not type(a) == type(b):
		return False

	if a.ContentsSameQ(b):
		return True
	return False
# End ContentsSameQ

def ContentsDifferentQ(a,b):
	if not ContentsSameQ(a,b):
		return True
	return False
# End ContentsDifferentQ

def Difference(a,b):
	return a.Difference(b)
# End Difference





