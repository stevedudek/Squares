from HelperFunctions import*
from math import sin, cos, pi
from color import randColor, randColorRange, RGB
from random import choice

class Magnet(object):
	def __init__(self, squaremodel):
		self.name = "Magnet"
		self.square = squaremodel
		self.speed = 0.1
		self.counter = 0
		self.color = randColor()
		(self.a, self.b) = choice([(1,1), (1,2), (3,2), (5,4), (3, pi/2)])
		self.trail_length = 5
		self.full_cycle = 3 * 2 * pi
		self.white = RGB(255, 255, 255)
		self.bricks = Bricks(squaremodel)
		self.num_bricks = 80
		self.brick_length = 2
		          
	def next_frame(self):

		self.square.clear()

		for i in range(self.num_bricks):
			self.bricks.add_brick(randColorRange(self.color, 0.15), life=100000, pos=(self.square.rand_cell()),
							  length=self.brick_length, pitch=0.5, length_x=1, length_y=0, dx=0, dy=0)

		while (True):

			x_angle = sin(self.a * self.counter - (pi / 2.0))
			y_angle = sin(self.b * self.counter)

			x = int((x_angle + 1) * (self.square.width - 1) / 2.0)
			y = int((y_angle + 1) * (self.square.height - 1) / 2.0)

			self.adj_bricks((x,y))
			self.bricks.move_bricks()

			self.square.set_cell((x, y), self.white)
			self.square.set_cell((x+1, y), self.white)
			self.square.set_cell((x, y+1), self.white)
			self.square.set_cell((x+1, y+1), self.white)

			self.counter += (0.1 / (self.a + self.b))

			if self.counter > self.full_cycle:
				self.counter -= self.full_cycle
				(self.a, self.b) = choice([(1,1), (1,2), (3,2), (5,4), (3, pi/2)])

			yield self.speed

	def adj_bricks(self, coord):
		for b in self.bricks.get_bricks():
			b_coord = b.get_coord()
			b_x = coord[0] - b_coord[0]
			b_y = coord[1] - b_coord[1]
			dist = distance(coord, b_coord)
			if 2 < dist < 8:
				b.set_dx(b_x / (2 * dist * dist))
				b.set_dy(b_y / (2 * dist * dist))
				b.set_length_x(b_x / dist)
				b.set_length_y(b_y / dist)
			else:
				b.set_dx(0)
				b.set_dy(0)

