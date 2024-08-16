import lasio

from .layout._label import Label
from .layout._depth import Depth
from .layout._xaxis import Xaxis

from .layout._layout import Layout

def Wizard(lasfile:lasio.LASFile,**kwargs):

	layout = Layout(**kwargs)
	
def label(cycle:int=3,**kwargs):

	if kwargs.get("limit") is None:
		kwargs["limit"] = (0,10*cycle)

	return Label(**kwargs)

def depth(array:lasio.CurveItem,lower,upper,power,**kwargs):

	if kwargs.get("limit") is None:
		kwargs["limit"] = Datum(array,lower,upper,power).limit

	return Depth(**kwargs)

if __name__ == "__main__":

	layout = Layout(trails=5,curves=3,width=(2,),label_loc="top")

	print(layout.width)

	print(layout.head.curves)
	print(layout.head.height)
	print(layout.body.height)