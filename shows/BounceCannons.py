from HelperFunctions import*
from color import random_color, random_color_range, change_color

class BounceCannons(object):
	def __init__(self, squaremodel):
		self.name = "BounceCannons"
		self.square = squaremodel
		self.bricks = Bricks(squaremodel, bounce=True)
		self.speed = 0.01
		self.color1 = rand_color()
		self.color2 = change_color(self.color1, 0.5)
		self.density = randint(20, 50)
		          
	def next_frame(self):

		self.square.clear()

		while (True):

			if one_in(self.density):
				L_cannon = True if one_in(2) else False
				color = self.color1 if L_cannon else self.color2
				x_range = randint(10, 20) / 50.0
				dy = 0.45 - abs(x_range)
				self.bricks.add_brick(random_color_range(color, 0.05), life=1000,
									  pos=(0 if L_cannon else (self.square.width-1), 0),
									  length=1, pitch=1, length_x=0, length_y=0,
									  dx=x_range if L_cannon else -x_range, dy=dy,
									  accel_x=0, accel_y=0, use_faders=True, change=0.4)

			self.bricks.move_bricks()

			# Change the colors
			if one_in(10):
				self.color1 = random_color_range(self.color1, 0.01)

			if one_in(10):
				self.color2 = random_color_range(self.color2, 0.02)

			if one_in(100):
				self.density = up_or_down(self.density, 2, 20, 50)

			yield self.speed