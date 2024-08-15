from dataclasses import dataclass, field

import lasio

import numpy

@dataclass(frozen=True)
class Curve:

	array 	: lasio.CurveItem

	lower 	: float = None
	upper 	: float = None

	power 	: int = None

	colid 	: int = None
	rowid 	: int = None

	trail	: numpy.ndarray = field(
		init = False,
		repr = False,
		default = None,
		)

	def __post_init__(self):
		"""Assigns corrected lower and upper values."""

		lower = numpy.nanmin(self.array).tolist() if self.lower is None else self.lower
		upper = numpy.nanmax(self.array).tolist() if self.upper is None else self.upper

		power = min([self.upower(lower),self.upower(upper)]) if self.power is None else self.power

		lower,upper = self.ufloor(lower,power),self.uceil(upper,power)

		if self.power is None:
			object.__setattr__(self,'power',power)

		if self.lower is None:
			object.__setattr__(self,'lower',lower)

		if self.upper is None:
			object.__setattr__(self,'upper',upper)

	@property
	def limit(self):
		"""
		Returns the limit based on lower and upper values.
		"""
		return (self.lower,self.upper)

	@property
	def length(self):
		"""
		Returns the length based on limits.
		"""
		return self.upper-self.lower

	"""Static methods for float types."""

	@staticmethod
	def upower(x:float):
		"""
		Returns the tenth power that brings float point next to the first
		significant digit.
		"""
		return -int(numpy.floor(numpy.log10(abs(x))))

	@staticmethod
	def uceil(x:float,power:int=None):
		"""
		Returns the ceil value for the first significant digit by default.
		
		If the power is specified, it is used as a factor before ceiling.
		"""
		if power is None:
			power = Curve.upower(x)

		return (numpy.ceil(x*10**power)/10**power).tolist()

	@staticmethod
	def ufloor(x:float,power:int=None):
		"""
		Returns the floor value for the first significant digit by default.
		
		If the power is specified, it is used as a factor before flooring.
		"""
		if power is None:
			power = Curve.upower(x)

		return (numpy.floor(x*10**power)/10**power).tolist()

	@staticmethod
	def uround(x:float,power:int=None):
		"""Returns the rounded value for the first significant digit."""
		
		if power is None:
			power = Curve.upower(x)

		return (numpy.round(x*10**power)/10**power).tolist()

if __name__ == "__main__":

	print(Curve.upower(1312))

	a = Curve([0.1,2,9],upper=10)

	object.__setattr__(a,'trail',7)

	print(a.array)
	print(a.lower)
	print(a.upper)
	print(a.power)
	print(a.trail)