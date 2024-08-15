from dataclasses import dataclass, field

import lasio

import numpy

@dataclass(frozen=True)
class Datum:

	array 	: lasio.CurveItem

	lower 	: float = None
	upper 	: float = None

	power 	: int = None

	def __post_init__(self):
		"""Assigns corrected lower and upper values."""

		lower = numpy.nanmin(self.array).tolist()
		upper = numpy.nanmax(self.array).tolist()

		lower = lower if self.lower is None else self.lower
		upper = upper if self.upper is None else self.upper

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

if __name__ == "__main__":

	print(Curve.upower(1312))

	a = Curve([0.1,2,9],upper=10)

	object.__setattr__(a,'trail',7)

	print(a.array)
	print(a.lower)
	print(a.upper)
	print(a.power)
	print(a.trail)