from HelperFunctions import*
from square import get_center
from math import sin, cos, pi

class Sunburst2(object):
	def __init__(self, squaremodel):
		self.name = "Sunburst2"
		self.square = squaremodel
		self.bricks = Bricks(squaremodel, bounce=False)
		self.speed = randint(1,5) / 10.0
		self.color = randColor()
		self.density = randint(2, 5)
		self.syms = [2, 3, 4, 5, 6, 8, 10, 12]
		self.sym = randint(0, len(self.syms) - 1)

	def next_frame(self):

		self.square.clear()

		while (True):

			if oneIn(self.density):
				angle = randint(0, 359)
				life = randint(50, 150)
				length = randint(1,10)
				change = 0.5
				symmetry = self.syms[self.sym]
				center = get_center(self.square.rand_square())
				for i in range(symmetry):
					rad = 2 * 3.14159 * (angle + (i * 360 / symmetry)) / 360
					self.bricks.add_brick(wheel(self.color), life=life, pos=center,
										  length=length, pitch=1, length_x=sin(rad), length_y=cos(rad),
										  dx=sin(rad), dy=cos(rad), accel_x=0, accel_y=0, use_faders=False, change=change)

				self.color = randColorRange(self.color, 200)

			if oneIn(40):
				self.density = upORdown(self.density, 1, 2, 5)

			if oneIn(100):
				self.sym = upORdown(self.sym, 1, 0, len(self.syms) - 1)

			self.bricks.move_bricks()

			yield self.speed  	# random time set in init function