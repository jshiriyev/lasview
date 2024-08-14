import numpy

from ._base import BaseAxis

from ._utils import Binary, Multivar

class Linear(BaseAxis):

	def __init__(self,**kwargs):

		super().__init__(**kwargs)

	@property
	def lower(self):
		"""Returns the lower end value of axis."""
		return self.skip.lower
	
	@property
	def upper(self):
		"""Returns the upper end value of axis."""
		return self.cycle*10+self.skip.upper

	def __call__(self,data:numpy.ndarray,limit:tuple=None,multp:float=None,flip:bool=False):
		"""Returns the axis values and limit (left,right) for the data."""

		if limit is None:
			limit = Multivar.limit(data,flip)

		if multp is None:
			multp = Binary.multp(limit,self.length)

		delta = max(limit)-data if flip else data-min(limit)

		return self.lower+delta*multp,limit