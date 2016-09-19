from random import random, randint, choice
from copy import deepcopy

from HelperFunctions import*
from square import touch_neighbors
        						
class GameOfLife(object):
	def __init__(self, squaremodel):
		self.name = "GameOfLife"
		self.square = squaremodel
		self.speed = 0.1
		self.counter = 0
		self.color = randColor()
		self.cellmap = {}
		self.min_start = self.square.squares * 20
		self.max_start = self.square.squares * 100

		# Populate the cellmap with all the coordinates and blank it (set everything to False)
		for x in range(self.square.width):
			for y in range(self.square.height):
				self.cellmap[(x,y)] = False

	def next_frame(self):

		while (True):

			before_cells = [k for k,v in self.cellmap.iteritems() if v == True]

			self.check_life()

			after_cells = [k for k,v in self.cellmap.iteritems() if v == True]

			if self.counter % 400 == 0 or cmp(before_cells, after_cells) == 0:	# Have cells changed?
				self.square.clear()
				self.color = randColor()
				for i in range(randint(self.min_start, self.max_start)):
					self.light_square(choice(self.cellmap.keys()))
				yield self.speed

			self.counter += 1
			self.color += 25

			
			yield self.speed  	# random time set in init function

	def check_life(self):
		snapshot = {k:v for k,v in self.cellmap.iteritems()}

		for coord in self.cellmap.keys():
			ns = self.count_neighbors(snapshot, coord)
			life = snapshot[coord]

			if life and ns < 2:
				self.kill_square(coord)
			if life and ns > 3:
				self.kill_square(coord)
			if ~life and ns == 3:
				self.light_square(coord)

	def light_square(self, coord):
		self.square.set_cell(coord, wheel(self.color))
		self.cellmap[coord] = True

	def kill_square(self, coord):
		self.square.set_cell(coord, (0,0,0))
		self.cellmap[coord] = False

	def wrap(self, coord):
		(x,y) = coord
		return (x % self.square.width, y % self.square.height)

	def count_neighbors(self, cell_map, coord):
		return len([n for n in touch_neighbors(coord) if cell_map[self.wrap(n)] == True])
