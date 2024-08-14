import numpy

from ._base import BaseAxis

from ._utils import Binary

class Log(BaseAxis):

	def __init__(self,**kwargs):

		super().__init__(scale="log",**kwargs)

	@property
	def lower(self):
		"""Returns the lower end value of axis."""
		return 1+self.skip.lower
	
	@property
	def upper(self):
		"""Returns the upper end value of axis."""
		return (1+self.skip.upper)*10**self.cycle

	def __call__(self,data:numpy.ndarray,limit:tuple=None):
		"""Returns the axis values and limit (left,right) for the data."""

		if limit is None:
			limit = Binary.limit((numpy.nanmin(data),numpy.nanmax(data)))

		multp = Binary.multp(limit,self.length,scale="log")

		return data*multp,tuple([x/multp for x in self.limit])
