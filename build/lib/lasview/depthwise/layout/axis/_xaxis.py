from dataclasses import dataclass, field

import numpy

from lasview.depthwise.layout.items._curve import Curve

@dataclass(frozen=True)
class Xaxis:
	"""
	It initializes the axis of plane in a track:

	limit 	: lower and upper values of the axis
	
	major 	: sets the frequency of major ticks
	minor 	: sets the frequency of minor ticks

	scale   : axis scale: linear or log10, check the link below
			https://matplotlib.org/stable/users/explain/axes/axes_scales.html
			for the available scales in matplotlib.

	spot 	: location of axis in the layout, int

	"""

	limit 	: tuple[float] = None

	major 	: int = 10
	minor 	: range = range(1,10)

	scale 	: str = field(
		repr = False,
		default = "linear",
		)

	spot 	: int = field(
		repr = False,
		default = 0,
		)

	def __post_init__(self):

		if self.limit is not None:
			return

		if self.scale=="linear":
			object.__setattr__(self,'limit',(0,20))
		elif self.scale=="log10":
			object.__setattr__(self,'limit',(1,100))

	@property
	def lower(self):
		return min(self.limit)

	@property
	def upper(self):
		return max(self.limit)

	@property
	def length(self):
		"""Returns the length of axis."""
		return self.upper-self.lower
	
	@property
	def flip(self):
		"""Returns the lower and upper end of axis."""
		return self.limit != tuple(sorted(self.limit))

	def curve(self,data:numpy.ndarray,**kwargs):
		"""Returns an instance of Curve that carries only data information."""
		return Curve(data,**kwargs)

	def __call__(self,data:numpy.ndarray,**kwargs):
		"""Returns the axis values and limit (left,right) for the data."""

		curve = Curve(data,**kwargs)

		if self.scale == "linear":
			multp = curve.ufloor(self.length/curve.length)
		elif self.scale == "log10":
			multp = 10**curve.uceil(-numpy.log10(curve.lower))

		if self.scale == "linear":
			trail = self.lower+(curve.upper-data if flip else data-curve.lower)*multp
		elif self.scale == "log10":
			trail = data*multp

		object.__setattr__(curve,'trail',trail)

		return curve

if __name__ == "__main__":

	axis = BaseAxis(scale="log")

	print(axis.scale)
	print(axis)