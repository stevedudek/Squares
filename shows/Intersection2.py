from HelperFunctions import*
from color import random_color, random_color_range, dim_color

class Intersection2(object):
	def __init__(self, squaremodel):
		self.name = "Intersection2"
		self.square = squaremodel
		self.bricks = Bricks(squaremodel)
		self.speed = 0.2
		self.color1 = rand_color()
		self.color2 = rand_color()
		self.brick_speed = [randint(5, 20) / 20.0 for i in range(4)]
		self.density = randint(1,8)
		          
	def next_frame(self):

		self.square.clear()

		# 0 = left
		# 1 = right
		# 2 = bottom
		# 3 = top

		while (True):

			for i in range(self.density):
				brick_length = randint(3,7)

				side = True if one_in(2) else False
				color = self.color1 if side else self.color2
				if randint(0, self.square.height + self.square.width) < self.square.height:
					i = 0 if side else 1
				else:
					i = 2 if side else 3

				new_color = dim_color(random_color_range(color, brick_length / 150.0), 0.6)

				if i == 0:	# left
					self.bricks.add_brick(new_color,
										  life=20 + (self.square.width / self.brick_speed[i]),
										  pos=(-brick_length, randint(0, self.square.height)),
										  length=brick_length, pitch=1, length_x=1, length_y=0, dx=self.brick_speed[i], dy=0)
				elif i == 1:	# right
					self.bricks.add_brick(new_color,
										  life=20 + (self.square.width / self.brick_speed[i]),
										  pos=(self.square.width, randint(0, self.square.height)),
										  length=brick_length, pitch=1, length_x=1, length_y=0, dx=-self.brick_speed[i], dy=0)
				elif i == 2:	# bottom
					self.bricks.add_brick(new_color,
										  life=20 + (self.square.width / self.brick_speed[i]),
										  pos=(randint(0, self.square.width), -brick_length),
										  length=brick_length, pitch=1, length_x=0, length_y=1, dx=0, dy=self.brick_speed[i])
				else:	# top
					self.bricks.add_brick(new_color,
										  life=20 + (self.square.width / self.brick_speed[i]),
										  pos=(randint(0, self.square.width), self.square.height),
										  length=brick_length, pitch=1, length_x=0, length_y=1, dx=0, dy=-self.brick_speed[i])

			self.bricks.move_bricks()

			# Change the colors
			if one_in(20):
				self.color1 = random_color_range(self.color1, 0.05)

			if one_in(10):
				self.color1 = random_color_range(self.color1, 0.02)

			if one_in(100):
				self.density = up_or_down(self.density, 1, 1, 8)

			if one_in(500):
				self.brick_speed = [randint(5, 20) / 20.0 for i in range(4)]

			yield self.speed