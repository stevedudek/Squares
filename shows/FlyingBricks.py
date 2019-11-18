from HelperFunctions import*
from color import random_color_range

class FlyingBricks(object):
	def __init__(self, squaremodel):
		self.name = "FlyingBricks"
		self.square = squaremodel
		self.bricks = Bricks(squaremodel)
		self.speed = 0.05
		self.color = rand_color()
		self.white = (255, 0, 255)
		self.density = randint(2,10)
		          
	def next_frame(self):

		self.square.clear()

		while (True):

			if one_in(self.density):	# Regular bricks heading right
				brick_length = randint(3,7)
				brick_speed = 1.0 + (randint(-50, 50) / 100.0)
				self.bricks.add_brick(random_color_range(self.color, brick_length * 10 / 1000.0),
									  life=100 + (self.square.width / brick_speed),
									  pos=(-brick_length, randint(0, self.square.height)),
									  length=brick_length, pitch=1, length_x=1, length_y=0, dx=brick_speed, dy=0)

			if one_in(200):	# White bricks heading left
				brick_length = randint(5, 10)
				brick_speed = 2.0 + (randint(-50, 50) / 100.0)
				self.bricks.add_brick(self.white, life=100 + (self.square.width / brick_speed),
									  pos=(self.square.width, randint(0, self.square.height)),
									  length=brick_length, pitch=1, length_x=1, length_y=0, dx=-brick_speed, dy=0)

			self.bricks.move_bricks()

			# Change the colors
			if one_in(10):
				self.color = random_color_range(self.color, 0.005)

			if one_in(100):
				self.density = up_or_down(self.density, 1, 1, 10)

			yield self.speed  	# random time set in init function