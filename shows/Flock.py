from color import RGB, HSV

from HelperFunctions import*
from square import neighbors

class Bird(object):
	def __init__(self, squaremodel, pos, reflect=True):
		self.square = squaremodel
		self.pos = pos
		self.neigh_coords = [self.check_coord(n, self.square.width, self.square.height, reflect) for n in neighbors(pos)]
		self.color = [randint(0,255), randint(0,255), randint(0,255)]
		self.next_color = self.color
		self.velocity = [0, 0, 0]
		self.next_velocity = self.velocity

	def add_vel(self):
		self.next_color = [self.next_color[i] + self.next_velocity[i] for i in range(3)]
		for i in range(3):
			if self.next_color[i] < 0:
				self.next_color[i] = 0
				self.next_velocity[i] *= -1
			elif self.next_color[i] > 255:
				self.next_color[i] = 255
				self.next_velocity[i] *= -1

	def push_frame(self):
		self.color = self.next_color
		self.velocity = self.next_velocity

	def draw(self):
		self.square.set_cell(self.pos, RGB(self.color[0], self.color[1], self.color[2]))

	def get_color(self):
		return self.color

	def get_velocity(self):
		return self.velocity

	def set_next_vel(self, next_velocity):
		self.next_velocity = next_velocity

	def get_neighbors(self):
		return self.neigh_coords

	def check_coord(self, pos, max_x, max_y, reflect):
		x,y = pos
		return (self.check_axis(x, max_x, reflect), self.check_axis(y, max_y, reflect))

	def check_axis(self, val, max_val, reflect):
		if val < 0:
			return abs(val) if reflect else max_val + val
		elif val >= max_val:
			return max_val - (val - max_val) - 1 if reflect else val - max_val
		else:
			return val


class Flock(object):
	def __init__(self, squaremodel):
		self.name = "Flock"
		self.square = squaremodel
		self.bird_dict = {(x,y): Bird(squaremodel, (x,y)) for x in range(self.square.width) for y in range(self.square.height)}
		self.minDist = 20
		self.minDistSquare = self.minDist * self.minDist
		self.sepNormMag = 4
		self.ease = 0.25
		self.speed = 0.1

	def next_frame(self):

		while (True):

			for bird in self.bird_dict.values():
				color_sum = self.add_coords([self.bird_dict[n].get_color() for n in bird.get_neighbors()])
				vel_sum = self.add_coords([self.bird_dict[n].get_velocity() for n in bird.get_neighbors()])
				sep = self.add_coords([self.check_sep(self.subtract_coords(bird.get_color(), self.bird_dict[n].get_color())) for n in bird.get_neighbors()])

				color_sum = self.mult_coord(color_sum, 0.25)	# Divide by 4
				vel_sum = self.mult_coord(vel_sum, 0.25)	# Divide by 4

				if sum(sep) > 0:
					sepMagRecip = self.sepNormMag / sqrt(sep[0]*sep[0] + sep[1]*sep[1] + sep[2]*sep[2])
					sep = self.mult_coord(sep, sepMagRecip)

				bird.set_next_vel([self.ease * (sep[i] + color_sum[i] + vel_sum[i] - bird.color[i] - bird.next_velocity[i]) for i in range(3)])

			for bird in self.bird_dict.values():
				bird.add_vel()
				bird.push_frame()
				bird.draw()

			if oneIn(200):
				self.speed = upORdown(self.speed, 0.1, 0.2, 2.0)
			
			yield self.speed

	def mult_coord(self, coord, mult):
		return [coord[i] * mult for i in range(3)]

	def add_coords(self, coords):
		return [sum([coord[i] for coord in coords]) for i in range(3)]

	def subtract_coords(self, coord1, coord2):
		return [coord1[i] - coord2[i] for i in range(3)]

	def check_sep(self, coord):
		return coord if sum([coord[i] * coord[i] for i in range(3)]) < self.minDistSquare else [0, 0, 0]



