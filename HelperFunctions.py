from random import randint, choice
from color import*
from math import sqrt

#
# Constants
#
maxDistance = 12
maxColor = 1536
maxDir = 8
maxSquare = 3
NUM_PIXELS = 144

#
# Common random functions
#

# Random chance. True if 1 in Number
def oneIn(chance):
	return True if randint(1,chance) == 1 else False

# Return either 1 or -1
def plusORminus():
	return (randint(0,1) * 2) - 1

# Increase or Decrease a counter with a range
def upORdown(value, amount, min, max):
	value += (amount * plusORminus())
	return bounds(value, min, max)

# Increase/Decrease a counter within a range
def inc(value, increase, min, max):
	value += increase
	return bounds(value, min, max)

def bounds(value, min, max):
	if value < min:
		value = min
	if value > max:
		value = max
	return value


#
# Directions
#

# Get a random direction
def randDir():
	return randint(0,maxDir)

def randStraightDir():
	return randint(0, 3) * 2

# Return the left direction
def turn_left(dir):
	return (maxDir + dir - 1) % maxDir
	
# Return the right direction
def turn_right(dir):
	return (dir + 1) % maxDir

# Randomly turn left, straight, or right
def turn_left_or_right(dir):
	return (maxDir + dir + randint(-1,1) ) % maxDir

#
# Distance Functions
#
def distance(coord1, coord2):
	(x1,y1) = coord1
	(x2,y2) = coord2
	return sqrt( (x2-x1)*(x2-x1) + (y2-y1)*(y2-y1) )

#
# Color Functions
#

# Pick a random color
def randColor():
	return randint(0, maxColor-1)
	
# Returns a random color around a given color within a particular range
# Function is good for selecting blues, for example
def randColorRange(color, window):
	return (maxColor + color + randint(-window,window)) % maxColor

# Increase color by an amount (can be negative)
def changeColor(color, amount):
	return (maxColor + color + amount) % maxColor

# Wrapper for gradient_wheel in which the intensity is 1.0 (full)
def wheel(color):
	return gradient_wheel(color, 1)

# Picks a color in which one rgb channel is off and the other two channels
# revolve around a color wheel
def gradient_wheel(color, intense, saturation=0):
	color = color % maxColor  # just in case color is out of bounds
	channel = color // 256;
	value = color % 256;

	if channel == 0:
		r = 255
		g = value
		b = saturation
	elif channel == 1:
		r = 255 - value
		g = 255
		b = saturation
	elif channel == 2:
		r = saturation
		g = 255
		b = value
	elif channel == 3:
		r = saturation
		g = 255 - value
		b = 255
	elif channel == 4:
		r = value
		g = saturation
		b = 255
	else:
		r = 255
		g = saturation
		b = 255 - value

	return (r*intense, g*intense, b*intense)
	
# Picks a color in which one rgb channel is ON and the other two channels
# revolve around a color wheel
def white_wheel(color, intense):
	color = color % maxColor  # just in case color is out of bounds
	channel = color / 256;
	value = color % 256;

	if channel == 0:
		r = 255
		g = value
		b = 255 - value
	elif channel == 1:
		r = 255 - value
		g = 255
		b = value
	elif channel == 2:
		r = value
		g = 255 - value
		b = 255
	elif channel == 3:
		r = 255
		g = value
		b = 255 - value
	elif channel == 4:
		r = 255 - value
		g = 255
		b = value
	else:
		r = value
		g = 255 - value
		b = 255
	
	return (r*intense, g*intense, b*intense)

#
# Fader class and its collection: the Faders class
#
class Faders(object):
	def __init__(self, squaremodel):
		self.square = squaremodel
		self.fader_array = []

	def add_fader(self, color, pos, intense=1.0, growing=False, change=0.25):
		new_fader = Fader(self.square, color, pos, intense, growing, change)
		self.fader_array.append(new_fader)

	def cycle_faders(self, refresh=True):
		if refresh:
			self.square.black_cells()

		# Draw, update, and kill all the faders
		for f in self.fader_array:
			if f.is_alive() == True:
				f.draw_fader()
				f.fade_fader()
			else:
				f.black_cell()
				self.fader_array.remove(f)

	def num_faders(self):
		return len(self.fader_array)

class Fader(object):
	def __init__(self, squaremodel, color, pos, intense=1.0, growing=False, change=0.25):
		self.square = squaremodel
		self.pos = pos
		self.color = color
		self.intense = intense
		self.growing = growing
		self.decrease = change

	def draw_fader(self):
		self.square.set_cell(self.pos, gradient_wheel(self.color, self.intense))

	def fade_fader(self):
		if self.growing == True:
			self.intense += self.decrease
			if self.intense > 1.0:
				self.intense = 1.0
				self.growing = False
		else:
			self.intense -= self.decrease
			if self.intense < 0:
				self.intense = 0

	def is_alive(self):
		return self.intense > 0

	def black_cell(self):
		self.square.set_cell(self.pos, (0,0,0))

#
# Brick class and its collection: the Bricks class
#
class Bricks(object):
	def __init__(self, squaremodel, bounce=False):
		self.square = squaremodel
		self.bounce = bounce
		self.brick_array = []

	def add_brick(self, color, life, pos, length, pitch, length_x, length_y, dx, dy, accel_x=0, accel_y=0, use_faders=False, change=0.25):
		new_brick = Brick(self.square, color, life, pos, length, pitch, length_x, length_y, dx, dy, accel_x, accel_y, use_faders, change)
		self.brick_array.append(new_brick)

	def move_bricks(self):
		self.square.black_cells()

		# Draw, move, update, and kill all the bricks
		for b in self.brick_array:
			b.draw_brick()
			b.move_brick(self.bounce)
			if b.age_brick() == False:
				self.brick_array.remove(b)

	def set_all_dx(self, dx):
		for b in self.brick_array:
			b.set_dx(dx)

	def set_all_dy(self, dy):
		for b in self.brick_array:
			b.set_dy(dy)

	def set_all_accel_x(self, accel_x):
		for b in self.brick_array:
			b.set_accel_x(accel_x)

	def set_all_accel_y(self, accel_y):
		for b in self.brick_array:
			b.set_accel_y(accel_y)

	def num_bricks(self):
		return len(self.brick_array)

	def get_bricks(self):
		return self.brick_array

class Brick(object):
	def __init__(self, squaremodel, color, life, pos, length, pitch, length_x, length_y, dx, dy, accel_x=0, accel_y=0,
				 use_faders=False, change=0.25):
		self.square = squaremodel
		self.color = color
		self.life = life
		self.pos = pos
		self.length = length
		self.pitch = pitch
		self.length_x = length_x
		self.length_y = length_y
		self.dx = dx
		self.dy = dy
		self.accel_x = accel_x
		self.accel_y = accel_y
		self.use_faders = use_faders
		self.faders = Faders(squaremodel) if self.use_faders else None
		self.change = change

	def draw_brick(self):
		for i in range(int(round(self.length / self.pitch)) + 1):
			pos = (round(self.pos[0] + (i * self.pitch * self.length_x)),
				   round(self.pos[1] + (i * self.pitch * self.length_y)))
			if self.use_faders:
				self.faders.add_fader(self.color, pos, intense=1.0, growing=False, change=self.change)
			else:
				self.square.set_cell(pos, self.color)

		if self.use_faders:
			self.faders.cycle_faders(False)

	def move_brick(self, bounce):
		new_x = self.pos[0] + self.dx
		new_y = self.pos[1] + self.dy

		if bounce:
			if new_x < 0 or new_x >= (self.square.width - 1):
				self.dx *= (-1 + (randint(-10,10) / 50.0))
				new_x = self.pos[0] + self.dx
			if new_y < 0 or new_y >= (self.square.height - 1):
				self.dy *= (-1 + (randint(-10,10) / 50.0))
				new_y = self.pos[1] + self.dy

		self.pos = (new_x, new_y)
		self.dx, self.dy = self.dx + self.accel_x, self.dy + self.accel_y

	def age_brick(self):
		self.life -= 1
		return self.life > 0

	def get_coord(self):
		return self.pos

	def get_dx(self):
		return self.dx

	def get_dy(self):
		return self.dy

	def set_dx(self, dx):
		self.dx = dx

	def set_dy(self, dy):
		self.dy = dy

	def set_accel_x(self, accel_x):
		self.accel_x = accel_x

	def set_accel_y(self, accel_y):
		self.accel_y = accel_y

	def set_length_x(self, length_x):
		self.length_x = length_x

	def set_length_y(self, length_y):
		self.length_y = length_y

	def set_x(self, x):
		(old_x, y) = self.pos
		self.pos = (x, y)

	def set_y(self, y):
		(x, old_y) = self.pos
		self.pos = (x, y)