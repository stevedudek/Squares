from HelperFunctions import*
from random import choice
from math import sin, cos, pi
from color import randColor, randColorRange, changeColor

class Rotater(object):
	def __init__(self, squaremodel, length, speed, color, pos):
		self.square = squaremodel
		self.length = length
		self.speed = speed
		self.color = color
		self.faders = Faders(squaremodel)
		self.life = randint(50,100)
		self.angle = 0
		self.sym = choice([3,4,6,8])
		self.pos = pos
		self.change = 1.0 / randint(2,8)

	def draw_rotater(self):
		for l in range(self.length):
			for i in range(self.sym):
				rad = 2 * 3.14159 * (self.angle + (i * 360 / self.sym)) / 360
				pos = (round(self.pos[0] + (sin(rad) * l)), round(self.pos[1] + (cos(rad) * l)))
				self.faders.add_fader(changeColor(self.color, l * 0.01), pos, intense=1.0, growing=False, change=self.change)

		self.faders.cycle_faders(False)

	def rotate(self):
		self.angle = (self.angle + self.speed) % 360
		self.life -= 1
		if self.life == 0:
			self.faders.fade_all()
		else:
			self.draw_rotater()
		return self.life > 0


class Rotaters(object):
	def __init__(self, squaremodel):
		self.name = "Rotaters"
		self.square = squaremodel
		self.rotaters = []
		self.speed = 0.1
		self.color = randColor()
		self.density = randint(1, 4)

	def next_frame(self):

		self.square.clear()

		while (True):

			self.square.black_cells()

			while len(self.rotaters) < 7:
				length = randint(3,10)
				new_rotater = Rotater(self.square, length, 2 * (11 - length), randColorRange(self.color, 0.2), self.square.rand_cell())
				self.rotaters.append(new_rotater)

			for r in self.rotaters:
				if r.rotate() == False:
					self.rotaters.remove(r)

			if oneIn(30):
				self.color = randColorRange(self.color, 0.1)

			if oneIn(40):
				self.density = upORdown(self.density, 1, 1, 4)

			yield self.speed