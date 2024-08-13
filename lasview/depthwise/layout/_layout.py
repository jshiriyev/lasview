from ._axis import Axis
from ._axis import Depth
from ._axis import Label

from ._box import Box

from ._trail import Trail

class Layout():

	def __init__(self,ntrails : int = 3,/,
					  ncurves : int = 3,
					    depth : dict = None,
					    label : dict = None,
					    width : tuple[int] = None,
					   height : tuple[int] = None,
					  ):
		"""It sets elements for different trails in the axes:

		ntrails : number of trails including depth trail in the figure, integer
		ncurves : maximum number of curves in trails

		depth 	: dictionary containing location and axis key-value pairs
		label 	: dictionary containing location (head, top, bottom or None) and axis key-value pairs

		width 	: width of trail, len(width) must be equal to either one,
				two or the number of trails; tuple of ints

		height 	: height per label row and height per unit distance,
				len(height) must be equal to two; tuple of ints
		"""

		self._ntrails = ntrails
		self._ncurves = ncurves

		self._depth = Depth(**(depth or {}))
		self._label = Label(**(label or {}))

		# Setting the width tuple of the layout
		self._width  = self.get_width(width)

		# Setting the height tuple of the layout
		self._height = self.get_height(height)

		self._trails = [Trail(width=w,height=self.height) for w in self.width]

	@property
	def ntrails(self):
		return self._ntrails

	def __len__(self):
		return self._trails.__len__()

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

	@property
	def height(self):

		head_height = self.height[0]*self.ncurves
		body_height = self.height[1]*self.depth.length

		return (head_height,body_height)

	@property
	def size(self):
		return (sum(self.width),sum(self.height))

	def set(self,index:int,**kwargs):

		self[index] = Axis(**kwargs)

	def __setitem__(self,index:int,xaxis:Axis):

		self._trails[index] = Trail(
			head=Box(xaxis=xaxis,yaxis=self.label.axis),
			body=Box(xaxis=xaxis,yaxis=self.depth.axis),
			)

	def __getitem__(self,index):
		return self._trails[index]

	def get_width(self,width:tuple[float]):

		if width is None:
			return Layout.get_width((2,4))

		if len(width)==1:
			return width*self.ntrails

		if len(width)==2:
			_width = list((width[1],)*self.ntrails)
			_width[self.depth.spot] = width[0]
			return tuple(_width)

		if len(width)==self.ntrails:
			return width

		raise Warning("Length of width and number of columns does not match")
		
	@staticmethod
	def get_height(height:tuple[float]):

		if height is None:
			height = (1.,0.5)

		return height

if __name__ == "__main__":

	layout = Layout(trails=5,curves=3,width=(2,),label_loc="top")

	print(layout.width)

	print(layout.head.curves)
	print(layout.head.height)
	print(layout.body.height)