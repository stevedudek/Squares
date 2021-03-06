from HelperFunctions import*
from color import random_color, random_color_range

class Snowglobe2(object):
	def __init__(self, squaremodel):
		self.name = "Snowglobe2"
		self.square = squaremodel
		self.speed = 0.03
		self.counter = 0
		self.color = rand_color()
		self.bricks = Bricks(squaremodel)
		self.num_bricks = self.square.width * randint(5,20)
		self.brick_length = 2
		          
	def next_frame(self):

		self.square.clear()

		for i in range(self.num_bricks):
			self.bricks.add_brick(random_color_range(self.color, 0.1), life=100000, pos=(self.square.rand_cell()),
								  length=self.brick_length, pitch=1, length_x=0, length_y=1, dx=0, dy=0, accel_y=-0.1)

		while (True):

			while (True):
				self.counter += 1
				self.bricks.move_bricks()
				for b in self.bricks.get_bricks():
					if b.get_coord()[1] < 0:
						b.set_y(0)

				if one_in(50) and self.counter > 50:
					self.counter = 0
					for b in self.bricks.get_bricks():
						b.set_dy(randint(10,40) / 10.0)

				yield self.speed
