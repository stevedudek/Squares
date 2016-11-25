from HelperFunctions import*
from color import randColor, randColorRange, changeColor

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
		color = changeColor(self.color, self.gradient * self.size) if self.type else gradient_wheel(self.color, float(self.max_size - self.size + 1) / self.max_size)
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
		self.color = randColor()
		self.density = randint(4, 40)
		self.type = True

	def next_frame(self):

		self.square.clear()

		while (True):

			if len(self.growers) < 3 or oneIn(self.density):
				self.growers.append(Grower(self.square, randint(3, 8), randColorRange(self.color, 0.01), self.square.rand_cell(), randint(10, 30) / 500.0, self.type))

			for g in self.growers:
				g.draw_grower()
				if g.grow_grower() == False:
					self.growers.remove(g)

			if oneIn(100):
				self.type = not self.type

			if oneIn(100):
				self.color = randColorRange(self.color, 0.02)

			if oneIn(40):
				self.density = upORdown(self.density, 2, 4, 40)

			yield self.speed