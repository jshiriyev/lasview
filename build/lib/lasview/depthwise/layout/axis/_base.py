from dataclasses import dataclass, field

@dataclass
class Skip:
	"""BaseAxis property containing lower and upper skip amounts."""
	lower 	: int = 0
	upper 	: int = 0

@dataclass(frozen=True)
class BaseAxis:
	"""
	It initializes the axis of plane in a track plot:

	cycle 	: sets the number of cycles in the axis
			where the length of each cycle is ten.

	minor 	: sets the frequency of minor ticks

	skip 	: how many minor units to skip from lower and
			upper side, tuple of two integers, values may
			change in between (0-9), 0 means no skip.

	scale   : axis scale: linear or logarithmic, check the link below
			https://matplotlib.org/stable/users/explain/axes/axes_scales.html
			for the available scales in matplotlib.

	spot 	: location of axis in the layout, int

	"""

	cycle 	: int = 2

	major 	: int = 10
	minor 	: range = range(1,10)

	skip  	: tuple[int] = (0,0)

	scale 	: str = field(
		repr = False,
		default = "linear",
		)

	spot 	: int = field(
		repr = False,
		default = 0,
		)

	def __post_init__(self):

		object.__setattr__(self,'skip',Skip(*self.skip))

	@property
	def length(self):
		"""Returns the length of axis."""
		return self.upper-self.lower
	
	@property
	def limit(self):
		"""Returns the lower and upper end of axis."""
		return (self.lower,self.upper)

if __name__ == "__main__":

	axis = BaseAxis(scale="log")

	print(axis.scale)
	print(axis)