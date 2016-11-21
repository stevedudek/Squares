from HelperFunctions import*
from math import sin, cos, pi
from color import randColor, randColorRange

class TwoWaves(object):
	def __init__(self, squaremodel):
		self.name = "TwoWaves"
		self.square = squaremodel
		self.sparkles = Faders(squaremodel)
		self.speed = 0.1
		self.color1 = randColor()
		self.color2 = randColor()
		self.counter = 0
		          
	def next_frame(self):

		self.square.clear()

		while (True):

			for x in range(self.square.width):
				waggle = sin(2*pi*(self.counter % 100) / 100)
				waggle2 = cos(2 * pi * (self.counter % 100) / 100)
				y = round((sin((x + self.counter) / (2*pi)) * waggle + 1) * self.square.height / 2)
				y2 = round((cos((x + self.counter) / (2 * pi)) * waggle2 + 1) * self.square.height / 2)

				self.sparkles.add_fader(randColorRange(self.color1, 0.02), (x, y), 1.0, False, 0.2)
				self.sparkles.add_fader(randColorRange(self.color2, 0.02), (x, y2), 1.0, False, 0.05)

			self.sparkles.cycle_faders()

			# Change the colors
			if oneIn(10):
				self.color1 = randColorRange(self.color1, 0.01)

			if oneIn(5):
				self.color2 = randColorRange(self.color2, 0.01)

			self.counter -= 1
			yield self.speed  	# random time set in init function