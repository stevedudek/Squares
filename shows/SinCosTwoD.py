from HelperFunctions import*
from math import sin, cos, pi
from color import randColor, randColorRange

class SinCosTwoD(object):
	def __init__(self, squaremodel):
		self.name = "SinCosTwoD"
		self.square = squaremodel
		self.speed = 0.15
		self.color = randColor()
		self.counter = 0
		self.repeat = randint(1,4)
		self.wag_speed = randint(10, 50)

		          
	def next_frame(self):

		self.square.clear()

		while (True):
			waggle = sin(2 * pi * self.get_fract(self.counter, self.wag_speed))  # Up and Down motion results = -1 to +1

			for x in range(self.square.width):
				for y in range(self.square.height):
					intensity = sin(float(x) / self.repeat) * cos(float(y) / self.repeat)	# -1 to 1

					spread = (0.25 + (intensity * waggle)) / 2	 # (-1 to 1) * (-1 to 1) + 1 = 0 to 2 / 2 = 0 to 1

					self.square.set_cell((x, y), gradient_wheel(self.color, spread))

			if waggle == 0 and oneIn(10):
				self.repeat = upORdown(self.repeat, 1, 1, 4)

			# Change the colors
			if oneIn(10):
				self.color = randColorRange(self.color, 0.007)

			self.counter += 1
			yield self.speed

	def get_fract(self, var, max_var):
		"""Return 0 - 1.0 the fraction a var is to max_var"""
		return (var % max_var) / float(max_var)