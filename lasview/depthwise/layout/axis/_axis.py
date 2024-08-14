import numpy

from ._linear import Linear

from ._log import Log

from ._utils import Multivar

def Axis(scale:str='linear',**kwargs):
	"""It returns either linear or log axis based on scale."""
	return Linear(**kwargs) if scale=="linear" else Log(**kwargs)

def Depth(values:numpy.ndarray,spot:int=1,**kwargs):
	"""It returns linear axis where the location is specified."""

	cycle = Multivar.cycle(values,power=-1)

	return Linear(spot=spot,cycle=cycle,**kwargs)

def Label(spot:int=0,**kwargs):
	"""It returns label axis where the location is specified."""
	return Linear(spot=spot,**kwargs)

if __name__ == "__main__":

	xaxis = Axis(scale="log",skip=(1,3))

	# print(xaxis.skip.upper)

	# print(xaxis.limit)

	# print(Axis.ceil(0.03573465))
	# print(Axis.floor(0.03573465))
	# print(Axis.round(0.03573465))

	# print(Axis.ceil(3459))
	# print(Axis.floor(3459))
	# print(Axis.round(3459))

	# print(Axis(cycle=2).get_multp((0.1,0.4)))
	# print(Axis(cycle=3).get_multp((0.1,0.5)))

	xaxis = Axis(cycle=1,skip=(6,0))

	data = numpy.array([0.61,0.7,0.8,0.9,0.99])

	data,limit = xaxis(data,limit=(1,0.6))

	print(data,limit)

	# print(Axis(cycle=1,skip=(6,0)).get_multp((0.1,0.4)))


