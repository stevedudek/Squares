from random import random, randint, choice

from HelperFunctions import*

class Sparkle(object):
	def __init__(self, squaremodel, color, pos, intense=0, growing=True):
		self.square = squaremodel
		self.pos = pos
		self.color = color
		self.intense = intense
		self.growing = growing
	
	def draw_sparkle(self):
		self.square.set_cell(self.pos, gradient_wheel(self.color, self.intense))

	def dark_sparkle(self):
		self.square.set_cell(self.pos, (0,0,0))

	def fade_sparkle(self):
		if oneIn(3):
			if self.growing == True:
				self.intense += 0.25
				if self.intense >= 1.0:
					self.intense = 1
					self.growing = False
				return True
			else:
				self.intense -= 0.25
				return self.intense > 0

        						
class Sparkles(object):
	def __init__(self, squaremodel):
		self.name = "Sparkles"        
		self.square = squaremodel
		self.sparkles = []	# List that holds Sparkle objects
		self.speed = 0.1
		self.color = randColor()
		self.spark_num = self.square.squares * 20
		          
	def next_frame(self):

		self.square.clear()

		while (True):
			
			while len(self.sparkles) < self.spark_num:
				new_sparkle = Sparkle(self.square, randColorRange(self.color, 30), self.square.rand_cell())
				self.sparkles.append(new_sparkle)

			# Draw the sparkles
			for s in self.sparkles:
				s.draw_sparkle()
				if s.fade_sparkle() == False:
					s.dark_sparkle()
					self.sparkles.remove(s)
			
			# Change the colors
			if oneIn(100):
				self.color = randColorRange(self.color, 30)
			
			yield self.speed  	# random time set in init function