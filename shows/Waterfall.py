from HelperFunctions import*
from color import random_color, random_color_range, change_color

class Waterfall(object):
	def __init__(self, squaremodel):
		self.name = "Waterfall"
		self.square = squaremodel
		self.bricks = Bricks(squaremodel, bounce=False)
		self.speed = 0.1
		self.color1 = rand_color()
		self.color2 = change_color(self.color1, 0.5)
		self.density = randint(2, 5)
		self.accel = randint(1, 10)
		self.fade = randint(1, 5)
		          
	def next_frame(self):

		self.square.clear()

		while (True):

			for i in range(self.density):
				L_cannon = True if one_in(2) else False
				color = self.color1 if L_cannon else self.color2
				x_range = randint(1, 20) / 20.0
				x = 0 if L_cannon else (self.square.width-1)

				self.bricks.add_brick(random_color_range(color, 0.05), life=self.square.width,
									  pos=(x, self.square.height - 3),
									  length=0, pitch=1, length_x=0, length_y=0,
									  dx=x_range if L_cannon else -x_range, dy=0,
									  accel_x=0, accel_y=-self.accel / 100.0, use_faders=True, change=1.0/self.fade)

			self.bricks.move_bricks()

			# Prevent drops from escaping off bottom of screen
			for b in self.bricks.get_bricks():
				(x, y) = b.get_coord()
				if y < 0:
					b.set_y(0)

			# Change the colors
			if one_in(10):
				self.color1 = random_color_range(self.color1, 0.01)

			if one_in(10):
				self.color2 = random_color_range(self.color2, 0.02)

			if one_in(100):
				self.density = up_or_down(self.density, 1, 2, 5)

			if one_in(100):
				self.accel = up_or_down(self.accel, 1, 1, 10)

			if one_in(100):
				self.fade = up_or_down(self.fade, 1, 1, 5)

			yield self.speed