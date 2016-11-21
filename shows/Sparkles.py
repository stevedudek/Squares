from color import randColor, randColorRange
from HelperFunctions import*

class Sparkles(object):
	def __init__(self, squaremodel):
		self.name = "Sparkles"
		self.square = squaremodel
		self.sparkles = Faders(squaremodel)
		self.speed = 0.2
		self.color = randColor()
		self.spark_num = self.square.squares * 20

	def next_frame(self):

		self.square.clear()

		while (True):

			while self.sparkles.num_faders() < self.spark_num:
				self.sparkles.add_fader(randColorRange(self.color, 0.05), self.square.rand_cell())

			self.sparkles.cycle_faders()

			# Change the colors
			if oneIn(100):
				self.color = randColorRange(self.color, 0.1)

			yield self.speed