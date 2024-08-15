import numpy

from ._xaxis import Xaxis

class Depth(Xaxis):

	def __init__(self,**kwargs):
		super().__init__(**kwargs)

	def __call__(self,data:numpy.ndarray,**kwargs):
		return Curve(data,**kwargs)