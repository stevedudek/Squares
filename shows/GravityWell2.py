from HelperFunctions import*
from random import choice
from color import randColor, randColorRange

class GravityWell2(object):
	def __init__(self, squaremodel):
		self.name = "GravityWell2"
		self.square = squaremodel
		self.bricks = Bricks(squaremodel, bounce=False)
		self.speed = 0.1
		self.color = randColor()
		self.dust_color = randColor()
		self.center = (self.square.width / 2.0, self.square.height / 2.0)
		self.density = randint(2, 10)
		self.strength = randint(20, 50)

	def next_frame(self):

		self.square.clear()

		while (True):

			if oneIn(self.density):
				end = choice(self.square.frame_cells())
				dist = distance(self.center, end)
				length = 1
				dx = (end[0] - self.center[0]) / dist
				dy = (end[1] - self.center[1]) / dist

				self.bricks.add_brick(randColorRange(self.dust_color, 0.05), 200, self.center, length=length, pitch=1,
									  length_x=dx, length_y=dy, dx=dx, dy=dy,
									  accel_x=-dx/self.strength, accel_y=-dy/self.strength, use_faders=True, change=0.1)

			self.draw_well()
			self.bricks.move_bricks(False)

			for b in self.bricks.get_bricks():
				if distance(b.get_coord(), self.center) <= 1 and b.get_life() < 180:
					self.bricks.kill_brick(b)

			if oneIn(10):
				self.dust_color = randColorRange(self.dust_color, 0.02)

			if oneIn(10):
				self.color = randColorRange(self.color, 0.007)

			if oneIn(40):
				self.density = upORdown(self.density, 1, 2, 10)

			if oneIn(40):
				self.strength = upORdown(self.strength, 5, 20, 50)

			yield self.speed

	def draw_well(self):
		max_dist = distance((0,0), self.center)

		for x in range(self.square.width):
			for y in range(self.square.height):
				self.square.set_cell((x,y), gradient_wheel(self.color, (distance((x,y), self.center)) / max_dist))