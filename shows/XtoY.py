from HelperFunctions import*
from color import random_color, random_color_range
from util import make_interpolater


class XtoY(object):
	def __init__(self, squaremodel):
		self.name = "XtoY"
		self.square = squaremodel
		self.diags = Bricks(squaremodel)
		self.diagdensity = randint(2,10)
		self.speed = 0.1
		self.color = rand_color()
		self.brick_color = rand_color()
		self.x_center = randint(0, self.square.width)
		self.y_center = randint(0, self.square.height)

		          
	def next_frame(self):

		interp_func = make_interpolater(0, 4, 0, 1)

		self.square.clear()

		while (True):
			for x in range(self.square.width):
				for y in range(self.square.height):
					new_x = (x + self.x_center) % self.square.width
					new_y = (y + self.y_center) % self.square.height

					x_fact = (x * 2.0 / self.square.width)
					y_fact = (y * 2.0 / self.square.height)
					self.square.set_cell((new_x, new_y), gradient_wheel(self.color, interp_func(x_fact ** y_fact) ** 2))

			if one_in(self.diagdensity):
				brick_x = randint(-self.square.height, self.square.width - self.square.height)
				brick_length = randint(3,8)
				brick_color = random_color_range(self.brick_color, 0.1)
				self.diags.add_brick(brick_color, life=100, pos=(brick_x, self.square.height),
									 length=brick_length, pitch=1, length_x=-1, length_y=1, dx=1, dy=-1)
				self.diags.add_brick(random_color_range(brick_color, 0.1), life=100, pos=(brick_x + 1, self.square.height),
									 length=brick_length, pitch=1, length_x=-1, length_y=1, dx=1, dy=-1)

			self.diags.move_bricks(False)

			# Change the colors
			if one_in(10):
				self.color = random_color_range(self.color, 0.01)

			if one_in(2):
				self.x_center = up_or_down(self.x_center, 1, 0, self.square.width)

			if one_in(2):
				self.y_center = up_or_down(self.y_center, 1, 0, self.square.height)

			yield self.speed