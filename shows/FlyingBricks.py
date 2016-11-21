from HelperFunctions import*
from color import randColor, randColorRange, RGB

class FlyingBricks(object):
	def __init__(self, squaremodel):
		self.name = "FlyingBricks"
		self.square = squaremodel
		self.bricks = Bricks(squaremodel)
		self.speed = 0.05
		self.color = randColor()
		self.white = RGB(255, 255, 255)
		self.density = randint(2,10)
		          
	def next_frame(self):

		self.square.clear()

		while (True):

			if oneIn(self.density):	# Regular bricks heading right
				brick_length = randint(3,7)
				brick_speed = 1.0 + (randint(-50, 50) / 100.0)
				self.bricks.add_brick(randColorRange(self.color, brick_length * 10 / 1000.0),
									  life=60 + (self.square.width / brick_speed),
									  pos=(-brick_length, randint(0, self.square.height)),
									  length=brick_length, pitch=1, length_x=1, length_y=0, dx=brick_speed, dy=0)

			if oneIn(200):	# White bricks heading left
				brick_length = randint(5, 10)
				brick_speed = 2.0 + (randint(-50, 50) / 100.0)
				self.bricks.add_brick(self.white, life=60 + (self.square.width / brick_speed),
									  pos=(self.square.width, randint(0, self.square.height)),
									  length=brick_length, pitch=1, length_x=1, length_y=0, dx=-brick_speed, dy=0)

			self.bricks.move_bricks()

			# Change the colors
			if oneIn(10):
				self.color = randColorRange(self.color, 0.005)

			if oneIn(100):
				self.density = upORdown(self.density, 1, 1, 10)

			yield self.speed  	# random time set in init function