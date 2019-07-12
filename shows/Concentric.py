from HelperFunctions import*
from color import random_color, random_color_range, change_color

class Grower(object):
	def __init__(self, squaremodel, max_size, color, pos, gradient, type):
		self.square = squaremodel
		self.size = 0
		self.max_size = max_size
		self.color = color
		self.pos = pos
		self.gradient = gradient
		self.type = type

	def draw_grower(self):
		color = gradient_wheel(change_color(self.color, self.gradient * self.size), 0.4) if self.type \
			else gradient_wheel(self.color, 0.4 * float(self.max_size - self.size + 1) / self.max_size)
		self.square.draw_circle(self.pos, self.size, color)

	def grow_grower(self):
		self.size += 1
		return self.size <= self.max_size


class Concentric(object):
	def __init__(self, squaremodel):
		self.name = "Concentric"
		self.square = squaremodel
		self.growers = []
		self.max_growers = 10
		self.speed = 0.2
		self.color = rand_color()
		self.density = randint(4, 40)
		self.type = True

	def next_frame(self):

		self.square.clear()

		while (True):

			if len(self.growers) < 3 or one_in(self.density):
				self.growers.append(Grower(self.square, randint(3, 8), random_color_range(self.color, 0.01), self.square.rand_cell(), randint(10, 30) / 500.0, self.type))

			for g in self.growers:
				g.draw_grower()
				if g.grow_grower() == False:
					self.growers.remove(g)

			if one_in(100):
				self.type = not self.type

			if one_in(100):
				self.color = random_color_range(self.color, 0.02)

			if one_in(40):
				self.density = up_or_down(self.density, 2, 4, 40)

			yield self.speed