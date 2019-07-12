from HelperFunctions import*
from square import neighbors

class Bird(object):
	def __init__(self, squaremodel, pos, reflect=False):
		self.square = squaremodel
		self.pos = pos
		self.neigh_coords = [self.check_coord(n, self.square.width, self.square.height, reflect) for n in neighbors(pos)]
		self.color = 0
		self.set_random()
		self.next_color = self.color
		self.velocity = 0.0
		self.next_velocity = self.velocity

	def add_vel(self):
		self.next_color += self.next_velocity
		# (q,r) = divmod(self.next_color, 255)
		# if q > 0:
		# 	print "wrapped %d -> %d" % (self.next_color, r)
		# 	self.next_velocity *= -1
		# self.next_color = r

		if self.next_color < 0:
			self.next_color = 255
			self.next_velocity *= -1
		elif self.next_color > 255:
			self.next_color = 0
			self.next_velocity *= -1

	def set_random(self):
		self.color = randint(0, 255)
		self.next_color = self.color
		self.velocity = 0.0
		self.next_velocity = self.velocity

	def push_frame(self):
		self.color = self.next_color
		self.velocity = self.next_velocity

	def draw(self):
		self.square.set_cell(self.pos, (self.color, 255, 255))	# (vary H, S=255, V=255)

	def get_color(self):
		return self.color

	def get_velocity(self):
		return self.velocity

	def set_next_vel(self, accel):
		self.next_velocity += accel

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


def color_diff(c1, c2):
	if c1 > c2:
		c2,c1 = c1,c2
	return min(abs(c2-c1), abs((c1+255)-c2))

class Flock3(object):
	def __init__(self, squaremodel):
		self.name = "Flock3"
		self.square = squaremodel
		self.bird_dict = {(x,y): Bird(squaremodel, (x,y)) for x in range(self.square.width) for y in range(self.square.height)}
		self.minDist = 10
		self.minDistSquare = self.minDist * self.minDist
		self.sepNormMag = 10
		self.ease = 0.25
		self.speed = 0.1

	def next_frame(self):

		while (True):

			for bird in self.bird_dict.values():
				color_avg = sum([self.bird_dict[n].get_color() for n in bird.get_neighbors()]) / 4.0
				vel_avg = sum([self.bird_dict[n].get_velocity() for n in bird.get_neighbors()])/ 4.0
				sep = sum([self.check_sep(bird.get_color() - self.bird_dict[n].get_color()) for n in bird.get_neighbors()])

				if sep > 0:
					sep = self.sepNormMag

				bird.set_next_vel(self.ease * (sep + color_avg + vel_avg - bird.color - bird.next_velocity))

			for bird in self.bird_dict.values():
				bird.add_vel()
				bird.push_frame()
				bird.draw()

			if one_in(25):
				self.speed = up_or_down(self.speed, 0.1, 0.2, 2.0)

			# if randint(0,100) == 1:
			# 	coord_list = self.bird_dict.keys()
			# 	shuffle(coord_list)
			# 	for coord in coord_list[:randint(1, len(coord_list))]:
			# 		self.bird_dict[coord].set_random()

			yield self.speed

	def check_sep(self, coord):
		return coord if coord * coord < self.minDistSquare else 0



