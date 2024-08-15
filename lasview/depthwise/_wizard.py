import lasio

from .layout._layout import Layout

class Wizard(Layout):

	def __init__(self,lasfile:lasio.LASFile,**kwargs):
		"""It sets elements for different trails in the axes
		by inheritting everything from layout.

		lasfile : the file that is going to be visualized.
		"""
		super().__init__(**kwargs)

		self._lasfile = lasfile

	@property
	def lasfile(self):
		return self._lasfile

	@property
	def depth(self):
		return self._depth

	@depth.setter
	def depth(self,value:dict):
		self._depth = Depth(**value)

	@property
	def label(self):
		return self._label

	@label.setter
	def label(self,value:dict):
		self._label = Label(**value)
	

if __name__ == "__main__":

	layout = Layout(trails=5,curves=3,width=(2,),label_loc="top")

	print(layout.width)

	print(layout.head.curves)
	print(layout.head.height)
	print(layout.body.height)