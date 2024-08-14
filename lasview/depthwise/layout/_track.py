from ._plane import Plane

class Trail():

	def __init__(self,head:dict=None,body:dict=None):

		self._head = Plane(**(head or {}))
		self._body = Plane(**(body or {}))

	@property
	def head(self):
		return self._head
	
	@property
	def body(self):
		return self._body

	@head.setter
	def head(self,value:dict):
		self._head = Plane(**value)

	@body.setter
	def body(self,value:dict):
		self._body = Plane(**value)

if __name__ == "__main__":

	pass

	# a = Track()
	
	# print(a.head)

	# a.apple = 7

	# print(a.head)