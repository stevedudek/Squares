from HelperFunctions import*
from math import sin, cos, pi

class Sparkle(object):
	def __init__(self, squaremodel, color, pos, intense=0, growing=True, decrease=0.25):
		self.square = squaremodel
		self.pos = pos
		self.color = color
		self.intense = intense
		self.growing = growing
		self.decrease = decrease

	def draw_sparkle(self):
		self.square.set_cell(self.pos, gradient_wheel(self.color, self.intense))

	def dark_sparkle(self):
		self.square.set_cell(self.pos, (0, 0, 0))

	def fade_sparkle(self):
		if oneIn(3):
			if self.growing == True:
				self.intense += self.decrease
				if self.intense >= 1.0:
					self.intense = 1
					self.growing = False
				return True
			else:
				self.intense -= self.decrease
				return self.intense > 0

class TwoWaves(object):
	def __init__(self, squaremodel):
		self.name = "TwoWaves"
		self.square = squaremodel
		self.sparkles = []  # List that holds Sparkle objects
		self.speed = randint(1,10) / 100.0
		self.color1 = randColor()
		self.color2 = randColor()
		self.counter = 0
		          
	def next_frame(self):

		self.square.clear()

		while (True):
			self.square.black_cells()
			for x in range(self.square.width):
				waggle = sin(2*pi*(self.counter % 100) / 100)
				waggle2 = cos(2 * pi * (self.counter % 100) / 100)
				y = int((sin((x + self.counter) / (2*pi)) * waggle + 1) * self.square.height / 2)
				y2 = int((cos((x + self.counter) / (2 * pi)) * waggle2 + 1) * self.square.height / 2)
				# self.square.set_cell((x,y), wheel(self.color))
				new_sparkle = Sparkle(self.square, randColorRange(self.color1, 30), (x,y), 1.0, False, 0.5)
				self.sparkles.append(new_sparkle)
				new_sparkle = Sparkle(self.square, randColorRange(self.color1, 30), (x, y2), 1.0, False, 0.25)
				self.sparkles.append(new_sparkle)

			# Draw the sparkles
			for s in self.sparkles:
				s.draw_sparkle()
				if s.fade_sparkle() == False:
					s.dark_sparkle()
					self.sparkles.remove(s)

			# Change the colors
			if oneIn(10):
				self.color1 = randColorRange(self.color1, 10)

			if oneIn(5):
				self.color2 = randColorRange(self.color2, 20)

			self.counter -= 1
			yield self.speed  	# random time set in init function