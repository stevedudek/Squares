from HelperFunctions import*
from color import randColor, randColorRange

class Cannons(object):
	def __init__(self, squaremodel):
		self.name = "Cannons"
		self.square = squaremodel
		self.bricks = Bricks(squaremodel)
		self.speed = 0.04
		self.color = randColor()
		self.density = randint(6,20)
		self.trail = randint(1,20)
		          
	def next_frame(self):

		self.square.clear()

		while (True):

			if oneIn(self.density):
				for cannon in range(3):
					x_range = randint(-100, 100) / 100.0
					dy = 1.2 - abs(x_range)
					x_pos = (cannon + 1) * self.square.width // 4
					self.bricks.add_brick(randColorRange(self.color, 0.15), life=100, pos=(x_pos, 0),
										  length=0, pitch=1, length_x=0, length_y=0, dx=x_range, dy=dy,
										  accel_x=0, accel_y=-0.04, use_faders=True, change=(self.trail / 20.0))

			self.bricks.move_bricks()

			# Change the colors
			if oneIn(10):
				self.color = randColorRange(self.color, 0.005)

			if oneIn(100):
				self.density = upORdown(self.density, 1, 6, 20)

			if oneIn(20):
				self.trail = upORdown(self.trail, 1, 1, 20)

			yield self.speed  	# random time set in init function