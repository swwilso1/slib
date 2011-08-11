import types

class Object(object):
	"""The Object class."""

	log_object = None
	global_dry_run = False

	def __init__(self, **kwargs):
		if kwargs.has_key("log"):
			Object.log_object = kwargs["log"]	
		
		if kwargs.has_key("verbose"):
			if type(kwargs["verbose"]) != types.BooleanType:
				raise TypeError("verbose keyword value must be Boolean")
			Object.verbose = kwargs["verbose"]


	# End __init__


	def setClassVerbose(self, arg):
		if type(arg) != types.BooleanType:
			raise TypeError("Argument must be boolean")
		Object.verbose = arg

	# End setClassVerbose
	
	
	def getClassVerbose(self):
		if Object.__dict__.has_key("verbose"):
			return Object.verbose
		return False
	
	# End getClassVerbose
	

	def setClassLog(self, log):
		Object.log_object = log

	# End set_class_log

	def enableGlobalDryRun(self):
		Object.global_dry_run = True

	# End enableGlobalDryRun	

	def logIfVerbose(self, arg):
		if Object.log_object and Object.getClassVerbose(self) and arg != None:
			Object.log_object.log(str(arg))
	# End logIfVerbose
	
	def logIfDryRun(self, arg):
		if Object.log_object and Object.global_dry_run and arg != None:
			Object.log_object.log(str(arg))

	# End logIfDryRun
	
	

# End Object
