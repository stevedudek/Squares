from HelperFunctions import*
from color import randColor, randColorRange
from util import make_interpolater


class XtoY(object):
	def __init__(self, squaremodel):
		self.name = "XtoY"
		self.square = squaremodel
		self.diags = Bricks(squaremodel)
		self.diagdensity = randint(2,10)
		self.speed = 0.1
		self.color = randColor()
		self.brick_color = randColor()
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
					self.square.set_cell((new_x, new_y), gradient_wheel(self.color, interp_func(x_fact ** y_fact)))

			if oneIn(self.diagdensity):
				brick_x = randint(-self.square.height, self.square.width - self.square.height)
				brick_length = randint(3,8)
				brick_color = randColorRange(self.brick_color, 0.1)
				self.diags.add_brick(brick_color, life=100, pos=(brick_x, self.square.height),
									 length=brick_length, pitch=1, length_x=-1, length_y=1, dx=1, dy=-1)
				self.diags.add_brick(randColorRange(brick_color, 0.1), life=100, pos=(brick_x + 1, self.square.height),
									 length=brick_length, pitch=1, length_x=-1, length_y=1, dx=1, dy=-1)

			self.diags.move_bricks(False)

			# Change the colors
			if oneIn(10):
				self.color = randColorRange(self.color, 0.01)

			if oneIn(2):
				self.x_center = upORdown(self.x_center, 1, 0, self.square.width)

			if oneIn(2):
				self.y_center = upORdown(self.y_center, 1, 0, self.square.height)

			yield self.speed