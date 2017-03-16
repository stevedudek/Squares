from HelperFunctions import*
from math import sin, cos, pi
from color import randColor, randColorRange

class Packets(object):
	def __init__(self, squaremodel):
		self.name = "Packets"
		self.square = squaremodel
		self.sparkles = Faders(squaremodel)
		self.speed = 0.2
		self.color = randColor()
		self.counter = 0
		self.wave_speed = randint(1, 10)
		self.wag_speed = randint(10, 50)
		self.decay = randint(5,10) / 40.0
		self.color_x = randint(1, 20)
		self.color_y = randint(1, 20)

		          
	def next_frame(self):

		self.square.clear()

		while (True):
			self.square.black_cells()

			waggle = sin(2 * pi * self.get_fract(self.counter, self.wag_speed))  # Up and Down motion results = -1 to +1
			y_off = int(waggle * self.square.height * 0.5)

			for x in range(self.square.width):
				angle = 2 * pi * self.get_fract(x + (self.counter * (self.wave_speed / 5.0)), self.square.width)
				y_top = 0.5 + ((sin(angle) * waggle + 0.8) * self.square.height / 2)  # (-1 to 1) * (-1 to 1) + 1 = 0 to 2
				y_bottom = self.square.height - y_top - 1

				for y in range(self.square.height):
					if y_bottom <= y <= y_top:
						color = randColorRange(self.color, (self.color_x * x / 3000.0) + (self.color_y * y / 3000.0))
						self.sparkles.add_fader(color, (x, y + y_off), intense=1.0, growing=False, change=self.decay)

			self.sparkles.cycle_faders()

			# Change the colors
			if oneIn(10):
				self.color = randColorRange(self.color, 0.007)

			if oneIn(10):
				self.color_x = upORdown(self.color_x, 2, 1, 30)

			if oneIn(10):
				self.color_y = upORdown(self.color_y, 2, 1, 30)

			self.counter -= 1
			yield self.speed  	# random time set in init function

	def get_fract(self, var, max_var):
		"""Return 0 - 1.0 the fraction a var is to max_var"""
		return (var % max_var) / float(max_var)