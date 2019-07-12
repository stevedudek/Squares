from HelperFunctions import*
from math import sin, cos, pi
from color import random_color, random_color_range
from random import choice

class LissajousGrade(object):
	def __init__(self, squaremodel):
		self.name = "LissajousGrade"
		self.square = squaremodel
		self.speed = 0.1
		self.counter = 0
		self.color = rand_color()
		(self.a, self.b) = choice([(1, 2), (3, 2), (5, 4), (1.5, 0), (3, pi / 2)])
		self.full_cycle = 3 * 2 * pi
		self.repeat = choice([1, 2, 3, 4, 6, 8])
		self.grade = randint(3,10)
		          
	def next_frame(self):

		while (True):

			for x in range(self.square.width):
				for y in range(self.square.height):
					self.square.set_cell((x, y), gradient_wheel(self.color, 0.8 * max([self.calc_intense((x,y), self.get_lj_coord(j)) for j in range(self.repeat)])))

			self.counter += 0.05
			if self.counter > self.full_cycle:
				self.counter -= self.full_cycle
				self.trail_length = randint(10, 200)
				(self.a, self.b) = choice([(1,1), (1,2), (3,2), (5,4), (3, pi/2)])
				self.color = random_color_range(self.color, 10)
				self.repeat = choice([1, 2, 3, 4, 6, 8])

			self.color = random_color_range(self.color, 0.007)

			if one_in(100):
				self.grade = up_or_down(self.grade, 1, 3, 10)

			yield self.speed  	# random time set in init function

	def calc_intense(self, coord1, coord2):
		return 1.0 - (distance(coord1, coord2) / self.grade)

	def get_lj_coord(self, repeat):
		time = self.counter + (self.full_cycle * repeat / self.repeat)
		x_angle = sin(self.a * time - (pi / 2.0))
		y_angle = sin(self.b * time)

		x = int((x_angle + 1) * self.square.width / 2)
		y = int((y_angle + 1) * self.square.height / 2)

		return (x,y)