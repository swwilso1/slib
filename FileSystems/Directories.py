#! /usr/bin/env python

import os
import shutil
from slib.Objects import Object
from slib.FileSystems import FileSystemBaseObject
from slib.FileSystems import FindFullDirectory
from BlockDevices import BlockDevice
from CharacterDevices import CharacterDevice
from Fifos import Fifo
from Files import File
from SymbolicLinks import SymbolicLink
from Sockets import Socket
from types import *


class Directory(FileSystemBaseObject):
	"""The Directory class."""

	def __init__(self, name, **kwargs):
		dirname = str(name)
		if kwargs.has_key('autofind'):
			if kwargs['autofind']:
				dirname = FindFullDirectory(dirname)
		FileSystemBaseObject.__init__(self, dirname, **kwargs)

	# End __init__


	@property
	def parent(self):
		return Directory(self.path)

	# End parent
	

	def __getObjectAccordingToClass(self,name,path):
		e = FileSystemBaseObject(self.fullpath + os.sep + name)
		if e.directory:
			obj = Directory(self.fullpath + os.sep + name)
		elif e.characterSpecialDevice:
			obj = CharacterDevice(self.fullpath + os.sep + name)
		elif e.blockSpecialDevice:
			obj = BlockDevice(self.fullpath + os.sep + name)
		elif e.regular:
			obj = File(self.fullpath + os.sep + name)
		elif e.fifo:
			obj = Fifo(self.fullpath + os.sep + name)
		elif e.symbolicLink:
			obj = SymbolicLink(self.fullpath + os.sep + name)
		elif e.socket:
			obj = Socket(self.fullpath + os.sep + name)
		else:
			obj = e
		return obj

	# End __getObjectAccordingToClass
	


	@property
	def entries(self):
		entries = []
		names = os.listdir(self.fullpath)
		for name in names:
			entries.append(self.__getObjectAccordingToClass(name,self.fullpath))

		return entries
	# End entries
	

	@property
	def empty(self):
		return len(self.entries) == 0

	# End empty
	


	@property
	def files(self):
		files = []
		try:
			entries = os.listdir(self.fullpath)
		except OSError as e:
			if not Object.global_dry_run:
				raise e
			entries = []

		for entry in entries:
			obj = FileSystemBaseObject(self.fullpath + os.sep + entry)
			if not obj.directory and \
			   not obj.socket and \
			   not obj.symbolicLink and \
			   not obj.fifo:
				files.append(self.__getObjectAccordingToClass(entry,self.fullpath))
		return files
	# End files

	@property
	def directories(self):
		directories = []
		try:
			entries = os.listdir(self.fullpath)
		except OSError as e:
			if not Object.global_dry_run:
				raise e
			entries = []
		for entry in entries:
			obj = self.__getObjectAccordingToClass(entry,self.fullpath)
			if obj.directory:
				directories.append(obj)
		return directories
	# End directories

	@property
	def characters(self):
		specials = []
		try:
			entries = os.listdir(self.fullpath)
		except OSError as e:
			if not Object.global_dry_run:
				raise e
			entries = []
		for entry in entries:
			obj = self.__getObjectAccordingToClass(entry,self.fullpath)
			if obj.characterSpecialDevice:
				specials.append(obj)
		return specials
	# End characters
	
	@property
	def blocks(self):
		specials = []
		try:
			entries = os.listdir(self.fullpath)
		except OSError as e:
			if not Object.global_dry_run:
				raise e
			entries = []
		for entry in entries:
			obj = self.__getObjectAccordingToClass(entry,self.fullpath)
			if obj.blockSpecialDevice:
				specials.append(obj)
		return specials
	# End blocks
	
	@property
	def regulars(self):
		regs = []
		try:
			entries = os.listdir(self.fullpath)
		except OSError as e:
			if not Object.global_dry_run:
				raise e
			entries = []
		for entry in entries:
			obj = self.__getObjectAccordingToClass(entry,self.fullpath)
			if obj.regular:
				regs.append(obj)
		return regs
	# End regulars
	
	@property
	def fifos(self):
		specials = []
		try:
			entries = os.listdir(self.fullpath)
		except OSError as e:
			if not Object.global_dry_run:
				raise e
			entries = []
		for entry in entries:
			obj = self.__getObjectAccordingToClass(entry,self.fullpath)
			if obj.fifo:
				specials.append(obj)
		return specials
	# End fifos

	@property
	def links(self):
		specials = []
		try:
			entries = os.listdir(self.fullpath)
		except OSError as e:
			if not Object.global_dry_run:
				raise e
			entries = []
		for entry in entries:
			obj = self.__getObjectAccordingToClass(entry,self.fullpath)
			if obj.symbolicLink:
				specials.append(obj)
		return specials
	# End links

	@property
	def sockets(self):
		specials = []
		try:
			entries = os.listdir(self.fullpath)
		except OSError as e:
			if not Object.global_dry_run:
				raise e
			entries = []
		for entry in entries:
			obj = self.__getObjectAccordingToClass(entry,self.fullpath)
			if obj.socket:
				specials.append(obj)
		return specials
	# End sockets


	@property
	def all_files(self):
		files = self.files
		dirs = self.directories
		for d in dirs:
			files.extend(d.all_files)
		return files
	# End all_files
	
	@property
	def all_characters(self):
		files = self.characters
		dirs = self.directories
		for d in dirs:
			files.extend(d.all_characters)
		return files
	# End all_characters

	@property
	def all_blocks(self):
		files = self.blocks
		dirs = self.directories
		for d in dirs:
			files.extend(d.all_blocks)
		return files
	# End all_blocks

	@property
	def all_regulars(self):
		files = self.regulars
		dirs = self.directories
		for d in dirs:
			files.extend(d.all_regulars)
		return files
	# End all_regulars

	@property
	def all_fifos(self):
		files = self.fifos
		dirs = self.directories
		for d in dirs:
			files.extend(d.all_fifos)
		return files
	# End all_fifos
	
	@property
	def all_links(self):
		files = self.links
		dirs = self.directories
		for d in dirs:
			files.extend(d.all_links)
		return files
	# End all_links

	@property
	def all_sockets(self):
		files = self.sockets
		dirs = self.directories
		for d in dirs:
			files.extend(d.all_sockets)
		return files
	# End all_sockets
	
	@property
	def all_entries(self):
		entries = self.entries
		dirs = self.directories
		for d in dirs:
			entries.append(d)
			entries.extend(d.all_entries)
		return entries
	# End all_entries


	@property
	def extensions(self):
		allEntries = self.all_entries
		extensions = {}
		for entry in allEntries:
			if entry.hasExtension:
				if not extensions.has_key(entry.extension):
					extensions[entry.extension] = True
		return extensions.keys()

	# End extensions


	def create(self):
		if Object.log_object and Object.global_dry_run:
			Object.log_object.log("mkdir " + self.fullpath)
		if not Object.global_dry_run:
			os.makedirs(self.fullpath)

	# End create
	
	def remove(self):
		if os.path.exists(self.fullpath):
			shutil.rmtree(self.fullpath)

	# End remove
	

	def __getitem__(self,key):
		if type(key) != StringType and type(key) != UnicodeType:
			raise KeyError(key)
		obj = FileSystemBaseObject(key)
		if not obj.exists:
			raise KeyError(key)
		
		return self.__getObjectAccordingToClass(obj.name, obj.path)

	# End __getitem__
	

	def __contains__(self,obj):
		return self.has_key(obj)
	# End __contains__
	
	
	def has_key(self,key):
		if type(key) != StringType and type(key) != UnicodeType:
			return False

		obj = FileSystemBaseObject(key)
		if not obj.exists:
			return False

		return True
		
	# End has_key

	def keys(self):
		return [ entry.fullpath for entry in self.entries ]
	# End keys	


	def hasChild(self,child):
		for entry in self.entries:
			if child == entry.name:
				return True
			if entry.directory:
				if entry.hasChild(child):
					return True
		return False	
			
	# End hasChild
	
	
	def getChildren(self,child):
		children = []
		for entry in self.entries:
			if child == entry.name:
				children.append(entry)
			if entry.directory:
				children.extend(entry.getChildren(child))
		return children
	# End getChildren
	
	
	def make_current_directory(self):
		current_directory = os.getcwd()
		try:
			if Object.log_object and Object.global_dry_run:
				Object.log_object.log("cd " + self.fullpath)
			os.chdir(self.fullpath)
		except OSError as e:
			if not Object.global_dry_run:
				raise e
		return Directory(current_directory)

	# End make_current_directory
	

# End Directory



def MakeDirectoryAndRemovePreviousContents(name,clearDirectory=True):
	if os.path.exists(name):
		if not clearDirectory:
			shutil.rmtree(name)
			if Object.log_object and Object.global_dry_run:
				Object.log_object.log("mkdir " + name)
			os.mkdir(name)
	else:
		if Object.log_object and Object.global_dry_run:
			Object.log_object.log("mkdir " + name)
		os.mkdir(name)

# End MakeDirectoryAndRemovePreviousContents


def RemoveDirectory(name):
	if os.path.exists(name):
		shutil.rmtree(name)

# End RemoveDirectory

