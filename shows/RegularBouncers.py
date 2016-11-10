from HelperFunctions import*
from math import sin, cos, pi

class RegularBouncers(object):
	def __init__(self, squaremodel):
		self.name = "RegularBouncers"
		self.square = squaremodel
		self.bricks = Bricks(squaremodel, bounce=True)
		self.speed = 0.01
		self.color = randColor()
		self.density = randint(20, 50)
		self.counter = 0
		self.inc = 0

	def next_frame(self):

		self.square.clear()

		while (True):

			if self.counter % self.density == 0:
				color = (self.color + (self.inc * 5)) % maxColor
				dx = self.inc / 100.0
				dy = 1.0 - dx

				self.bricks.add_brick(wheel(color), life=200, pos=(0, self.square.height-1),
									  length=0, pitch=1, length_x=0, length_y=0,
									  dx=dx, dy=dy, accel_x=0, accel_y=0, use_faders=True, change=0.4)

				self.bricks.add_brick(wheel(color), life=1000, pos=(self.square.width - 1, self.square.height - 1),
									 length=0, pitch=1, length_x=0, length_y=0,
									 dx=-dx, dy=dy, accel_x=0, accel_y=0, use_faders=True, change=0.2)

				self.inc = (self.inc + 1) % 100

			self.bricks.move_bricks()

			self.counter += 1

			yield self.speed  	# random time set in init function