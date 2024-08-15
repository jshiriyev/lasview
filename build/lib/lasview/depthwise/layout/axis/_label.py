from dataclasses import dataclass, field

import numpy

@dataclass(frozen=True)
class Label:
	"""
	It initializes the axis of plane in a track:

	cycle 	: number of curves
	
	major 	: sets the frequency of major ticks
	minor 	: sets the frequency of minor ticks

	spot 	: location of axis in the layout, int

	"""

	cycle 	: int = 3

	major 	: int = 10
	minor 	: range = range(1,10)

	spot 	: int = field(
		repr = False,
		default = 0,
		)

	@property
	def lower(self):
		return 0

	@property
	def upper(self):
		return self.cycle*10

	@property
	def limit(self):
		return (self.lower,self.upper)

	@property
	def length(self):
		"""Returns the length of axis."""
		return self.upper-self.lower