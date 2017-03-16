from HelperFunctions import*
from random import choice
from color import randColor, randColorRange

class GravityWell(object):
	def __init__(self, squaremodel):
		self.name = "GravityWell"
		self.square = squaremodel
		self.bricks = Bricks(squaremodel, bounce=False)
		self.speed = 0.1
		self.color = randColor()
		self.dust_color = randColor()
		self.center = (self.square.width / 2.0, self.square.height / 2.0)
		self.density = randint(1, 4)

	def next_frame(self):

		self.square.clear()

		while (True):

			if oneIn(self.density):
				start = choice(self.square.frame_cells())
				dist = distance(start, self.center)
				length = 1
				dx = (self.center[0] - start[0]) / dist
				dy = (self.center[1] - start[1]) / dist
				self.bricks.add_brick(randColorRange(self.dust_color, 0.02), 50, start, length, 1, dx, dy, dx, dy)

			self.draw_well()
			self.bricks.move_bricks(False)

			for b in self.bricks.get_bricks():
				if distance(b.get_coord(), self.center) <= 1:
					self.bricks.kill_brick(b)

			if oneIn(10):
				self.dust_color = randColorRange(self.dust_color, 0.02)

			if oneIn(10):
				self.color = randColorRange(self.color, 0.007)

			if oneIn(40):
				self.density = upORdown(self.density, 1, 1, 4)

			yield self.speed

	def draw_well(self):
		max_dist = distance((0,0), self.center)

		for x in range(self.square.width):
			for y in range(self.square.height):
				self.square.set_cell((x,y), gradient_wheel(self.color, 0.4 * ((distance((x,y), self.center)) / max_dist) ** 2))