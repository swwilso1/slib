#! /usr/bin/env python

import os
import shutil
import slib.FileSystems
import slib.FileSystems.BlockDevices
import slib.FileSystems.CharacterDevices
import slib.FileSystems.Fifos
import slib.FileSystems.Files
import slib.FileSystems.SymbolicLinks
import slib.FileSystems.Sockets
from types import *


class Directory(slib.FileSystems.FileSystemBaseObject):
	"""The Directory class."""

	def __init__(self, name, path=None):
		slib.FileSystems.FileSystemBaseObject.__init__(self, name, path)

	# End __init__


	@property
	def parent(self):
		return Directory(self.path)

	# End parent
	

	def __getObjectAccordingToClass(self,name,path):
		e = slib.FileSystems.FileSystemBaseObject(name, self.fullpath)
		if e.directory:
			obj = Directory(name,self.fullpath)
		elif e.characterSpecialDevice:
			obj = slib.FileSystems.CharacterDevices.CharacterDevice(name,self.fullpath)
		elif e.blockSpecialDevice:
			obj = slib.FileSystems.BlockDevices.BlockDevice(name,self.fullpath)
		elif e.regular:
			obj = slib.FileSystems.Files.File(name,self.fullpath)
		elif e.fifo:
			obj = slib.FileSystems.Fifos.Fifo(name,self.fullpath)
		elif e.symbolicLink:
			obj = slib.FileSystems.SymbolicLinks.SymbolicLink(name,self.fullpath)
		elif e.socket:
			obj = slib.FileSystems.Sockets.Socket(name,self.fullpath)
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
	def files(self):
		files = []
		entries = os.listdir(self.fullpath)
		for entry in entries:
			obj = slib.FileSystems. FileSystemBaseObject(entry, self.fullpath)
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
		entries = os.listdir(self.fullpath)
		for entry in entries:
			obj = self.__getObjectAccordingToClass(entry,self.fullpath)
			if obj.directory:
				directories.append(obj)
		return directories
	# End directories

	@property
	def characters(self):
		specials = []
		entries = os.listdir(self.fullpath)
		for entry in entries:
			obj = self.__getObjectAccordingToClass(entry,self.fullpath)
			if obj.characterSpecialDevice:
				specials.append(obj)
		return specials
	# End characters
	
	@property
	def blocks(self):
		specials = []
		entries = os.listdir(self.fullpath)
		for entry in entries:
			obj = self.__getObjectAccordingToClass(entry,self.fullpath)
			if obj.blockSpecialDevice:
				specials.append(obj)
		return specials
	# End blocks
	
	@property
	def regulars(self):
		regs = []
		entries = os.listdir(self.fullpath)
		for entry in entries:
			obj = self.__getObjectAccordingToClass(entry,self.fullpath)
			if obj.regular:
				regs.append(obj)
		return regs
	# End regulars
	
	@property
	def fifos(self):
		specials = []
		entries = os.listdir(self.fullpath)
		for entry in entries:
			obj = self.__getObjectAccordingToClass(entry,self.fullpath)
			if obj.fifo:
				specials.append(obj)
		return specials
	# End fifos

	@property
	def links(self):
		specials = []
		entries = os.listdir(self.fullpath)
		for entry in entries:
			obj = self.__getObjectAccordingToClass(entry,self.fullpath)
			if obj.symbolicLink:
				specials.append(obj)
		return specials
	# End links

	@property
	def sockets(self):
		specials = []
		entries = os.listdir(self.fullpath)
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

	def __getitem__(self,key):
		if type(key) != StringType and type(key) != UnicodeType:
			raise KeyError(key)
		obj = slib.FileSystems.FileSystemBaseObject(key)
		if not obj.exists:
			raise KeyError(key)
		
		return self.__getObjectAccordingToClass(obj.name, obj.path)

		# skey = str(key)
		# path = self.fullpath + os.path.sep + os.path.dirname(skey)
		# name = os.path.basename(skey)
		# obj = slib.FileSystems.FileSystemBaseObject(name,path)
		# if not obj.exists:
		# 	raise KeyError(skey)
		# return self.__getObjectAccordingToClass(name,path)
	# End __getitem__
	

	def __contains__(self,obj):
		return self.has_key(obj)
	# End __contains__
	
	
	def has_key(self,key):
		if type(key) != StringType and type(key) != UnicodeType:
			return False

		obj = slib.FileSystems.FileSystemBaseObject(key)
		if not obj.exists:
			return False

		return True
		

		# path = self.fullpath + os.path.sep + os.path.dirname(key)
		# name = os.path.basename(key)
		# obj = slib.FileSystems.FileSystemBaseObject(name,path)
		# if not obj.exists:
		# 	return False
		# return True
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
	

# End Directory



def MakeDirectoryAndRemovePreviousContents(name,clearDirectory=True):
	if os.path.exists(name):
		if not clearDirectory:
			shutil.rmtree(name)
			os.mkdir(name)
	else:
		os.mkdir(name)

# End MakeDirectoryAndRemovePreviousContents


def RemoveDirectory(name):
	if os.path.exists(name):
		shutil.rmtree(name)

# End RemoveDirectory

