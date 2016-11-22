from HelperFunctions import*
from color import randColor, randColorRange, changeColor

class BounceCannons2(object):
	def __init__(self, squaremodel):
		self.name = "BounceCannons2"
		self.square = squaremodel
		self.bricks = Bricks(squaremodel)
		self.speed = 0.05
		self.color1 = randColor()
		self.color2 = changeColor(self.color1, 0.5)
		self.density = randint(1, 5)
		self.length = randint(1,10)
		          
	def next_frame(self):

		self.square.clear()

		while (True):

			if oneIn(self.density):
				L_cannon = True if oneIn(2) else False
				color = self.color1 if L_cannon else self.color2
				x_range = randint(5, 44) / 100.0
				dy = (0.45 - abs(x_range)) * plusORminus()
				self.bricks.add_brick(randColorRange(color, 0.1), life=200,
									  pos=(0 if L_cannon else (self.square.width-1), self.square.height / 2),
									  length=self.length, pitch=0.5, length_x=-0.5 if L_cannon else 0.5,
									  length_y=0.5 if L_cannon else -0.5,
									  dx=x_range if L_cannon else -x_range, dy=dy,
									  accel_x=0, accel_y=0, use_faders=False)

			self.bricks.move_bricks()

			for b in self.bricks.get_bricks():
				b.set_length_x(b.get_dx())
				b.set_length_y(b.get_dy())

			# Change the colors
			if oneIn(10):
				self.color1 = randColorRange(self.color1, 0.05)

			if oneIn(10):
				self.color2 = randColorRange(self.color2, 0.03)

			if oneIn(100):
				self.density = upORdown(self.density, 1, 1, 5)

			yield self.speed  	# random time set in init function