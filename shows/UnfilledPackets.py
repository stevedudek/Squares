from HelperFunctions import*
from math import sin, cos, pi

class UnfilledPackets(object):
	def __init__(self, squaremodel):
		self.name = "UnfilledPackets"
		self.square = squaremodel
		self.sparkles = []  # List that holds Sparkle objects
		self.speed = randint(1,5) / 10.0
		self.color = randColor()
		self.counter = 0
		self.wave_speed = randint(1, 10)
		self.wag_speed = randint(10, 50)
		self.decay = randint(1,10) / 20.0
		self.color_x = randint(1, 4)
		self.color_y = randint(1, 10)
		self.freq = randint(1,6)

		          
	def next_frame(self):

		self.square.clear()

		while (True):
			self.square.black_cells()

			waggle = sin(2 * pi * self.get_fract(self.counter, self.wag_speed))  # Up and Down motion results = -1 to +1

			for x in range(self.square.width):
				angle = self.freq * pi * self.get_fract(x, 24)
				y_top = 0.5 + ((sin(angle) * waggle + 0.8) * self.square.height / 2)  # (-1 to 1) * (-1 to 1) + 1 = 0 to 2
				y_bottom = self.square.height - y_top - 1

				for y in range(self.square.height):
					if y < y_bottom or y > y_top:
						color = wheel(self.color + (self.color_x * x) + (self.color_y * y))
					else:
						color = wheel(self.color - (self.color_x * x) - (self.color_y * y))

					self.square.set_cell((x, y), color)

			# Change the colors
			if oneIn(10):
				self.color = randColorRange(self.color, 10)

			if oneIn(10):
				self.color_x = upORdown(self.color_x, 2, 1, 30)

			if oneIn(10):
				self.color_y = upORdown(self.color_y, 2, 1, 30)

			if waggle == 0:
				self.freq = randint(1,4)

			self.counter -= 1
			yield self.speed  	# random time set in init function

	def get_fract(self, var, max_var):
		"""Return 0 - 1.0 the fraction a var is to max_var"""
		return (var % max_var) / float(max_var)