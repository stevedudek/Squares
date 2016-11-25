from HelperFunctions import*
from math import sin, cos, pi
from color import randColor, randColorRange, changeColor, RGB
from random import choice

class Fireworks(object):
	def __init__(self, squaremodel):
		self.name = "Fireworks"
		self.square = squaremodel
		self.tails = Bricks(squaremodel, bounce=False)
		self.heads = Bricks(squaremodel, bounce=False)
		self.speed = 0.1
		self.tail_color = RGB(255, 255, 255)	# white
		self.head_color = randColor()
		self.density = randint(2,20)
		self.counter = 0
		          
	def next_frame(self):

		self.square.clear()

		while (True):

			if self.tails.num_bricks() < 1 or oneIn(self.density):
				self.tails.add_brick(self.tail_color, life=1000, pos=(randint(0, self.square.width), 0),
									  length=0, pitch=1, length_x=0, length_y=0,
									  dx=randint(-10,10) / 50.0, dy=0.5,
									  accel_x=0, accel_y=0, use_faders=True, change=0.25)

			self.tails.move_bricks()

			for t in self.tails.get_bricks():
				(x,y) = t.get_coord()
				if y >= self.square.height / 2 and oneIn(int(self.square.height / 3)):

					sym = choice([3, 4, 6, 8, 10, 12])
					start_angle = randint(0, int(360 / sym))

					for i in range(sym):
						angle = 2 * pi * (start_angle + (360.0 * i / sym)) / 360.0
						self.heads.add_brick(randColorRange(self.head_color, 0.01), life=randint(self.square.big_width(), self.square.big_width()*2),
											 pos=(x,y), length=0, pitch=1, length_x=0, length_y=0,
											 dx=sin(angle), dy=cos(angle), accel_x=0, accel_y=randint(0,10) * 0.001,
											 use_faders=True, change=1.0 / randint(1, 4))

					self.tails.kill_brick(t)

			self.heads.move_bricks(refresh=False)

			# Change the colors
			if oneIn(10):
				self.head_color = randColorRange(self.head_color, 0.1)

			self.density = upORdown(self.density, 1, 1, 20)

			self.counter += 1

			yield self.speed