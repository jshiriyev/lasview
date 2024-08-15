import numpy

from ._xaxis import Xaxis

class Depth(Xaxis):

	def __init__(self,**kwargs):

		super().__init__(self,**kwargs)

	def __call__(self,data:numpy.ndarray,**kwargs):
		"""Returns an instance of Curve that carries only data information."""
		return Curve(data,**kwargs)