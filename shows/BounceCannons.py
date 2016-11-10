from HelperFunctions import*
from math import sin, cos, pi

class BounceCannons(object):
	def __init__(self, squaremodel):
		self.name = "BounceCannons"
		self.square = squaremodel
		self.bricks = Bricks(squaremodel, bounce=True)
		self.speed = 0.01
		self.color1 = randColor()
		self.color2 = self.color1 + (maxColor // 2)
		self.density = randint(20, 50)
		          
	def next_frame(self):

		self.square.clear()

		while (True):

			if oneIn(self.density):
				L_cannon = True if oneIn(2) else False
				color = self.color1 if L_cannon else self.color2
				x_range = randint(10, 20) / 50.0
				dy = 0.45 - abs(x_range)
				self.bricks.add_brick(wheel(randColorRange(color, 100)), life=1000,
									  pos=(0 if L_cannon else (self.square.width-1), 0),
									  length=0, pitch=1, length_x=0, length_y=0,
									  dx=x_range if L_cannon else -x_range, dy=dy,
									  accel_x=0, accel_y=0, use_faders=True, change=0.4)

			self.bricks.move_bricks()

			# Change the colors
			if oneIn(10):
				self.color1 = randColorRange(self.color1, 20)

			if oneIn(10):
				self.color2 = randColorRange(self.color2, 40)

			if oneIn(100):
				self.density = upORdown(self.density, 2, 20, 50)

			yield self.speed  	# random time set in init function