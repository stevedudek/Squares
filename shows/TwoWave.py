from HelperFunctions import*
from math import sin, cos, pi
from color import random_color, random_color_range
from random import choice

class TwoWaves(object):
	def __init__(self, squaremodel):
		self.name = "TwoWaves"
		self.square = squaremodel
		self.sparkles = Faders(squaremodel)
		self.speed = 0.1
		self.color1 = rand_color()
		self.color2 = rand_color()
		self.counter = 0
		self.freq1 = choice([0.5, 1, 2, 4])
		self.freq2 = choice([0.5, 1, 2, 4])
		          
	def next_frame(self):

		self.square.clear()

		while (True):

			for x in range(self.square.width):
				waggle = sin(2 * pi * (self.counter % 100) / 100)
				waggle2 = cos(2 * pi * (self.counter % 100) / 100)
				y = round((sin((x + self.counter) / (self.freq1 * pi)) * waggle + 1) * (self.square.height-1) / 2)
				y2 = round((cos((x + self.counter) / (self.freq2 * pi)) * waggle2 + 1) * (self.square.height-1) / 2)

				for i in range(2):
					self.sparkles.add_fader(random_color_range(self.color1, 0.02), (x - i, y), 0.5, False, 0.05)
					self.sparkles.add_fader(random_color_range(self.color2, 0.02), (x - i, y2), 0.5, False, 0.05)

			self.sparkles.cycle_faders()

			# Change the colors
			if one_in(10):
				self.color1 = random_color_range(self.color1, 0.01)

			if one_in(5):
				self.color2 = random_color_range(self.color2, 0.01)

			self.counter -= 1
			yield self.speed  	# random time set in init function