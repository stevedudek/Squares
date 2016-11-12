from HelperFunctions import*
from math import sin, cos, pi

class Rain(object):
	def __init__(self, squaremodel):
		self.name = "Rain"
		self.square = squaremodel
		self.raindrops = Bricks(squaremodel)
		self.speed = 0.04
		self.blue = 1100
		self.density = randint(2,10)
		self.wind = 0
		          
	def next_frame(self):

		self.square.clear()

		while (True):

			for i in range(self.density):
				self.raindrops.add_brick(wheel(randColorRange(self.blue, 30)), life=self.square.height + 2,
									  pos=(randint(-10, 10 + self.square.width), self.square.height), length=0, pitch=1, length_x=0,
										 length_y=-1, dx=self.wind / 10.0, dy=-1, accel_x=0, accel_y=0, use_faders=False)

			self.raindrops.move_bricks()

			if oneIn(20):
				self.density = upORdown(self.density, 1, 2, 10)

			if oneIn(20):
				self.wind = upORdown(self.wind, 1, -10, 10)
				self.raindrops.set_all_dx(self.wind / 10.0)

			if oneIn(500):
				self.square.set_all_cells((255, 255, 100))

			yield self.speed  	# random time set in init function