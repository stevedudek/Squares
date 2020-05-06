"""
Model to communicate with a Square simulator over a TCP socket

"""
from color import gradient_wheel
from random import choice, randint
from math import sin, cos, pi
from pixel import Pixel

BIG_COORD = [ (0,0), (1,0), (2,0), (3,0) ]
NUM_DISPLAYS = len(BIG_COORD)
SQUARE_SIZE = 12    # Number of LEDs high/wide for each square

"""
March 2020 Changes
1. DMX King

July 2019 Changes
1. Implement Pixel class in place of hash table

Nov 2018 Changes
1. No more fades to black, so removed "fract" variable below
2. Added send_intensity()

Parameters for each Square: (X, Y)
"""


class Square(object):
    """
    Square object (= square model) represents all LEDs (so all 4 giant squares)
    Each Square is composed of Pixel objects

    Square coordinates are stored in a hash table.
    Keys are (s,x,y) coordinate triples
    Pixel objects are the values
    """
    def __init__(self):
        self.size = (self.width, self.height)
        self.cellmap = self.add_pixels()  # { coord: pixel object }

    def __repr__(self):
        return "Squares: {} x {}".format(self.width, self.height)

    @property
    def squares(self):
        return NUM_DISPLAYS

    def all_cells(self):
        """Get all valid coordinates"""
        return self.cellmap.keys()

    def all_pixels(self):
        """Get all pixel objects"""
        return self.cellmap.values()

    def all_onscreen_pixels(self):
        return [pixel for pixel in self.all_pixels() if pixel.cell_exists()]

    def cell_exists(self, coord):
        """True if the coordinate is valid"""
        return coord in self.cellmap

    def get_pixel(self, coord):
        """Get the pixel object associated with the (x,y) coordinate"""
        return self.cellmap.get(coord)

    def inbounds(self, coord):
        """Is the coordinate inbounds?"""
        (x, y) = coord
        return 0 <= x < self.width and 0 <= y < self.height

    def set_cell(self, coord, color, wrap=False):
        """Set the pixel at coord (x,y) to color hsv"""
        if wrap:
            (x, y) = coord
            coord = (x % self.width, y % self.height)

        if self.cell_exists(coord):
            self.get_pixel(coord).set_color(color)

    def set_cells(self, coords, color, wrap=False):
        """Set the pixels at coords to color hsv"""
        for coord in coords:
            self.set_cell(coord, color, wrap)

    def set_all_cells(self, color):
        """Set all cells to color hsv"""
        for pixel in self.all_onscreen_pixels():
            pixel.set_color(color)

    def black_cell(self, coord):
        """Blacken the pixel at coord (x,y)"""
        if self.cell_exists(coord):
            self.get_pixel(coord).set_black()

    def black_all_cells(self):
        """Blacken all pixels"""
        for pixel in self.all_onscreen_pixels():
            pixel.set_black()

    def clear(self):
        """Force all cells to black"""
        for pixel in self.all_onscreen_pixels():
            pixel.force_black()

    def push_next_to_current_frame(self):
        """Push the next frame back into the current frame"""
        for pixel in self.all_onscreen_pixels():
            pixel.push_next_to_current_frame()

    def interpolate_frame(self, fraction):
        """Dump the current frame into the interp frame"""
        for pixel in self.all_onscreen_pixels():
            pixel.interpolate_frame(fraction)

    #
    # Setting up the Square
    #
    @staticmethod
    def add_pixels():
        """cellmap is a dictionary of { coord: pixel object }
           could do this as a complicated one-liner, but not worth the obscurity"""
        cellmap = {}

        for BIG_X, BIG_Y in BIG_COORD:
            for x in range(SQUARE_SIZE):
                for y in range(SQUARE_SIZE):
                    x_coord = x + (BIG_X * SQUARE_SIZE)
                    y_coord = y + (BIG_Y * SQUARE_SIZE)
                    cellmap[(x_coord, y_coord)] = Pixel(x_coord, y_coord)
        return cellmap

    @property
    def height(self):
        return SQUARE_SIZE * self.big_height

    @property
    def big_height(self):
        return max([y for (x,y) in BIG_COORD]) - min([y for (x,y) in BIG_COORD]) + 1

    @property
    def width(self):
        return SQUARE_SIZE * self.big_width

    @property
    def big_width(self):
        return max([x for (x, y) in BIG_COORD]) - min([x for (x, y) in BIG_COORD]) + 1

    def rand_cell(self):
        """Pick a random coordinate"""
        return choice(list(self.cellmap.keys()))

    @staticmethod
    def rand_square():
        """Pick a random big square number"""
        return randint(0, len(BIG_COORD)-1)

    @property
    def num_squares(self):
        return len(BIG_COORD)

    @staticmethod
    def edges(square_num):
        """Return a list of edges for the particular sq number"""
        (x_offset, y_offset) = get_LL_corner(square_num)

        bottom = [(x_offset + x, y_offset) for x in range(SQUARE_SIZE)]
        top = [(x_offset + x, y_offset + SQUARE_SIZE - 1) for x in range(SQUARE_SIZE)]
        left = [(x_offset, y_offset + y) for y in range(1, SQUARE_SIZE - 1)]
        right = [(x_offset + SQUARE_SIZE - 1, y_offset + y) for y in range(1, SQUARE_SIZE - 1)]

        return bottom + top + left + right

    def frame_cells(self):
        """Return a list of outer frame cells"""
        return [(x, 0) for x in range(self.width)] + \
               [(x, self.height-1) for x in range(self.width)] + \
               [(0, y) for y in range(self.height)] + \
               [(self.width - 1, y) for y in range(self.height)]

    @staticmethod
    def is_on_square(square_num, coord):
        """Is the coordinate on a particular square?"""
        (x, y) = coord
        (x_corner, y_corner) = get_LL_corner(square_num)

        return x_corner <= x < (x_corner + SQUARE_SIZE) and y_corner <= y < (y_corner + SQUARE_SIZE)

    def draw_circle(self, center, r, color):
        if r < 1:
            self.set_cell(center, color)
            return

        (x_center, y_center) = center

        self.set_cells([(round(x_center + (r * sin(2 * pi * angle / (r * 8)))),
                         round(y_center + (r * cos(2 * pi * angle / (r * 8))))) for angle in range(r * 8)], color)

    def draw_sphere(self, center, radius, color, fade=False):
        for r in reversed(range(radius)):
            color_adj = gradient_wheel(color, float(radius - r + 1) / radius) if fade else color
            self.draw_circle(center, r, color_adj)


"""
square cell primitives
"""


def neighbors(coord):
    """Returns a list of the four neighboring tuples at a given coordinate"""
    (x,y) = coord

    _coords = [ (0, 1), (1, 0), (0, -1), (-1, 0) ]

    return [(x+dx, y+dy) for (dx,dy) in _coords]


def touch_neighbors(coord):
    """Returns a list of the eight neighboring tuples at a given coordinate"""
    (x,y) = coord

    _coords = [ (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1) ]

    return [(x+dx, y+dy) for (dx,dy) in _coords]


def square_in_line(coord, direction, distance=0):
    """
    Returns the coord and all pixels in the direction along the distance
    """
    return [square_in_direction(coord, direction, x) for x in range(distance)]


def square_in_direction(coord, direction, distance=1):
    """
    Returns the coordinates of the cell in a direction from a given cell
    Direction is indicated by an integer
    """
    for i in range(distance):
        coord = square_nextdoor(coord, direction)
    return coord


def square_nextdoor(coord, direction):
    """
    Returns the coordinates of the square cell in the given direction
    Coordinates determined from a lookup table
    """
    _lookup = [ (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1) ]

    (x,y) = coord
    (dx,dy) = _lookup[(direction % len(_lookup))]
    
    return (x+dx, y+dy)


def get_rand_neighbor(coord):
    """
    Returns a random neighbors
    Neighbor may not be in bounds
    """
    return choice(neighbors(coord))


def get_LL_corner(square_num):
    """
    Returns the lower-left coordinate of the square_num
    """
    big_x, big_y = BIG_COORD[square_num]
    return big_x * SQUARE_SIZE, big_y * SQUARE_SIZE


def get_center(square_num):
    """
    Returns the center coordinate of the square_num
    """
    half_square = SQUARE_SIZE // 2
    (x_ll, y_ll) = get_LL_corner(square_num)
    return (x_ll + half_square, y_ll + half_square)


def square_shape(coord, size):
    """
    Get the cells of a square whose lower-left corner is at coord
    """
    (x_ll, y_ll) = coord
    return [(x + x_ll, y + y_ll) for x in range(size) for y in range(size)]


def mirror_coords(coord, sym=4):
    """
    Return the 1, 2, or 4 mirror coordinates
    """
    if sym == 1:
        return [coord]

    (x, y) = coord
    x_offset, y_offset = x % SQUARE_SIZE, y % SQUARE_SIZE
    x_ll, y_ll = x - x_offset, y - y_offset

    if sym == 2:
        return [(x_offset + x_ll, y_offset + y_ll), (SQUARE_SIZE - y_offset + x_ll, SQUARE_SIZE - x_offset + y_ll)]
    else:
        return [(x_offset + x_ll, y_offset + y_ll), (y_offset + x_ll, SQUARE_SIZE - x_offset + y_ll),
                (SQUARE_SIZE - y_offset + x_ll, SQUARE_SIZE - x_offset + y_ll), (SQUARE_SIZE - y_offset + x_ll, x_offset + y_ll)]
