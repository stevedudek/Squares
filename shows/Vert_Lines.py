from HelperFunctions import*
from color import random_color, change_color, dim_color

class VertLines(object):
	def __init__(self, squaremodel):
		self.name = "VertLines"
		self.square = squaremodel
		self.speed = randint(1,10) / 100.0
		self.color1 = rand_color()
		self.color2 = rand_color()
		          
	def next_frame(self):

		# self.square.clear()

		while (True):
			for x in range(self.square.width):
				for y in range(self.square.height):
					color = change_color(self.color1, - y * 0.02) if x % 2 else change_color(self.color2, y * 0.02)
					self.square.set_cell((x,y), dim_color(color, 0.33))

			# Change the colors
			if one_in(10):
				self.color1 = change_color(self.color1, 0.007)

			if one_in(2):
				self.color2 = change_color(self.color2, -0.007)
			
			yield self.speed  	# random time set in init function