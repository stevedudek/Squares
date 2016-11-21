from HelperFunctions import*
from color import randColor, changeColor

class VertLines(object):
	def __init__(self, squaremodel):
		self.name = "VertLines"
		self.square = squaremodel
		self.speed = randint(1,10) / 100.0
		self.color1 = randColor()
		self.color2 = randColor()
		          
	def next_frame(self):

		# self.square.clear()

		while (True):
			for x in range(self.square.width):
				for y in range(self.square.height):
					color = changeColor(self.color1,  - y * 0.02) if x % 2 else changeColor(self.color2, y * 0.02)
					self.square.set_cell((x,y), color)
			
			# Change the colors
			if oneIn(10):
				self.color1 = changeColor(self.color1, 0.007)

			if oneIn(2):
				self.color2 = changeColor(self.color2, -0.007)
			
			yield self.speed  	# random time set in init function