from HelperFunctions import*
from color import randColor, randColorRange, changeColor, dim_color
from math import sin, cos, pi

class Diagonals(object):
	def __init__(self, squaremodel):
		self.name = "Diagonals"
		self.square = squaremodel
		self.bricks = Bricks(squaremodel)
		self.speed = 0.25
		self.color = randColor()
		self.density = randint(1,4)
		self.length = randint(2,10)
		          
	def next_frame(self):

		while (True):


			for i in range(self.density):
				color = dim_color(randColorRange(self.color, 0.1), 0.5)
				x = randint(0, self.square.width)
				# add_brick(self, color, life, pos, length, pitch, length_x, length_y, dx, dy, accel_x=0, accel_y=0, use_faders=False, change=0.25):
				self.bricks.add_brick(color, 40, pos=(x,0), length=self.length, pitch=1, length_x=-1, length_y=-1, dx=1, dy=1)
				self.bricks.add_brick(color, 40, pos=(x,0), length=self.length, pitch=1, length_x=1, length_y=-1, dx=-1, dy=1)
				self.bricks.add_brick(color, 40, pos=(x, self.square.height), length=self.length, pitch=1, length_x=-1, length_y=1, dx=1, dy=-1)
				self.bricks.add_brick(color, 40, pos=(x, self.square.height), length=self.length, pitch=1, length_x=1, length_y=1, dx=-1, dy=-1)

			self.bricks.move_bricks()

			# Change the colors
			if oneIn(10):
				self.color = randColorRange(self.color, 0.2)

			if oneIn(100):
				self.density = upORdown(self.density, 1, 1, 4)

			if oneIn(50):
				self.length = upORdown(self.length, 1, 2, 10)

			yield self.speed  	# random time set in init function