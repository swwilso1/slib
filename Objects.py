

class Object(object):
	"""The Object class."""

	def __init__(self, **kwargs):
		if kwargs.has_key("log"):
			self.log_object = kwargs["log"]
		else:
			self.log_object = None

	# End __init__

# End Object
