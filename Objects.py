

class Object(object):
	"""The Object class."""

	log_object = None

	def __init__(self, **kwargs):
		if kwargs.has_key("log"):
			Object.log_object = kwargs["log"]

	# End __init__

	def setClassLog(self, log):
		Object.log_object = log

	# End set_class_log
	

# End Object
