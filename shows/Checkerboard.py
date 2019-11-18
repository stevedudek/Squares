from HelperFunctions import*
from random import randint

class Checkerboard(object):
	def __init__(self, squaremodel):
		self.name = "Checkerboard"
		self.square = squaremodel
		self.speed = 0.3
		self.color1 = randint(0, MAX_HUE)
		self.color2 = randint(0, MAX_HUE)

	def next_frame(self):

		self.square.clear()
		while (True):

			for x in range(self.square.width):
				for y in range(self.square.height):
					hue = self.color1 if (x + y) % 2 else self.color2
					self.square.set_cell((x,y), (hue, 255, 255))

			if one_in(10):
				self.color1 += 1

			yield self.speed