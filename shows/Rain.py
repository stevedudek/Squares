from HelperFunctions import*
from color import rgb_to_hsv, random_color_range

class Rain(object):
	def __init__(self, squaremodel):
		self.name = "Rain"
		self.square = squaremodel
		self.raindrops = Bricks(squaremodel)
		self.speed = 0.04
		self.blue = rgb_to_hsv((0,0,255))
		self.density = randint(2,10)
		self.wind = 0
		          
	def next_frame(self):

		self.square.clear()

		while (True):

			for i in range(self.density):
				self.raindrops.add_brick(random_color_range(self.blue, 0.05), life=self.square.height + 2,
										 pos=(randint(-10, 10 + self.square.width), self.square.height), length=0, pitch=1, length_x=0,
										 length_y=-1, dx=self.wind / 10.0, dy=-1, accel_x=0, accel_y=0, use_faders=False)

			self.raindrops.move_bricks()

			if one_in(20):
				self.density = up_or_down(self.density, 1, 2, 10)

			if one_in(20):
				self.wind = up_or_down(self.wind, 1, -10, 10)
				self.raindrops.set_all_dx(self.wind / 10.0)

			if one_in(500):
				self.square.set_all_cells(rgb_to_hsv((255, 255, 100)))

			yield self.speed  	# random time set in init function