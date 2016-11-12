from HelperFunctions import*
from math import sin, cos, pi

class WavePendulumFilled(object):
	def __init__(self, squaremodel):
		self.name = "WavePendulumFilled"
		self.square = squaremodel
		self.speed = 0.05
		self.counter = 0
		self.color = randColor()
		self.min_freq = 10	# fastest pendulum does this many cycles in one loop
		self.cycle_time = 5	# speed of one cycle
		self.cycles = int(self.cycle_time / self.speed)
		self.gradient = 10
		self.up_down = True
		          
	def next_frame(self):

		while (True):

			for x in range(self.square.width):

				w = (self.min_freq + x) / float(self.cycles)	# pendulum frequency
				y_top = (cos(w * self.counter) + 1) * self.square.height / 2

				for y in range(self.square.height):
					if self.up_down:
						c = wheel(self.color + (x * self.gradient)) if y < y_top else (0,0,0)
					else:
						c = wheel(self.color + (x * self.gradient)) if y > y_top else (0,0,0)

					self.square.set_cell((x, y), c)

			self.counter += 1
			if self.counter % (int(2 * pi * self.cycles)) == 0:
				self.min_freq = upORdown(self.min_freq, 1, 3, 10)
				self.gradient = upORdown(self.gradient, 2, 5, 15)
				self.color = randColorRange(self.color, 10)
				self.up_down = not self.up_down

			yield self.speed  	# random time set in init function