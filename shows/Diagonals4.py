from HelperFunctions import*
from color import randColor, randColorRange, changeColor, RGB
from math import sin, cos, pi

class Diagonals4(object):
	def __init__(self, squaremodel):
		self.name = "Diagonals4"
		self.square = squaremodel
		self.bricks = Bricks(squaremodel, bounce=True)
		self.speed = 0.15
		self.color = randColor()
		self.density = randint(1,6)
		self.fade = randint(4, self.square.width)
		self.life = 100
		          
	def next_frame(self):

		while (True):

			if oneIn(self.density):
				color = randColorRange(self.color, 0.01)
				change = 1.0 / self.fade
				x = randint(0, self.square.width)

				self.bricks.add_brick(color, life=self.life, pos=(x, 0), length=0, pitch=1, length_x=-1, length_y=-1, dx=1, dy=1, use_faders=True, change=change)
				self.bricks.add_brick(color, life=self.life, pos=(x, 0), length=0, pitch=1, length_x=1, length_y=-1, dx=-1, dy=1, use_faders=True, change=change)
				self.bricks.add_brick(color, life=self.life, pos=(x, self.square.height), length=0, pitch=1, length_x=-1, length_y=1, dx=1, dy=-1, use_faders=True, change=change)
				self.bricks.add_brick(color, life=self.life, pos=(x, self.square.height), length=0, pitch=1, length_x=1, length_y=1, dx=-1, dy=-1, use_faders=True, change=change)

			self.bricks.move_bricks()

			# Change the colors
			if oneIn(10):
				self.color = randColorRange(self.color, 0.2)

			if oneIn(100):
				self.density = upORdown(self.density, 1, 1, 6)

			if oneIn(20):
				self.fade = upORdown(self.fade, 2, 4, self.square.width)

			yield self.speed  	# random time set in init function