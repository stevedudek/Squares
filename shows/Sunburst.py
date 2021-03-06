from HelperFunctions import*
from math import sin, cos, pi
from color import random_color, random_color_range

class Sunburst(object):
	def __init__(self, squaremodel):
		self.name = "Sunburst"
		self.square = squaremodel
		self.bricks = Bricks(squaremodel, bounce=False)
		self.speed = 0.2
		self.color = rand_color()
		self.density = randint(1, 4)
		self.syms = [2, 3, 4, 5, 6, 8, 10, 12]
		self.sym = randint(0, len(self.syms) - 1)

	def next_frame(self):

		self.square.clear()

		while (True):

			if one_in(self.density):
				angle = randint(0, 359)
				life = randint(50, 500)
				change = randint(1,5) / 10.0
				symmetry = self.syms[self.sym]

				for i in range(symmetry):
					rad = 2 * 3.14159 * (angle + (i * 360 / symmetry)) / 360
					self.bricks.add_brick(self.color, life=life, pos=(self.square.width // 2, self.square.height // 2),
										  length=randint(1,4), pitch=1, length_x=sin(rad), length_y=cos(rad),
										  dx=sin(rad), dy=cos(rad), accel_x=0, accel_y=0, use_faders=False, change=change)

				self.color = random_color_range(self.color, 0.1)

			if one_in(40):
				self.density = up_or_down(self.density, 1, 1, 4)

			if one_in(100):
				self.sym = up_or_down(self.sym, 1, 0, len(self.syms) - 1)

			self.bricks.move_bricks()

			yield self.speed