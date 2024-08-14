from ._axis import Axis

class Plane():

	def __init__(self,xaxis:dict=None,yaxis:dict=None):

		self._xaxis = Axis(**(xaxis or {}))
		self._yaxis = Axis(**(yaxis or {}))

	@property
	def xaxis(self):
		return self._xaxis
	
	@property
	def yaxis(self):
		return self._yaxis

	@xaxis.setter
	def xaxis(self,value:dict):
		self._xaxis = Axis(**value)

	@yaxis.setter
	def yaxis(self,value:dict):
		self._yaxis = Axis(**value)

if __name__ == "__main__":

	pass