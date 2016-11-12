from HelperFunctions import*
from square import*
        		
class Branch(object):
	def __init__(self, squaremodel, square_num, color, pos, dir, life, decay):
		self.square = squaremodel
		self.square_num = square_num
		self.color = color
		self.pos = pos
		self.dir = dir
		self.life = life
		self.decay = decay

	def draw_branch(self, inversion):
		if inversion:
			ratio = self.life / float(self.decay)  # dark center
		else:
			ratio = 1 - self.life / float(self.decay) # light center
		
		self.square.set_cell(self.pos, gradient_wheel(self.color, ratio))
							
		# Random chance that path changes
		if oneIn(3):
			self.dir = turn_left_or_right(self.dir)
	
	def move_branch(self):			
		newspot = square_in_direction(self.pos, self.dir, 1)	# Where is the branch going?
		if self.square.is_on_square(self.square_num, newspot) and self.life < 40:# Is new spot off the board?
			self.pos = newspot	# On board. Update spot
			self.life += 1
			return True
		return False	# Off board. Pick a new direction
				
				
class CenterBranches(object):
	def __init__(self, squaremodel):
		self.name = "Center Branches"        
		self.square = squaremodel
		self.livebranches = []	# List that holds Branch objects
		self.speed = 0.03
		self.maincolor =  randColor()	# Main color of the show
		self.inversion = randint(0,1)	# Toggle for effects
		self.fork = randint(5,30)
		self.decay = randint(4,20)
		          
	def next_frame(self):
    	
		while (True):
			
			# Add a center branch
			
			if len(self.livebranches) == 0 or oneIn(3):
				sq = self.square.rand_square()  # Pick a random Square
				newbranch = Branch(self.square, sq, self.maincolor, get_center(sq), randDir(), 0, self.decay)
				self.livebranches.append(newbranch)
				
			for b in self.livebranches:
				b.draw_branch(self.inversion)
				
				# Chance for branching
				if oneIn(self.fork):	# Create a fork
					newdir = turn_left_or_right(b.dir)
					newbranch = Branch(self.square, b.square_num, b.color, b.pos, newdir, b.life, b.decay)
					self.livebranches.append(newbranch)
					
				if b.move_branch() == False:	# branch has moved off the board
					self.livebranches.remove(b)	# kill the branch

			if oneIn(10):
				self.decay = upORdown(self.decay, 1, 4, 20)

			if oneIn(10):
				self.fork = upORdown(self.fork, 1, 5, 30)

			if oneIn(20):
				self.maincolor = randColorRange(self.maincolor, 50)

			if oneIn(500):
				self.inversion = randint(0, 1)  # Toggle for effects

			yield self.speed