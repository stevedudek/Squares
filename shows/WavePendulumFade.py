from HelperFunctions import*
from math import sin, cos, pi

class WavePendulumFade(object):
	def __init__(self, squaremodel):
		self.name = "WavePendulumFade"
		self.square = squaremodel
		self.sparkles = []  # List that holds Sparkle objects
		self.speed = 0.05
		self.counter = 0
		self.color = randColor()
		self.min_freq = 10	# fastest pendulum does this many cycles in one loop
		self.cycle_time = 8	# speed of one cycle
		self.cycles = int(self.cycle_time / self.speed)
		self.gradient = 3
		          
	def next_frame(self):

		while (True):

			self.square.black_cells()

			for y in range(self.square.height):

				w = (self.min_freq + y) / float(self.cycles) # pendulum frequency
				x = int((cos(w * self.counter) + 1) * self.square.width / 2)

				self.square.set_cell((x, y), wheel(self.color + (y * self.gradient)))

			self.counter += 1
			if self.counter % (int(2 * pi * self.cycles)) == 0:
				self.color = randColorRange(self.color, 100)
				self.gradient = upORdown(self.gradient, 1, 1, 8)

			yield self.speed  	# random time set in init function