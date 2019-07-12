from HelperFunctions import*
from math import sin, cos, pi
from color import random_color, random_color_range

class SineWave(object):
	def __init__(self, squaremodel):
		self.name = "SineWave"
		self.square = squaremodel
		self.sparkles = Faders(squaremodel)
		self.speed = 0.1
		self.color = rand_color()
		self.counter = 0
		self.wag_speed = randint(25, 500)
		self.decay = randint(1,10) / 20.0

		          
	def next_frame(self):

		self.square.clear()

		while (True):
			self.square.black_all_cells()

			for x in range(self.square.width):
				waggle = sin(2 * pi * self.get_fract(self.counter, self.wag_speed))	# Up and Down motion results = -1 to +1
				angle = 2 * pi * self.get_fract(x + self.counter, self.square.width)
				y = int((sin(angle) * waggle + 1) * self.square.height / 2)	# (-1 to 1) * (-1 to 1) + 1 = 0 to 2

				self.sparkles.add_fader(random_color_range(self.color, 0.03), (x, y), 1.0, False, self.decay)

			self.sparkles.cycle_faders()

			# Change the colors
			if one_in(10):
				self.color = random_color_range(self.color, 0.007)

			self.counter -= 1
			yield self.speed  	# random time set in init function

	def get_fract(self, var, max_var):
		"""Return 0 - 1.0 the fraction a var is to max_var"""
		return (var % max_var) / float(max_var)