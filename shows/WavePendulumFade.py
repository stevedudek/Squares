from HelperFunctions import*
from math import sin, cos, pi
from color import randColor, randColorRange, changeColor

class WavePendulumFade(object):
	def __init__(self, squaremodel):
		self.name = "WavePendulumFade"
		self.square = squaremodel
		self.faders = Faders(squaremodel)
		self.speed = 0.01
		self.counter = 0
		self.color = randColor()
		self.min_freq = 10	# fastest pendulum does this many cycles in one loop
		self.cycle_time = 8	# speed of one cycle
		self.cycles = int(self.cycle_time / self.speed)
		self.gradient = 20
		          
	def next_frame(self):

		while (True):

			self.square.black_cells()

			for y in range(self.square.height):

				w = (self.min_freq + y) / float(self.cycles) # pendulum frequency
				x = int((cos(w * self.counter) + 1) * self.square.width / 2)

				self.faders.add_fader(changeColor(self.color, y * self.gradient / 1500.0), (x,y), intense=1.0, growing=False, change=0.05)

			self.faders.cycle_faders()

			self.counter += 1

			if self.counter % (int(2 * pi * self.cycles)) == 0:
				self.color = randColorRange(self.color, 0.15)
				self.gradient = upORdown(self.gradient, 5, 15, 40)

			yield self.speed  	# random time set in init function