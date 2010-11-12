#! /usr/bin/env python

import time
import types
from slib.Objects import Object
from slib.Errors import Error

class DateError(object):
	"""The DateError class."""

	def __init__(self, value, **kwargs):
		Error.__init__(self,value,**kwargs)
		self.value = value

	# End __init__

# End DateError


class Format(Object):
	"""The Format class."""

	days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
	months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', \
		'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

	def __init__(self, **kwargs):
		Object.__init__(self,**kwargs)
		self.military_time = False
	# End __init__


	def __call__(self,time):
		return str(time.time)

	# End __call__

	def number_as_string(self,number):
		if number <= 9:
			return '0' + str(number)
		else:
			return str(number)

	# End number_as_string
	

	def __repr__(self):
		return self.__class__.__name__ + "()"

	# End __repr__
	

# End Format


class VerboseFormat(Format):
	"""The VerboseFormat class."""

	def __init__(self, **kwargs):
		Format.__init__(self,**kwargs)

	# End __init__

	def __call__(self,time):
		day = self.days[time.weekday]
		month = self.months[time.month - 1]
		mday = self.number_as_string(time.day)
		hour = self.number_as_string(time.hour)
		minute = self.number_as_string(time.minute)
		second = self.number_as_string(time.second)
		year = self.number_as_string(time.year)
		if not self.military_time:
			if time.hour > 12:
				hour = self.number_as_string(time.hour - 12)
				ampm = 'PM'
			else:
				ampm = 'AM'
		else:
			ampm = None

		result = day + ' ' + month + ' ' + mday + ' ' + hour + ':' + minute + ':' + second

		if ampm:
			result += ' ' + ampm
		
		return result + ' ' + year
		
	# End __call__
	
# End VerboseFormat



class MonthDayYearWithSlashesFormat(Format):
	"""The MonthDayYearWithSlashesFormat class."""

	def __init__(self, **kwargs):
		Format.__init__(self,**kwargs)

	# End __init__

	
	def __call__(self,time):
		month = self.number_as_string(time.month)
		day = self.number_as_string(time.day)
		year = self.number_as_string(time.year)
		return month + "/" + day + "/" + year

	# End __call__
	
# End MonthDayYearWithSlashesFormat


class MonthDayYearWithDashesFormat(Format):
	"""The MonthDayYearWithDashes class."""

	def __init__(self, **kwargs):
		Format.__init__(self,**kwargs)

	# End __init__

	
	def __call__(self,time):
		month = self.number_as_string(time.month)
		day = self.number_as_string(time.day)
		year = self.number_as_string(time.year)
		return month + "-" + day + "-" + year

	# End __call__
	

# End MonthDayYearWithDashesFormat


class DateTimeFormat(Format):
	"""The DateTimeFormat class."""

	def __init__(self, **kwargs):
		Format.__init__(self,**kwargs)

	# End __init__
	
	
	def __call__(self,time):
		month = self.number_as_string(time.month)
		day = self.number_as_string(time.day)
		year = self.number_as_string(time.year)
		hour = self.number_as_string(time.hour)
		minute = self.number_as_string(time.minute)
		second = self.number_as_string(time.second)

		year = year[2:]

		if not self.military_time:
			if time.hour > 12:
				hour = self.number_as_string(time.hour - 12)
				ampm = 'PM'
			else:
				ampm = 'AM'
		else:
			ampm = None

		result = month + '/' + day + '/' + year + ' ' + hour + ':' + minute + ':' + second

		if ampm:
			result += ' ' + ampm
		
		return result

	# End __call__
	

# End DateTimeFormat


HOUR = 3600
DAY = HOUR * 24
YEAR = DAY * 365
LEAPYEAR = DAY * 366


class Date(Object):
	"""The Date class."""

	def __init__(self, intime=None, **kwargs):
		Object.__init__(self,**kwargs)
		if intime:
			if type(intime) == types.IntType or type(intime) == types.LongType or type(intime) == types.FloatType:
				self.time = intime
			else:
				self.time = time.time()
		else:
			self.time = time.time()
		self.timeframe = time.localtime
		self.formatter = VerboseFormat()
	# End __init__

	
	def update_time_to_current_time(self):
		self.time = time.time()

	# End set_time_to_current_time
	

	@property
	def use_local_time(self):
		if self.timeframe == time.localtime:
			return True
		return False

	# End use_local_type
	
	@use_local_time.setter
	def use_local_time(self,value):
		if value == True:
			self.timeframe = time.localtime
	
	@property
	def use_gm_time(self):
		if self.timeframe == time.gmtime:
			return True
		return False

	# End use_gm_time

	@use_gm_time.setter
	def use_gm_time(self, value):
		if value == True:
			self.timeframe = time.gmtime

	# End use_gm_time
	

	@property
	def year(self):
		return self.timeframe(self.time)[0]

	# End year

	
	@property
	def month(self):
		return self.timeframe(self.time)[1]

	# End month
	
	@property
	def day(self):
		return self.timeframe(self.time)[2]

	# End day
	
	@property
	def hour(self):
		return self.timeframe(self.time)[3]

	# End hour
	
	@property
	def minute(self):
		return self.timeframe(self.time)[4]

	# End minute
	
	@property
	def second(self):
		return self.timeframe(self.time)[5]

	# End second
	
	@property
	def weekday(self):
		return self.timeframe(self.time)[6]

	# End weekday
	
	@property
	def day_of_year(self):
		return self.timeframe(self.time)[7]

	# End day_of_year
	
	@property
	def daylight_savings_time(self):
		return self.timeframe(self.time)[8]

	# End daylight_savings_time

	
	@property
	def leapyear(self):
	 	year = self.year
		if year < 0:
			year += 1
			res = year % 4
			if res == 0:
				return True
			else:
				return False
		elif year < 1582:
			res = year % 4
			if res == 0:
				return True
			else:
				return False
		elif (year % 4) != 0:
			return False
		elif (year % 100) != 0:
			return True
		elif (year % 400) != 0:
			return False
		else:
			return True
	# End leapyear
	
	
	@property
	def timezone(self):
		return time.tzname

	# End timezone
	
	
	@property
	def tuple(self):
		return (self.month, self.day, self.year)

	# End tuple
	
	def __lt__(self,other):
		if isinstance(other, self.__class__):
			if self.time < other.time:
				return True
			return False
		elif type(other) == types.IntType or type(other) == types.LongType or type(other) == types.FloatType:
			if self.time < other:
				return True
			return False
		else:
			raise CalendarError("Unable to compare objects of type %s and %s" % (self.__class__.__name__, type(other)))

	# End __lt__
	

	def __le__(self,other):
		if isinstance(other, self.__class__):
			if self.time <= other.time:
				return True
			return False
		elif type(other) == types.IntType or type(other) == types.LongType or type(other) == types.FloatType:
			if self.time <= other:
				return True
			return False
		else:
			raise CalendarError("Unable to compare objects of type %s and %s" % (self.__class__.__name__, type(other)))

	# End __le__
	
	
	def __gt__(self,other):
		if isinstance(other, self.__class__):
			if self.time > other.time:
				return True
			return False
		elif type(other) == types.IntType or type(other) == types.LongType or type(other) == types.FloatType:
			if self.time > other:
				return True
			return False
		else:
			raise CalendarError("Unable to compare objects of type %s and %s" % (self.__class__.__name__, type(other)))

	# End __gt__


	def __ge__(self,other):
		if isinstance(other, self.__class__):
			if self.time >= other.time:
				return True
			return False
		elif type(other) == types.IntType or type(other) == types.LongType or type(other) == types.FloatType:
			if self.time >= other:
				return True
			return False
		else:
			raise CalendarError("Unable to compare objects of type %s and %s" % (self.__class__.__name__, type(other)))

	# End __ge__


	def __eq__(self,other):
		if isinstance(other, self.__class__):
			if self.time == other.time:
				return True
			return False
		elif type(other) == types.IntType or type(other) == types.LongType or type(other) == types.FloatType:
			if self.time == other:
				return True
			return False
		else:
			raise CalendarError("Unable to compare objects of type %s and %s" % (self.__class__.__name__, type(other)))

	# End __eq__


	def __ne__(self,other):
		if isinstance(other, self.__class__):
			if self.time != other.time:
				return True
			return False
		elif type(other) == types.IntType or type(other) == types.LongType or type(other) == types.FloatType:
			if self.time != other:
				return True
			return False
		else:
			raise CalendarError("Unable to compare objects of type %s and %s" % (self.__class__.__name__, type(other)))

	# End __ne__
	

	def __int__(self):
		return int(self.time)

	# End __int__


	def __long__(self):
		return long(self.time)

	# End __long__
	
	
	def __float__(self):
		return float(self.time)

	# End __float__
	
	
	def __complex__(self):
		return complex(self.time)

	# End __complex__
	
	
	def __hex__(self):
		return hex(self.time)

	# End __hex__
	
	def __oct__(self):
		return oct(self.time)

	# End __oct__
	
	
	def __add__(self,other):
		if isinstance(other, self.__class__):
			return self.__class__(self.time + other.time)
		elif type(other) == types.IntType or type(other) == types.LongType or type(other) == types.FloatType:
			return self.__class__(self.time + other)
		else:
			raise CalendarError("Cannot add objects of type %s and %s" % (self.__class__.__name__, type(other)))

	# End __add__
	
	
	def __radd__(self,other): # other + self
		if isinstance(other, self.__class__):
			return self.__class__(self.time + other.time)
		elif type(other) == types.IntType or type(other) == types.LongType or type(other) == types.FloatType:
			return self.__class__(self.time + other)
		else:
			raise CalendarError("Cannot add objects of type %s and %s" % (self.__class__.__name__, type(other)))

	# End __radd__


	def __iadd__(self,other):
		if isinstance(other, self.__class__):
			self.time += other.time
		elif type(other) == types.IntType or type(other) == types.LongType or type(other) == types.FloatType:
			self.time += other
		else:
			raise CalendarError("Cannot add objects of type %s and %s" % (self.__class__.__name__, type(other)))

	# End __iadd__

	
	def __sub__(self,other):
		if isinstance(other, self.__class__):
			return self.__class__(self.time - other.time)
		elif type(other) == types.IntType or type(other) == types.LongType or type(other) == types.FloatType:
			return self.__class__(self.time - other)
		else:
			raise CalendarError("Cannot subtract objects of type %s and %s" % (self.__class__.__name__, type(other)))

	# End __sub__


	def __rsub__(self,other):
		if isinstance(other, self.__class__):
			return self.__class__(other.time - self.time)
		elif type(other) == types.IntType or type(other) == types.LongType or type(other) == types.FloatType:
			return self.__class__(other - self.time)
		else:
			raise CalendarError("Cannot subtract objects of type %s and %s" % (self.__class__.__name__, type(other)))

	# End __rsub__
	
	
	def __isub__(self,other):
		if isinstance(other, self.__class__):
			self.time -= other.time
		elif type(other) == types.IntType or type(other) == types.LongType or type(other) == types.FloatType:
			self.time -= other
		else:
			raise CalendarError("Cannot subtract objects of type %s and %s" % (self.__class__.__name__, type(other)))

	# End __isub__
	
	
	def __str__(self):
		return self.formatter(self)

	# End __str__
	
	
	def __repr__(self):
		return self.__class__.__name__ + "(" + str(self.time) + ")"

	# End __repr__
	
	
	def __coerce__(self,other):
		if isinstance(other,self.__class__):
			return self,other
		if isinstance(other,Date):
			return self,self.__class__(other.time)
		try:
			return self, self.__class__(other)
		except ValueError, e:
			pass

	# End __coerce__
	
	

# End Date

