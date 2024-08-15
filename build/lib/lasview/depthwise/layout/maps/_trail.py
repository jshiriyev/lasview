from ._head import Head
from ._body import Body

class Trail():

	def __init__(self,head:dict=None,body:dict=None):

		self._head = Head(**(head or {}))
		self._body = Body(**(body or {}))

	@property
	def head(self):
		return self._head
	
	@property
	def body(self):
		return self._body

	@head.setter
	def head(self,value:dict):
		self._head = Head(**value)

	@body.setter
	def body(self,value:dict):
		self._body = Body(**value)

if __name__ == "__main__":

	pass