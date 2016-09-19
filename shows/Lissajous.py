from HelperFunctions import*
from math import sin, cos, pi

class Lissajous(object):
	def __init__(self, squaremodel):
		self.name = "Lissajous"
		self.square = squaremodel
		self.speed = 0.1
		self.counter = 0
		self.color = randColor()
		(self.a, self.b) = choice([(1, 2), (3, 2), (5, 4), (1.5, 0), (3, pi / 2)])
		self.trail_length = 100
		self.repeat = 2
		self.full_cycle = 3 * 2 * pi
		          
	def next_frame(self):

		self.square.clear()

		while (True):

			self.square.black_cells()

			for i in reversed(range(self.trail_length)):
				intense = 1.0 - (float(i) / self.trail_length)

				for j in range(self.repeat):
					time = self.counter - (0.01 * i) + (self.full_cycle * j / self.repeat)

					x_angle = sin(self.a * time - (pi / 2.0))
					y_angle = sin(self.b * time)

					x = int((x_angle + 1) * self.square.width / 2)
					y = int((y_angle + 1) * self.square.height / 2)

					self.square.set_cell((x, y), gradient_wheel(self.color + (self.counter * 20), intense))

			self.counter += 0.1
			if self.counter > self.full_cycle:
				self.counter -= self.full_cycle
				self.trail_length = randint(10,200)
				(self.a, self.b) = choice([(1,1), (1,2), (3,2), (5,4), (3, pi/2)])
				self.color = randColorRange(self.color, 10)
				self.repeat = choice([1, 2, 3, 4, 6, 8])

			self.color = randColorRange(self.color, 20)

			yield self.speed