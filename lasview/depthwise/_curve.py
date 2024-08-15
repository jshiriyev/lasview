from dataclasses import dataclass, field

import lasio

import numpy

from layout._xaxis import Xaxis
from layout._unary import Unary

@dataclass(frozen=True)
class Curve(Datum):

	colid 	: int = None
	rowid 	: int = None

	trail	: numpy.ndarray = field(
		init = False,
		repr = False,
		default = None,
		)

	def __call__(self,xaxis:Xaxis):
		"""Returns the axis values and limit (left,right) for the data."""

		if scale == "linear":
			multp = self.ufloor(self.length/curve.length)
		elif scale == "log10":
			multp = 10**self.uceil(-numpy.log10(curve.lower))

		if scale == "linear":
			trail = self.lower+(curve.upper-data if flip else data-curve.lower)*multp
		elif scale == "log10":
			trail = data*multp

		object.__setattr__(curve,'trail',trail)

		return curve

if __name__ == "__main__":

	print(Curve.upower(1312))

	a = Curve([0.1,2,9],upper=10)

	object.__setattr__(a,'trail',7)

	print(a.array)
	print(a.lower)
	print(a.upper)
	print(a.power)
	print(a.trail)