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
import time
import stat
import types
import hashlib

from slib.Objects import Object
from slib.Errors import Error
from slib.Commands.Shells import Shell
from slib.Commands import CommandError


DIRECTORY = 1
CHARACTER_DEVICE = 2
BLOCK_DEVICE = 3
REGULAR_FILE = 4
FIFO = 5
SYMBOLIC_LINK = 6
SOCKET = 7
NO_TYPE = 99

USER_READ     = 0x1
USER_WRITE    = 0x2
USER_EXECUTE  = 0x4
GROUP_READ    = 0x8
GROUP_READ    = 0x10
GROUP_WRITE   = 0x20
GROUP_EXECUTE = 0x40
OTHER_READ    = 0x80
OTHER_WRITE   = 0x100
OTHER_EXECUTE = 0x200
SETUID        = 0x400
SETGID        = 0x800
STICKYBIT     = 0x1000


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


class FileSystemError(Error):
	"""The FileSystemError class."""

	def __init__(self, value, **kwargs):
		Error.__init__(self,value, **kwargs)
	# End __init__

# End FSObjectException


class FileSystemBaseObject(Object):
	"""The FileSystemBaseObject class."""

	def __init__(self, name, **kwargs):
		Object.__init__(self, **kwargs)
		strname = str(name)
		if strname.count(os.path.sep) > 0:
			directory = os.path.dirname(strname)
			basename = os.path.basename(strname)
			self.name = basename
			self._path = directory
		else:
			self.name = strname
			self._path = None
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
	def realpath(self):
		return os.path.realpath(self.fullpath)
	# End realpath


	@property
	def st_mode(self):
		if not Object.global_dry_run:
			fsdata = os.lstat(self.fullpath)
			return fsdata.st_mode
		return 0
	# End st_mode

	@property
	def st_ino(self):
		if not Object.global_dry_run:
			fsdata = os.lstat(self.fullpath)
			return fsdata.st_ino
		return 0
	# End st_ino

	@property
	def st_dev(self):
		if not Object.global_dry_run:
			fsdata = os.lstat(self.fullpath)
			return fsdata.st_dev
		return 0
	# End st_dev

	@property
	def st_nlink(self):
		if not Object.global_dry_run:
			fsdata = os.lstat(self.fullpath)
			return fsdata.st_nlink
		return 0
	# End st_nlink

	@property
	def st_uid(self):
		if not Object.global_dry_run:
			fsdata = os.lstat(self.fullpath)
			return fsdata.st_uid
		return 0
	# End st_uid

	@property
	def st_gid(self):
		if not Object.global_dry_run:
			fsdata = os.lstat(self.fullpath)
			return fsdata.st_gid
		return 0
	# End st_gid

	@property
	def st_size(self):
		if not Object.global_dry_run:
			fsdata = os.lstat(self.fullpath)
			return fsdata.st_size
		return 0
	# End st_size

	@property
	def st_atime(self):
		if not Object.global_dry_run:
			fsdata = os.lstat(self.fullpath)
			return fsdata.st_atime
		return 0
	# End st_atime

	@property
	def st_mtime(self):
		if not Object.global_dry_run:
			fsdata = os.lstat(self.fullpath)
			return fsdata.st_mtime
		return 0
	# End st_ino

	@property
	def st_ctime(self):
		if not Object.global_dry_run:
			fsdata = os.lstat(self.fullpath)
			return fsdata.st_ctime
		return 0
	# End st_ctime

	@property
	def directory(self):
		try:
			return stat.S_ISDIR(self.st_mode)
		except OSError as e:
			return False
	# End directory

	@property
	def characterSpecialDevice(self):
		try:
			return stat.S_ISCHR(self.st_mode)
		except OSError as e:
			return False
	# End characterSpecialDevice

	@property
	def blockSpecialDevice(self):
		try:
			return stat.S_ISBLK(self.st_mode)
		except OSError as e:
			return False
	# End blockSpecialDevice

	@property
	def regular(self):
		try:
			return stat.S_ISREG(self.st_mode)
		except OSError as e:
			return False
	# End regular

	@property
	def fifo(self):
		try:
			return stat.S_ISFIFO(self.st_mode)
		except OSError as e:
			return False
	# End fifo

	@property
	def symbolicLink(self):
		try:
			return os.path.islink(self.fullpath)
		except OSError as e:
			return False
	# End symbolicLink

	@property
	def socket(self):
		try:
			return stat.S_ISSOCK(self.st_mode)
		except OSError as e:
			return False
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
	def target(self):
		if self.type == SYMBOLIC_LINK:
			return os.readlink(self.fullpath)
		return None

	@property
	def hidden(self):
		if re.search(r'^\..*',self.name):
			return True
		return False

	# End hidden

	@property
	def extension(self):
		return None

	# End extension

	@property
	def hasExtension(self):
		if self.extension:
			return True
		return False

	# End hasExtension


	@property
	def exists(self):
		try:
			result = os.lstat(self.fullpath)
		except OSError as e:
			return False
		return True;
	# End exists


	@property
	def checksum(self):
		if self.regular:
			sha256 = hashlib.sha256()
			with open(self.fullpath, "rb") as f:
				for chunk in iter(lambda: f.read(4096), b""):
					sha256.update(chunk)
			return sha256.hexdigest()
		return ""

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
	def hasSetUID(self):
		if stat.S_IMODE(self.st_mode) & stat.S_ISUID:
			return True
		return False
	# End hasSetUID


	@property
	def hasSetGID(self):
		if stat.S_IMODE(self.st_mode) & stat.S_ISGID:
			return True
		return False
	# End hasSetGID


	@property
	def hasStickyBit(self):
		if stat.S_IMODE(self.st_mode) & stat.S_ISVTX:
			return True
		return False
	# End hasStickyBit


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


	def setPermissions(self, permissions):

		mode = 0

		if (permissions & USER_READ) == USER_READ:
			mode |= stat.S_IRUSR
		if (permissions & USER_WRITE) == USER_WRITE:
			mode |= stat.S_IWUSR
		if (permissions & USER_EXECUTE) == USER_EXECUTE:
			mode |= stat.S_IXUSR
		if (permissions & GROUP_READ) == GROUP_READ:
			mode |= stat.S_IRGRP
		if (permissions & GROUP_WRITE) == GROUP_WRITE:
			mode |= stat.S_IWGRP
		if (permissions & GROUP_EXECUTE) == GROUP_EXECUTE:
			mode |= stat.S_IXGRP
		if (permissions & OTHER_READ) == OTHER_READ:
			mode |= stat.S_IROTH
		if (permissions & OTHER_WRITE) == OTHER_WRITE:
			mode |= stat.S_IWOTH
		if (permissions & OTHER_EXECUTE) == OTHER_EXECUTE:
			mode |= stat.S_IXOTH
		if (permissions & SETUID) == SETUID:
			mode |= stat.S_ISUID
		if (permissions & SETGID) == SETGID:
			mode |= stat.S_ISGID
		if (permissions & STICKYBIT) == STICKYBIT:
			mode |= stat.S_ISVTX

		try:
			os.chmod(self.fullpath, mode)
		except OSError as e:
			raise FileSystemError("Unable to change permissions on file %s: %s" % (self.fullpath, str(e)))

	# End setPermissions


	def remove(self):
		if self.exists:
			os.remove(self.fullpath)


	def Difference(self,other):
		if self.__class__ != other.__class__:
	    		raise FileSystemError("%s not a %s" % (str(other),str(self.__class__)))
	    	shell = Shell()
		shell.capture_output = True
		o = shell.execute("diff " + self.fullpath + " " + other.fullpath)
		return o
	# End Difference


	def ContentsSameQ(self,other):
		if self.__class__ != other.__class__:
			raise FileSystemError("%s not a %s" % (str(other),str(self.__class__)))
		shell = Shell()
		shell.capture_output = True
		try:
			shell.execute("diff " + self.fullpath + " " + other.fullpath)
		except CommandError, e:
			return False
		return True

	# End ContentsSameQ

	def ContentsDifferentQ(self,other):
		if not self.ContentsSameQ(other):
			return True
		return False
	# End ContentsDifferentQ


	def __add__(self, other):
		return self.__class__(self.fullpath + os.sep + str(other))

	# End __add__


	def __radd__(self, other):
		return self.__class__(str(other) + os.sep + self.fullpath)

	# End __radd__


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
		return self.__class__.__name__ + "(" + self.path + os.sep + self.name + ")"
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



__all__ = ["BlockDevices",
	"CharacterDevices",
	"Directories",
	"Fifos",
	"Files",
	"Sockets",
	"SymbolicLinks",
	"DIRECTORY",
	"CHARACTER_DEVICE",
	"BLOCK_DEVICE",
	"REGULAR_FILE",
	"FIFO",
	"SYMBOLIC_LINK",
	"SOCKET",
	"NO_TYPE",
	"USER_READ",
	"USER_WRITE",
	"USER_EXECUTE",
	"GROUP_READ",
	"GROUP_WRITE",
	"GROUP_EXECUTE",
	"OTHER_READ",
	"OTHER_WRITE",
	"OTHER_EXECUTE",
	"SETUID",
	"SETGID",
	"STICKYBIT",
	"FileSystemError"
]


import BlockDevices
import CharacterDevices
import Directories
import Fifos
import Files
import Sockets
import SymbolicLinks



