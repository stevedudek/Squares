from HelperFunctions import*
from square import*
from color import random_color, random_color_range, change_color
        		
class Swirl(object):
	def __init__(self, squaremodel, square_num, color, pos, dir, sym, life, longevity):
		self.square = squaremodel
		self.square_num = square_num
		self.color = color
		self.pos = pos
		self.dir = dir
		self.sym = sym	# 1, 2, or 4
		self.life = life	# How long the branch has been around
		self.longevity = longevity

	def draw_swirl(self):
		self.square.set_cells(mirror_coords(self.pos, self.sym), gradient_wheel(self.color, 0.5 * (1 - self.life / float(self.longevity))))
							
		# Random chance that path changes - spirals only in one direction
		if one_in(2):
			self.dir = turn_left(self.dir)
	
	def move_swirl(self):			
		newspot = square_in_direction(self.pos, self.dir, 1)	# Where is the swirl going?
		if self.square.is_on_square(self.square_num, newspot) and self.life < 50:	# Is new spot off the board?
			self.pos = newspot	# On board. Update spot
			self.life += 1
			return True
		return False	# Off board. Kill.

class Swirls(object):
	def __init__(self, squaremodel):
		self.name = "Swirls"        
		self.square = squaremodel
		self.liveswirls = []	# List that holds Swirl objects
		self.speed = 0.1
		self.maincolor = rand_color()
		self.longevity = randint(40, 100)
		          
	def next_frame(self):
    	
		while (True):
			
			# Randomly add a center swirl
			
			if len(self.liveswirls) == 0 or one_in(30):
				for sq in range(self.square.num_squares):
					newswirl = Swirl(self.square, sq, self.maincolor, get_center(sq), rand_dir(), choice([1, 2, 4]), 0, self.longevity)
					self.liveswirls.append(newswirl)
					self.maincolor = change_color(self.maincolor, 0.02)
				
			for s in self.liveswirls:
				s.draw_swirl()
				
				# Chance for branching
				if one_in(15):	# Create a fork
					newdir = turn_left(s.dir) # always fork left
					newswirl = Swirl(self.square, sq, s.color, s.pos, newdir, s.sym, s.life, s.longevity)
					self.liveswirls.append(newswirl)
					
				if s.move_swirl() == False:	# Swirl has moved off the board
					self.liveswirls.remove(s)	# kill the branch

			if one_in(20):
				self.longevity = up_or_down(self.longevity, 2, 40, 100)

			if one_in(40):
				self.maincolor = random_color_range(self.maincolor, 0.02)

			yield self.speed