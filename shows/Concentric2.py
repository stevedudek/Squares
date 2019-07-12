from HelperFunctions import*
from color import random_color, random_color_range, change_color
from random import choice

class Grower(object):
	def __init__(self, squaremodel, max_size, color, pos, gradient):
		self.square = squaremodel
		self.size = 0
		self.max_size = max_size
		self.color = random_color_range(color, 0.1)
		self.pos = pos
		self.gradient = gradient

	def draw_grower(self):
		self.square.draw_circle(self.pos, self.size, gradient_wheel(self.color, 0.8 * float(self.max_size - self.size) / self.max_size))

	def grow_grower(self):
		self.size += 1
		return self.size <= self.max_size


class Concentric2(object):
	def __init__(self, squaremodel):
		self.name = "Concentric2"
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

			if len(self.growers) < 10 or one_in(self.density):
				pos = (randint(-self.square.height, self.square.width + self.square.height), self.square.height / 2)
				self.growers.append(Grower(self.square, randint(3, 8), self.color, pos, randint(10, 30) / 500.0))

			for g in self.growers:
				g.draw_grower()
				if g.grow_grower() == False:
					self.growers.remove(g)

			if one_in(100):
				self.color = random_color_range(self.color, 0.02)

			if one_in(40):
				self.density = up_or_down(self.density, 2, 4, 40)

			yield self.speed