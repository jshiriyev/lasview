import numpy

class Unary():

	def power(x:float):
		"""
		Returns the tenth power that brings float point next to the first
		significant digit.
		"""
		return -int(numpy.floor(numpy.log10(abs(x))))

	def ceil(x:float,power:int=None):
		"""
		Returns the ceil value for the first significant digit by default.
		
		If the power is specified, it is used as a factor before ceiling.
		"""
		if power is None:
			power = Unary.power(x)

		return numpy.ceil(x*10**power)/10**power

	def floor(x:float,power:int=None):
		"""
		Returns the floor value for the first significant digit by default.
		
		If the power is specified, it is used as a factor before flooring.
		"""
		if power is None:
			power = Unary.power(x)

		return numpy.floor(x*10**power)/10**power

	def round(x:float,power:int=None):
		"""Returns the rounded value for the first significant digit."""
		
		if power is None:
			power = Unary.power(x)

		return numpy.round(x*10**power)/10**power

class Binary():

	def multp(limit:tuple[float],length:float=None,scale:str="linear"):
		"""Returns the multiplication factor that will bring the limit to the axis scale."""

		if scale == "linear" and length is None:
			return 1

		if scale == "linear":
			return Unary.floor(length/Binary.length(limit))

		if scale == "log":
			return 10**Unary.ceil(-numpy.log10(min(limit)))

	def limit(limit:tuple[float],power:int=None,flip:bool=False):
		"""
		Returns the limit by using the same power for lower and upper values.
		"""

		if power is None:
			power = Binary.power(limit)

		xmin = Unary.floor(min(limit),power).tolist()
		xmax = Unary.ceil(max(limit),power).tolist()

		return (xmax,xmin) if flip else (xmin,xmax)

	def cycle(limit:tuple[float],power=None,major=10.):

		limit = Binary.limit(limit,power)

		length = Binary.length(limit)

		return Unary.ceil(length/major)

	def power(limit:tuple[float]):
		"""
		Returns the tenth power that brings float point next to the first
		significant digit based on the absolutely largest value in the limit.
		"""
		return min([Unary.power(x) for x in limit])

	def length(limit:tuple[float]):
		"""
		Returns the length based on limits.
		"""
		return max(limit)-min(limit)

	def issorted(limit:tuple[float]):
		"""
		Retruns bool showing whether limit is sorted.
		"""
		return limit == tuple(sorted(limit))

class Multivar():

	def limit(data:numpy.ndarray,power:int=None,flip:bool=False):
		"""
		Returns the limit of the given dataset.
		"""
		xmin = numpy.nanmin(data)
		xmax = numpy.nanmax(data)

		return Binary.limit((xmin,xmax),power=power,flip=flip)

	def cycle(data:numpy.ndarray,power=None,major=10):

		limit = Multivar.limit(data,power)

		length = Binary.length(limit)

		return Unary.ceil(length/major)

if __name__ == "__main__":

	print(Unary.power(0.001223))
	print(Unary.power(122.3))

	print(Unary.ceil(0.001223))
	print(Unary.ceil(122.3))

	print(Unary.floor(0.001223))
	print(Unary.floor(122.3))

	print(Unary.round(0.001223))
	print(Unary.round(122.3))

	print(Unary.round(0.001523))
	print(Unary.round(152.3))

	print(Binary.power((0.1,100)))
	print(Unary.power(100))
	print(Unary.power(0.1))

	print(Binary.limit((0.1,100)))
	print(Binary.limit((100,0.1)))