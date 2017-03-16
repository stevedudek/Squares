from HelperFunctions import*
from color import randColor, randColorRange, changeColor, dim_color
from math import sin, cos, pi

class FilledSineWave(object):
	def __init__(self, squaremodel):
		self.name = "FilledSineWave"
		self.square = squaremodel
		self.sparkles = []  # List that holds Sparkle objects
		self.speed = 0.1
		self.color = randColor()
		self.counter = 0
		self.wave_speed = randint(1, 10)
		self.wag_speed = randint(40, 80)
		self.decay = randint(1,10) / 20.0
		self.color_x = randint(1, 20)
		self.color_y = randint(1, 20)

		          
	def next_frame(self):

		while (True):
			self.square.black_cells()

			for x in range(self.square.width):
				waggle = sin(2 * pi * self.get_fract(self.counter, self.wag_speed))  # Up and Down motion results = -1 to +1
				angle = 2 * pi * self.get_fract(x + (self.counter * (self.wave_speed / 10.0)), self.square.width)
				y_top = (sin(angle) * waggle + 0.9) * self.square.height / 2 # (-1 to 1) * (-1 to 1) + 1 = 0 to 2

				for y in range(self.square.height):
					if y <= y_top:
						self.square.set_cell((x,y), dim_color(changeColor(self.color, (self.color_x * x / 1000.0) + (self.color_y * y / 1000.0)), 0.5))

			# Change the colors
			if oneIn(10):
				self.color = randColorRange(self.color, 0.005)

			if oneIn(10):
				self.color_x = upORdown(self.color_x, 1, 1, 30)

			if oneIn(10):
				self.color_y = upORdown(self.color_y, 1, 1, 30)

			self.counter -= 1
			yield self.speed  	# random time set in init function

	def get_fract(self, var, max_var):
		"""Return 0 - 1.0 the fraction a var is to max_var"""
		return (var % max_var) / float(max_var)