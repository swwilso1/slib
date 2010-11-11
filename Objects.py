

class Object(object):
	"""The Object class."""

	def __init__(self, **kwargs):
		if kwargs.has_key("log"):
			self.log = kwargs["log"]
		else:
			self.log = None

	# End __init__

# End Object
