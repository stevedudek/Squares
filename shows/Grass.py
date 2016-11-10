from HelperFunctions import*
from math import sin, cos, pi


class Grass(object):
	def __init__(self, squaremodel, color):
		self.square = squaremodel
		self.color = color
		self.a = randint(-10, 10) / 200.0
		self.b = 0.1
		self.c = randint(1, self.square.width)
		self.length = randint(4,10)
		self.density = 5
		self.bendy = randint(2,10) / 10.0

	def draw(self):
		for l in range(self.length):
			for d in range(self.density):
				y = l + (float(d) / self.density)
				x = (self.a * (y*y)) + (self.b * y) + self.c
				self.square.set_cell((round(x), round(y)), wheel(self.color))

	def adj_bend(self, wind):
		new_a = self.a + (wind * self.bendy)
		if (new_a < wind and wind >= 0) or (new_a > wind and wind < 0):
			self.a = new_a

class Grasses(object):
	def __init__(self, squaremodel):
		self.name = "Grasses"
		self.square = squaremodel
		self.speed = randint(1, 10) / 20.0
		self.counter = 0
		self.color = randColor()
		self.grasses = []
		self.num_grass = self.square.width
		self.counter = 0
		self.wind = 0
		self.max_wind = 0.1
		          
	def next_frame(self):

		self.square.clear()

		for i in range(self.num_grass):

			new_grass = Grass(self.square, randColorRange(self.color, 100))
			self.grasses.append(new_grass)

		while (True):

			self.square.set_all_cells([0, 0, 0])

			self.wind = self.max_wind * sin(2 * pi * self.counter / 60)

			for g in self.grasses:
				g.draw()
				g.adj_bend(self.wind)

			if oneIn(100):
				self.speed = upORdown(self.speed, 0.05, 0.05, 0.5)

			self.counter += 1

			yield self.speed
