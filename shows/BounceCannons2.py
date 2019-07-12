from HelperFunctions import*
from color import random_color, random_color_range, change_color

class BounceCannons2(object):
	def __init__(self, squaremodel):
		self.name = "BounceCannons2"
		self.square = squaremodel
		self.bricks = Bricks(squaremodel)
		self.speed = 0.05
		self.color1 = rand_color()
		self.color2 = change_color(self.color1, 0.5)
		self.density = randint(1, 5)
		self.length = randint(1,10)
		          
	def next_frame(self):

		self.square.clear()

		while (True):

			if one_in(self.density):
				L_cannon = True if one_in(2) else False
				color = self.color1 if L_cannon else self.color2
				x_range = randint(5, 44) / 100.0
				dy = (0.45 - abs(x_range)) * plus_or_minus()
				self.bricks.add_brick(random_color_range(color, 0.1), life=200,
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
			if one_in(10):
				self.color1 = random_color_range(self.color1, 0.05)

			if one_in(10):
				self.color2 = random_color_range(self.color2, 0.03)

			if one_in(100):
				self.density = up_or_down(self.density, 1, 1, 5)

			yield self.speed  	# random time set in init function