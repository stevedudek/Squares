from HelperFunctions import*

class VertLines(object):
	def __init__(self, squaremodel):
		self.name = "VertLines"
		self.square = squaremodel
		self.speed = randint(1,10) / 100.0
		self.color1 = randColor()
		self.color2 = randColor()
		          
	def next_frame(self):

		# self.square.clear()

		while (True):
			for x in range(self.square.width):
				for y in range(self.square.height):
					color = self.color1 - (y * 30) if x % 2 else self.color2 + (y * 30)
					self.square.set_cell((x,y), wheel(color))
			
			# Change the colors
			if oneIn(10):
				self.color1 = changeColor(self.color1, 10)

			if oneIn(2):
				self.color2 = changeColor(self.color2, -10)
			
			yield self.speed  	# random time set in init function