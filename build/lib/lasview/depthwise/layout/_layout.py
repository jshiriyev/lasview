from .axis._axis import Axis, Depth, Label

from ._plane import Plane
from ._trail import Trail

class Layout():

	def __init__(self,ntrails : int = 3,/,
					  ncurves : int = 3,
					    depth : dict = None,
					    label : dict = None,
					    width : tuple[float] = None,
					   height : tuple[float] = None,
					  ):
		"""It sets elements for different trails in the axes:

		ntrails : number of trails including depth trail in the figure, integer
		ncurves : maximum number of curves in trails, integer

		depth 	: dictionary containing spot (integer) and axis key-value pairs
		label 	: dictionary containing spot (head, top, bottom or None) and axis key-value pairs

		width 	: width of trail, len(width) must be equal to either one,
				two or the number of trails; tuple of float

		height 	: height per label row and height per unit distance,
				len(height) must be equal to two; tuple of float
		"""

		self._ntrails = ntrails
		self._ncurves = ncurves

		self._depth = Depth(**(depth or {}))
		self._label = Label(**(label or {}))

		# Setting the width tuple of the layout
		self.width = width

		# Setting the height tuple of the layout
		self.height = height

		self._xaxes = [Axis() for _ in range(self.ntrails)]

	@property
	def ntrails(self):
		return self._ntrails

	def __len__(self):
		return self._ntrails

	@property
	def ncurves(self):
		return self._ncurves
	
	@property
	def shape(self):
		return (self.ntrails,self.ncurves)

	@property
	def depth(self):
		return self._depth

	@property
	def label(self):
		return self._label

	@property
	def width(self):
		return self._width

	@width.setter
	def width(self,width:tuple[float]):

		if width is None:
			self.width = (2,4)

		elif len(width)==1:
			self._width = width*self.ntrails

		elif len(width)==2:

			wlist = list((width[1],)*self.ntrails)

			wlist[self.depth.spot] = width[0]

			self._width = tuple(wlist)

		elif len(width)==self.ntrails:
			self._width = width

		else:
			raise Warning("Length of width and number of columns does not match")

	@property
	def height(self):

		head_height = self._height[0]*self.ncurves
		body_height = self._height[1]*self.depth.length

		return (head_height,body_height)

	@height.setter
	def height(self,height:tuple[float]):

		self._height = (1.,0.5) if height is None else height

	@property
	def size(self):
		
		return (sum(self.width),sum(self.height))

	def set(self,index:int,**kwargs):

		self[index] = Axis(**kwargs)

	def __setitem__(self,index:int,xaxis:Axis):

		self._xaxes[index] = xaxis

	def __getitem__(self,index):

		return self._xaxes[index]

if __name__ == "__main__":

	layout = Layout(trails=5,curves=3,width=(2,),label_loc="top")

	print(layout.width)

	print(layout.head.curves)
	print(layout.head.height)
	print(layout.body.height)