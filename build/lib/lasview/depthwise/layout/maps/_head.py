from lasview.depthwise.layout.axis._xaxis import Xaxis
from lasview.depthwise.layout.axis._label import Label

class Head():

	def __init__(self,xaxis:dict=None,yaxis:dict=None):

		self._xaxis = Xaxis(**(xaxis or {}))
		self._yaxis = Label(**(yaxis or {}))

	@property
	def xaxis(self):
		return self._xaxis
	
	@property
	def yaxis(self):
		return self._yaxis

	@xaxis.setter
	def xaxis(self,value:dict):
		self._xaxis = Xaxis(**value)

	@yaxis.setter
	def yaxis(self,value:dict):
		self._yaxis = Label(**value)