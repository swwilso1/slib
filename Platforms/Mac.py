#! /usr/bin/env python

import os
import re
import sys
import types

__all__ = ["Mac"]

from slib.Objects import Object
from slib.Platforms import PlatformInspectorBaseObject, PlatformInspectionError
from slib.Commands.Shells import Shell

class MacInspector(PlatformInspectorBaseObject):
	"""The MacInspector class."""

	def __init__(self, **kwargs):
		PlatformInspectorBaseObject.__init__(self,**kwargs)

		self._os = "Mac OS X"

		shell = Shell(capture_output=True)

		self._installedRam = shell.execute("sysctl hw.memsize | awk '{print $2; }'").strip()
		
		self._installedRam = long(self._installedRam)

		Object.logIfVerbose(self,"sw_vers -productVersion")
		self._osVersion = shell.execute("sw_vers -productVersion").strip()
		if re.match(r'[\d]+\.[\d]+$',self._osVersion):
			self._osVersion += ".0"

		Object.logIfVerbose(self,self._osVersion)

		self._machineHardware = shell.execute("uname -m").strip()
		
		if re.search(r'x86_64', self._machineHardware):
			self._systemID = "MacOSX-x86-64"
		elif re.search(r'i386', self._machineHardware):
			self._systemID = "MacOSX-x86"
		elif re.search(r'ppc', self._machineHardware):
			self._systemID = "MacOSX"
		
	# End __init__

# End MacInspector
