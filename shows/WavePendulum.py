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

class WavePendulum(object):
	def __init__(self, squaremodel):
		self.name = "WavePendulum"
		self.square = squaremodel
		self.sparkles = []  # List that holds Sparkle objects
		self.speed = 0.05
		self.counter = 0
		self.background = randColor()
		self.color = randColor()
		self.min_freq = 10	# fastest pendulum does this many cycles in one loop
		self.cycle_time = 5	# speed of one cycle
		self.cycles = int(self.cycle_time / self.speed)
		self.gradient = 3

		          
	def next_frame(self):
		# self.square.set_all_cells(wheel(self.background))

		while (True):

			self.square.set_all_cells(wheel(self.background))

			for x in range(self.square.width):

				w = (self.min_freq + x) / float(self.cycles)	# pendulum frequency
				y = int((cos(w * self.counter) + 1) * self.square.height / 2)

				self.square.set_cell((x, y), wheel(self.color + (y * self.gradient)))

					# new_sparkle = Sparkle(self.square, randColorRange(self.color, 50), (x,y), 1.0, False, self.decay)
					# self.sparkles.append(new_sparkle)

				# Draw the sparkles
				# for s in self.sparkles:
				# 	s.draw_sparkle()
				# 	if s.fade_sparkle() == False:
				# 		s.dark_sparkle()
				# 		self.sparkles.remove(s)


			self.counter += 1
			if self.counter % (int(2 * pi * self.cycles)) == 0:
				self.min_freq = upORdown(self.min_freq, 1, 3, 10)
				self.gradient = upORdown(self.gradient, 1, 0, 10)
				self.color = changeColor(self.color, 200)
				self.background = randColorRange(self.background, 20)


			yield self.speed  	# random time set in init function