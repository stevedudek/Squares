from HelperFunctions import*
from color import randColor, randColorRange, changeColor
from math import sin, cos, pi

class Diagonals3(object):
	def __init__(self, squaremodel):
		self.name = "Diagonals3"
		self.square = squaremodel
		self.bricks = Bricks(squaremodel)
		self.speed = 0.2
		self.color = randColor()
		self.density = randint(2,10)
		self.length = 0
		self.fade = 1.0 / randint(2, 10)
		self.life = self.square.height * 2
		          
	def next_frame(self):

		while (True):

			if oneIn(self.density):
				base_color = randColorRange(self.color, 0.05)
				x = randint(0, self.square.width)
				width = randint(2,5)
				for i in range(width):
					color = changeColor(base_color, i * 0.01)
					self.bricks.add_brick(color, life=self.life, pos=(x+i, 0), length=self.length, pitch=1, length_x=-1, length_y=-1, dx=1, dy=1, use_faders=True, change=self.fade)
					self.bricks.add_brick(color, life=self.life, pos=(x+i, 0), length=self.length, pitch=1, length_x=1, length_y=-1, dx=-1, dy=1, use_faders=True, change=self.fade)
					self.bricks.add_brick(color, life=self.life, pos=(x+i, self.square.height), length=self.length, pitch=1, length_x=-1, length_y=1, dx=1, dy=-1, use_faders=True, change=self.fade)
					self.bricks.add_brick(color, life=self.life, pos=(x+i, self.square.height), length=self.length, pitch=1, length_x=1, length_y=1, dx=-1, dy=-1, use_faders=True, change=self.fade)

			self.bricks.move_bricks(refresh=False)

			# Change the colors
			if oneIn(10):
				self.color = randColorRange(self.color, 0.2)

			if oneIn(50):
				self.fade = upORdown(self.fade, 1, 2, 10)

			if oneIn(50):
				self.density = upORdown(self.density, 1, 2, 10)

			yield self.speed  	# random time set in init function