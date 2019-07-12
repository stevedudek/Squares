from HelperFunctions import*
from math import sin, cos, pi
from color import random_color, random_color_range, change_color, dim_color

class SinCosColorTwoD(object):
	def __init__(self, squaremodel):
		self.name = "SinCosColorTwoD"
		self.square = squaremodel
		self.speed = 0.2
		self.color = rand_color()
		self.counter = 0
		self.repeat = randint(1,4)
		self.wag_speed = randint(20, 50)

		          
	def next_frame(self):

		self.square.clear()

		while (True):
			waggle = sin(2 * pi * self.get_fract(self.counter, self.wag_speed))  # Up and Down motion results = -1 to +1

			for x in range(self.square.width):
				for y in range(self.square.height):
					intensity = sin(float(x) / self.repeat) * cos(float(y) / self.repeat)	# -1 to 1
					spread = intensity * waggle	# (-1 to 1) * (-1 to 1) = -1 to 1

					self.square.set_cell((x, y), dim_color(change_color(self.color, spread * MAX_COLOR / 6000.0), 0.3))

			if waggle == 0 and one_in(10):
				self.repeat = up_or_down(self.repeat, 1, 1, 4)

			# Change the colors
			if one_in(10):
				self.color = random_color_range(self.color, 0.007)

			self.counter += 1
			yield self.speed

	def get_fract(self, var, max_var):
		"""Return 0 - 1.0 the fraction a var is to max_var"""
		return (var % max_var) / float(max_var)