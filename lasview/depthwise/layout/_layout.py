from ._axis import Axis

from ._box import Box

from ._trail import Trail

class Layout():

	def __init__(self,x:int=3,y:int=3,/,depth_loc:int=1,label_loc:str="top",width:tuple[float]=None,height:tuple[float]=None):
		"""
		It sets elements for different trails in the axes:

		x			: number of trails including depth trail in the figure, integer
		y			: maximum number of curves in trails, integer

		depth_loc   : location of depth trail, integer
		label_loc 	: location of label head, top, bottom or None

		width       : width of trail, len(width) must be equal to either one,
					  two or the number of trails; tuple of floats

		height      : height per label row and height per unit distance,
					  len(height) must be equal to two; tuple of floats
	
		"""

		self._trails = [Trail() for _ in range(x)]

		self._depth_loc = depth_loc
		self._label_loc = label_loc

		self._width = self.get_width(width,trails,depth_loc)

		self._height = self.get_height(height)

	def __len__(self):
		return self._trails.__len__()

	@property
	def shape(self):
		return (self.__len__(),self._curves)
	

	def set_label(self,**kwargs):
		self._label = Axis(**kwargs)

	def set_depth(self,**kwargs):
		self._depth = Axis(**kwargs)

	def set_trail(self,index,**kwargs):

		xaxis = Axis(**kwargs)

		self._trail[index] = Trail(
			head=Box(xaxis=xaxis,yaxis=self._label),
			body=Box(xaxis=xaxis,yaxis=self._depth),
			)

	def __getitem__(self,index):
		return self._xaxes[index]

	@property
	def depth_loc(self):
		return self._depth_loc

	@property
	def label_loc(self):
		return self._label_loc

	@property
	def width(self):
		return self._width

	@property
	def height(self):
		return self._height

	@property
	def depth(self):
		return self._depth

	@property
	def label(self):
		return self._label

	@property
	def figsize(self):

		return (sum(self._width),sum([h*g for h,g in zip(self.height,(self.curves,self.depth.length))]))

	@staticmethod
	def get_width(width:tuple[float],trails:int=3,depth_loc:int=1):

		if width is None:
			return Layout.get_width((2,4),trails,depth_loc)

		if len(width)==1:
			return width*trails

		if len(width)==2:
			_width = list((width[1],)*trails)
			_width[depth_loc] = width[0]
			return tuple(_width)

		if len(width)==trails:
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