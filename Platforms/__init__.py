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

import re
import sys
import types
import types
from .. Objects import Object
from .. Errors import Error, ArgumentError

class PlatformInspectionError(Error):
	"""The PlatformInspectionError class."""

	def __init__(self, value, **kwargs):
		Error.__init__(self, value, **kwargs)

	# End __init__

# End PlatformInspectionError


class PlatformInspectorBaseObject(Object):
	"""The PlatformInspectorBaseObject class."""

	def __init__(self, **kwargs):
		Object.__init__(self, **kwargs)
		self._installedRam = 0
		self._os = ""
		self._osVersion = ""
		self._systemID = ""
		self._machineHardware = ""
	# End __init__

	@property
	def installedRam(self):
		return self._installedRam

	# End installedRam

	@installedRam.setter
	def installedRam(self,value):
		if type(value) != types.IntType and type(value) != types.LongType:
			raise TypeError("Value must be an integral type")
		self._installedRam = value

	# End installedRam.setter

	@installedRam.deleter
	def installedRam(self):
		raise TypeError("Unable to delete installedRam")

	# End installedRam.deleter

	@property
	def os(self):
		return self._os

	# End os

	@os.setter
	def os(self,value):
		if type(value) != types.StringType:
			raise TypeError("Value must be a String object")
		self._os = value

	# End os.setter

	@os.deleter
	def os(self):
		raise TypeError("Unable to delete os")

	# End os.deleter

	@property
	def osVersion(self):
		return self._osVersion

	# End osVersion

	@osVersion.setter
	def osVersion(self,value):
		if type(value) != types.StringType:
			raise TypeError("Value must be a String object")
		self._osVersion = value

	# End osVersion.setter

	@osVersion.deleter
	def osVersion(self):
		raise TypeError("Unable to delete osVersion")

	# End osVersion.deleter


	@property
	def osMajorVersion(self):
		thisVersion = self.osVersion
		majorVersion = re.sub(r'([\d]+)\..*', '\\1', thisVersion)
		return int(majorVersion)
	# End osMajorVersion

	@osMajorVersion.setter
	def osMajorVersion(self,value):
		raise TypeError("Unable to reset osMajorVersion")

	# End osMajorVersion.setter

	@osMajorVersion.deleter
	def osMajorVersion(self):
		raise TypeError("Unable to delete osMajorVersion")

	# End osMajorVersion.deleter

	@property
	def osMinorVersion(self):
		thisVersion = self.osVersion
		minorVersion = re.sub(r'[\d]+\.([\d]+)\..*', '\\1', thisVersion)
		return int(minorVersion)

	# End osMinorVersion

	@osMinorVersion.setter
	def osMinorVersion(self,value):
		raise TypeError("Unable to reset osMinorVersion")

	# End osMinorVersion.setter


	@osMinorVersion.deleter
	def osMinorVersion(self):
		raise TypeError("Unable to delete osMinorVersion")

	# End osMinorVersion.deleter

	@property
	def osReleaseVersion(self):
		thisVersion = self.osVersion
		releaseVersion = re.sub(r'[\d]+\.[\d]+\.([\d]+)', '\\1', thisVersion)
		return int(releaseVersion)

	# End osReleaseVersion

	@osReleaseVersion.setter
	def osReleaseVersion(self,value):
		raise TypeError("Unable to reset osReleaseVersion")

	# End osReleaseVersion.setter

	@osReleaseVersion.deleter
	def osReleaseVersion(self):
		raise TypeError("Unable to reset osReleaseVersion")

	# End osReleaseVersion.deleter

	@property
	def systemID(self):
		return self._systemID

	# End systemID

	@systemID.setter
	def systemID(self,value):
		if type(value) != types.StringType:
			raise TypeError("Value must be a String object")
		self._systemID = value

	# End systemID.setter

	@systemID.deleter
	def systemID(self):
		raise TypeError("Unable to delete systemID")

	# End systemID.deleter


	@property
	def machineHardware(self):
		return self._machineHardware

	# End machineHardware

	@machineHardware.setter
	def machineHardware(self,value):
		if type(value) != types.StringType:
			raise TypeError("Value must be a String object")
		self._machineHardware = value

	# End machineHardware.setter

	@machineHardware.deleter
	def machineHardware(self):
		raise TypeError("Unable to delete machineHardware")

	# End machineHardware.deleter



# End PlatformInspectorBaseObject

from . import Mac