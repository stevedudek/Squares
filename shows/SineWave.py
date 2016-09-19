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

class SineWave(object):
	def __init__(self, squaremodel):
		self.name = "SineWave"
		self.square = squaremodel
		self.sparkles = []  # List that holds Sparkle objects
		self.speed = 0.1
		self.color = randColor()
		self.counter = 0
		self.wag_speed = randint(25, 500)
		self.decay = randint(1,10) / 20.0

		          
	def next_frame(self):

		self.square.clear()

		while (True):
			self.square.black_cells()

			for x in range(self.square.width):
				waggle = sin(2 * pi * self.get_fract(self.counter, self.wag_speed))	# Up and Down motion results = -1 to +1
				angle = 2 * pi * self.get_fract(x + self.counter, self.square.width)
				y = int((sin(angle) * waggle + 1) * self.square.height / 2)	# (-1 to 1) * (-1 to 1) + 1 = 0 to 2

				new_sparkle = Sparkle(self.square, randColorRange(self.color, 50), (x,y), 1.0, False, self.decay)
				self.sparkles.append(new_sparkle)

			# Draw the sparkles
			for s in self.sparkles:
				s.draw_sparkle()
				if s.fade_sparkle() == False:
					s.dark_sparkle()
					self.sparkles.remove(s)

			# Change the colors
			if oneIn(10):
				self.color = randColorRange(self.color, 10)

			self.counter -= 1
			yield self.speed  	# random time set in init function

	def get_fract(self, var, max_var):
		"""Return 0 - 1.0 the fraction a var is to max_var"""
		return (var % max_var) / float(max_var)