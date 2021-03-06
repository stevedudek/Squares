from HelperFunctions import*
from square import*
from color import random_color, random_color_range, change_color
        		
class Branch(object):
	def __init__(self, squaremodel, square_num, color, pos, dir, life):
		self.square = squaremodel
		self.square_num = square_num
		self.color = color
		self.pos = pos
		self.dir = dir
		self.life = life	# How long the branch has been around

	def draw_branch(self):
		self.square.set_cell(self.pos, gradient_wheel(self.color, 0.4 * (1.0 - (self.life / 20.0))))
	
	def move_branch(self):			
		newspot = square_in_direction(self.pos, self.dir, 1)	# Where is the branch going?
		if self.square.is_on_square(self. square_num, newspot) and self.life < 20:	# Is new spot off the board?
			self.pos = newspot	# On board. Update spot
			self.life += 1
			return True
		return False	# Off board. Pick a new direction
				
				
class Branches(object):
	def __init__(self, squaremodel):
		self.name = "Branches"        
		self.square = squaremodel
		self.livebranches = []	# List that holds Branch objects
		self.speed = 0.05
		self.maincolor =  rand_color()	# Main color of the show
		self.maindir = rand_dir() # Random initial main direction
		          
	def next_frame(self):
    	
		while (True):
			
			# Check how many branches are in play
			# If no branches, add one. If branches < 10, add more branches randomly
			while len(self.livebranches) < 10 or one_in(10):
				sq = self.square.rand_square()	# Pick a random Square
				newbranch = Branch(self.square, sq, random_color_range(self.maincolor, 0.02), choice(self.square.edges(sq)), self.maindir, 0)
				self.livebranches.append(newbranch)
				
			for b in self.livebranches:
				b.draw_branch()
				
				# Chance for branching
				if one_in(5):	# Create a fork
					new_dir = turn_left_or_right(b.dir)
					new_branch = Branch(self.square, b.square_num, change_color(b.color, 0.03), b.pos, new_dir, b.life)
					self.livebranches.append(new_branch)
					
				if b.move_branch() == False:	# branch has moved off the board
					self.livebranches.remove(b)	# kill the branch
								
			# Infrequently change the dominate direction
			if one_in(10):
				self.maindir = turn_left_or_right(self.maindir)
			
			yield self.speed  	# random time set in init function