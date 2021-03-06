from HelperFunctions import*
from math import sin, cos, pi
from color import random_color, random_color_range

class Snowglobe(object):
	def __init__(self, squaremodel):
		self.name = "Snowglobe"
		self.square = squaremodel
		self.speed = 0.2
		self.counter = 0
		self.color = rand_color()
		self.bricks = Bricks(squaremodel, bounce=True)
		self.num_bricks = 48
		          
	def next_frame(self):

		self.square.clear()

		for i in range(self.num_bricks):
			self.bricks.add_brick(random_color_range(self.color, 0.1), life=100000, pos=(self.square.rand_cell()),
								  length=randint(2,8), pitch=1, length_x=0, length_y=0.5, dx=0, dy=randint(4,10) / 10.0)

		while (True):

			self.bricks.move_bricks()
			self.bricks.set_all_accel_y(0.1 * sin(2 * pi * self.counter / 20))
			self.counter += 1

			yield self.speed
