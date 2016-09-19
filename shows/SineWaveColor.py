from HelperFunctions import*
from color import*
from math import sin, cos, pi

class SineWaveColor(object):
	def __init__(self, squaremodel):
		self.name = "SineWaveColor"
		self.square = squaremodel
		self.speed = 0.1
		self.color = randColor()
		self.counter = 0
		self.wave_speed = randint(1, 10)
		self.wag_speed = randint(10, 50)
		self.decay = randint(1,10) / 20.0
		self.color_x = randint(10, 20)
		self.freq1 = randint(1, 4)


	def next_frame(self):

		self.square.clear()

		while (True):
			for x in range(self.square.width):
				waggle = sin(2 * pi * self.get_fract(self.counter, self.wag_speed))  # Up and Down motion results = -1 to +1
				angle = self.freq1 * pi * self.get_fract(x + (self.counter * (self.wave_speed / 10.0)), self.square.width)
				y_top = (sin(angle) * waggle + 0.9) * self.square.height / 2 # (-1 to 1) * (-1 to 1) + 1 = 0 to 2
				(r,g,b) = wheel(self.color)
				col = RGB(r,g,b)

				for y in range(self.square.height):
					col_copy = col.copy()
					col_copy.h -= (0.01 * abs(y - y_top))
					self.square.set_cell((x,y), (col_copy.r, col_copy.g, col_copy.b))

			# Change the colors
			if oneIn(10):
				self.color = randColorRange(self.color, 10)

			if oneIn(10):
				self.color_x = upORdown(self.color_x, 1, 10, 30)

			if oneIn(10) and waggle == 0:
				self.freq1 = upORdown(self.freq1, 0.1, 1, 4)

			self.counter -= 1
			yield self.speed  	# random time set in init function

	def get_fract(self, var, max_var):
		"""Return 0 - 1.0 the fraction a var is to max_var"""
		return (var % max_var) / float(max_var)