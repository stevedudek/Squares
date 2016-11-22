from HelperFunctions import*
from math import sin, cos, pi
from color import randColor, randColorRange, changeColor

class SineCosine(object):
	def __init__(self, squaremodel):
		self.name = "SineCosine"
		self.square = squaremodel
		self.sparkles = []  # List that holds Sparkle objects
		self.speed = 0.1
		self.color1 = randColor()
		self.color2 = randColor()
		self.counter = 0
		self.wave_speed = randint(1, 10)
		self.wag_speed = randint(10, 50)
		self.decay = randint(1,10) / 20.0
		self.color_x = randint(1,20)
		self.color_y = randint(1, 20)
		self.freq1 = randint(1, 4)
		self.freq2 = randint(1, 4)

		          
	def next_frame(self):

		self.square.clear()

		while (True):
			self.square.black_cells()


			for x in range(self.square.width):

				sin_angle = self.freq1 * pi * self.get_fract(x + (self.counter * (self.wave_speed / 6.0)), self.square.width)
				y_sin_top = (sin(sin_angle) + 1.0) * self.square.height / 2.0 # (-1 to 1) * (-1 to 1) + 1 = 0 to 2

				cos_angle = self.freq2 * pi * self.get_fract(x - (self.counter * (self.wave_speed / 3.0)), self.square.width)
				y_cos_top = (sin(cos_angle) + 1.0) * self.square.height / 2.0  # (-1 to 1) * (-1 to 1) + 1 = 0 to 2

				for y in range(self.square.height):
					if y <= y_sin_top:
						self.square.set_cell((x, y), changeColor(self.color1, (self.color_x * x / 1500.0) + (self.color_y * y / 1500.0)))

					if y <= y_cos_top:
						self.square.set_cell((x, y), changeColor(self.color2, (self.color_x * y / 1500.0) + (self.color_y * x / 1500.0)))

			# Change the colors
			if oneIn(10):
				self.color1 = randColorRange(self.color1, 0.007)

			if oneIn(2):
				self.color2 = randColorRange(self.color2, 0.007)

			if oneIn(10):
				self.color_x = upORdown(self.color_x, 1, 1, 30)

			if oneIn(10):
				self.color_y = upORdown(self.color_y, 1, 1, 30)

			if oneIn(10):
				self.freq1 = upORdown(self.freq1, 0.05, 1, 4)

			if oneIn(10):
				self.freq2 = upORdown(self.freq2, 0.05, 1, 4)

			self.counter -= 1
			yield self.speed  	# random time set in init function

	def get_fract(self, var, max_var):
		"""Return 0 - 1.0 the fraction a var is to max_var"""
		return (var % max_var) / float(max_var)