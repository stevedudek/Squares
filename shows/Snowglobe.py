from HelperFunctions import*
from math import sin, cos, pi

class Snowglobe(object):
	def __init__(self, squaremodel):
		self.name = "Snowglobe"
		self.square = squaremodel
		self.speed = 0.01
		self.counter = 0
		self.color = randColor()
		self.bricks = Bricks(squaremodel, True)
		self.num_bricks = 80
		          
	def next_frame(self):

		self.square.clear()

		for i in range(self.num_bricks):
			self.bricks.add_brick(wheel(randColorRange(self.color, 200)), life=100000, pos=(self.square.rand_cell()),
							  length=randint(1,4), pitch=1, length_x=1, length_y=0, dx=0, dy=0)

		while (True):

			while (True):
				self.bricks.move_bricks()
				self.bricks.set_all_accel_y(0.01 * sin(2 * pi * self.counter / 20))
				self.counter += 1

				yield self.speed
