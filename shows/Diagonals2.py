from HelperFunctions import*
from color import randColor, randColorRange, changeColor
from math import sin, cos, pi

class Diagonals2(object):
	def __init__(self, squaremodel):
		self.name = "Diagonals2"
		self.square = squaremodel
		self.bricks = Bricks(squaremodel)
		self.speed = 0.4
		self.color = randColor()
		self.density = randint(1,3)
		self.length = randint(1,5)
		self.life = self.square.height
		          
	def next_frame(self):

		while (True):


			for i in range(self.density):
				color = randColorRange(self.color, 0.05)
				x = randint(0, self.square.width)
				# add_brick(self, color, life, pos, length, pitch, length_x, length_y, dx, dy, accel_x=0, accel_y=0, use_faders=False, change=0.25):
				self.bricks.add_brick(color, life=self.life, pos=(x,0), length=self.length, pitch=1, length_x=-1, length_y=-1, dx=1, dy=1, use_faders=True, change=0.25)
				self.bricks.add_brick(color, life=self.life, pos=(x,0), length=self.length, pitch=1, length_x=1, length_y=-1, dx=-1, dy=1, use_faders=True, change=0.25)
				self.bricks.add_brick(color, life=self.life, pos=(x, self.square.height), length=self.length, pitch=1, length_x=-1, length_y=1, dx=1, dy=-1, use_faders=True, change=0.25)
				self.bricks.add_brick(color, life=self.life, pos=(x, self.square.height), length=self.length, pitch=1, length_x=1, length_y=1, dx=-1, dy=-1, use_faders=True, change=0.25)

			self.bricks.move_bricks()

			# Change the colors
			if oneIn(10):
				self.color = randColorRange(self.color, 0.2)

			if oneIn(100):
				self.density = upORdown(self.density, 1, 1, 3)

			if oneIn(50):
				self.density = upORdown(self.length, 1, 1, 5)

			yield self.speed  	# random time set in init function