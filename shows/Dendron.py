from HelperFunctions import*
from square import*
from color import random_color, random_color_range
        		
class Dendron(object):
	def __init__(self, squaremodel, square_num, color, pos, dir, life, longevity):
		self.square = squaremodel
		self.square_num = square_num
		self.color = color
		self.pos = pos
		self.dir = dir
		self.life = life	# How long the branch has been around
		self.squaremodel = squaremodel
		self.longevity = longevity

	def draw_dendron(self, inversion):
		if inversion:
			ratio = self.life / float(self.longevity)	# dark center
		else:
			ratio = 1 - self.life / float(self.longevity)	# light center
			
		# color the 4 mirrored coordinates
		self.square.set_cells(mirror_coords(self.pos), gradient_wheel(self.color, 0.5 * ratio))
							
		# Random chance that path changes
		if one_in(4):
			self.dir = turn_left_or_right(self.dir)
	
	def move_dendron(self):			
		newspot = square_in_direction(self.pos, self.dir, 1)	# Where is the dendron going?
		if self.square.is_on_square(self.square_num, newspot) and self.life < 50:	# Is new spot off the board?
			self.pos = newspot	# On board. Update spot
			self.life += 1
			return True
		return False	# Off board. Kill.
	

				
class Dendrons(object):
	def __init__(self, squaremodel):
		self.name = "Dendrons"
		self.square = squaremodel
		self.livedendrons = []	# List that holds Dendron objects
		self.speed = 0.02
		self.maincolor =  rand_color()	# Main color of the show
		self.inversion = randint(0,1)	# Toggle for effects
		self.longevity = randint(20, 100)
		          
	def next_frame(self):
    	
		while (True):
			
			# Randomly add a center dendron
			
			if len(self.livedendrons) < 20 and one_in(5):
				sq = self.square.rand_square()
				newdendron = Dendron(self.square, sq, random_color_range(self.maincolor, 0.03), choice(self.square.edges(sq)), MAX_DIR, 0, self.longevity)
				self.livedendrons.append(newdendron)
				
			for d in self.livedendrons:
				d.draw_dendron(self.inversion)
				
				# Chance for branching
				if one_in(20):	# Create a fork
					newdir = turn_left_or_right(d.dir)
					newdendron = Dendron(self.square, sq, d.color, d.pos, newdir, d.life, d.longevity)
					self.livedendrons.append(newdendron)
					
				if d.move_dendron() == False:	# dendron has moved off the board
					self.livedendrons.remove(d)	# kill the branch

			if one_in(20):
				self.maincolor = random_color_range(self.maincolor, 0.05)

			if one_in(100):
				self.inversion = randint(0, 1)  # Toggle for effects

			if one_in(10):
				self.longevity = up_or_down(self.longevity, 1, 20, 100)

			yield self.speed