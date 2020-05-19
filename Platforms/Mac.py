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

import os
import re
import sys
import types

__all__ = ["Mac"]

from .. Objects import Object
from .. Platforms import PlatformInspectorBaseObject, PlatformInspectionError
from .. Commands.Shells import Shell

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
