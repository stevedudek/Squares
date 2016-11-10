from HelperFunctions import*
from math import sin, cos, pi

class Sunburst(object):
	def __init__(self, squaremodel):
		self.name = "Sunburst"
		self.square = squaremodel
		self.bricks = Bricks(squaremodel, bounce=False)
		self.speed = 0.2
		self.color = randColor()
		self.density = randint(2, 5)
		self.syms = [2, 3, 4, 5, 6, 8, 10, 12]
		self.sym = randint(0, len(self.syms) - 1)

	def next_frame(self):

		self.square.clear()

		while (True):

			if oneIn(self.density):
				angle = randint(0, 359)
				life = randint(50, 500)
				change = randint(1,5) / 10.0
				symmetry = self.syms[self.sym]

				for i in range(symmetry):
					rad = 2 * 3.14159 * (angle + (i * 360 / symmetry)) / 360
					self.bricks.add_brick(wheel(self.color), life=life, pos=(self.square.width // 2, self.square.height // 2),
										  length=0, pitch=1, length_x=0, length_y=0,
										  dx=sin(rad), dy=cos(rad), accel_x=0, accel_y=0, use_faders=True, change=change)

				self.color = randColorRange(self.color, 200)

			if oneIn(40):
				self.density = upORdown(self.density, 1, 2, 5)

			if oneIn(100):
				self.sym = upORdown(self.sym, 1, 0, len(self.syms) - 1)

			self.bricks.move_bricks()

			yield self.speed  	# random time set in init function