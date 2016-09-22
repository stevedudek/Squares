"""
Model to communicate with a Square simulator over a TCP socket

"""

SQUARE_SIZE = 12    # Number of LEDs high/wide for each square

"""
Parameters for each Square: (X, Y)
"""
BIG_COORD = [ (0,0), (1,0), (0,1), (1,1) ]

from random import choice, randint

def load_squares(model):
    return Square(model)

class Square(object):

    """
    Square coordinates are stored in a hash table.
    Keys are (r,p,d) coordinate triples
    Values are (strip, pixel) triples
    
    Frames implemented to shorten messages:
    Send only the pixels that change color
    Frames are hash tables where keys are (r,p,d) coordinates
    and values are (r,g,b) colors
    """
    def __init__(self, model):
        self.model = model
        self.cellmap = self.add_squares()
        self.squares = len(BIG_COORD)
        self.width = self.calc_width()
        self.height = self.calc_height()
        self.size = (self.width, self.height)
        self.curr_frame = {}
        self.next_frame = {}
        self.init_frames()

    def __repr__(self):
        return "Squares: {} x {}".format(self.width, self.height)

    def all_cells(self):
        "Return the list of valid coords"
        return list(self.cellmap.keys())

    def cell_exists(self, coord):
        return coord in self.cellmap

    def inbounds(self, coord):
        (x,y) = coord
        return (0 <= x < self.width and 0 <= y < self.height)

    def set_cell(self, coord, color, wrap=False):
        c = self.wrap_coord(coord, wrap)
        if self.cell_exists(c):
            self.next_frame[c] = color

    def set_cells(self, coords, color, wrap=False):
        for coord in coords:
            self.set_cell(coord, color, wrap)

    def set_all_cells(self, color):
        for c in self.all_cells():
            self.next_frame[c] = color

    def black_cells(self):
        self.set_all_cells((0,0,0))

    def clear(self):
        self.force_frame()
        self.set_all_cells((0,0,0))
        self.go()

    def go(self):
        self.send_frame()
        self.model.go()
        self.update_frame()

    def send_delay(self, delay):
        self.model.send_delay(delay)

    def update_frame(self):
        for coord in self.next_frame:
            self.curr_frame[coord] = self.next_frame[coord]

    def send_frame(self):
        for coord, color in self.next_frame.items():
            if self.curr_frame[coord] != color: # Has the color changed? Hashing to color values
                self.model.set_cell(coord, color)

    def force_frame(self):
        for coord in self.curr_frame:
            self.curr_frame[coord] = (-1,-1,-1)  # Force update

    def init_frames(self):
        for coord in self.cellmap:
            self.curr_frame[coord] = (0,0,0)
            self.next_frame[coord] = (0,0,0)

    def add_squares(self):
        cellmap = {}

        for (BIG_X, BIG_Y) in BIG_COORD:
            for x in range(SQUARE_SIZE):
                for y in range(SQUARE_SIZE):
                    cellmap[(x + (BIG_X * SQUARE_SIZE), y + (BIG_Y * SQUARE_SIZE))] = (0,0,0)
        return cellmap

    def calc_height(self):
        return SQUARE_SIZE * (max([y for (x,y) in BIG_COORD]) - min([y for (x,y) in BIG_COORD]) + 1)

    def calc_width(self):
        return SQUARE_SIZE * (max([x for (x,y) in BIG_COORD]) - min([x for (x,y) in BIG_COORD]) + 1)

    def wrap_coord(self, coord, wrap):
        (x,y) = coord
        return (x % self.width, y % self.height) if wrap else coord

    def rand_cell(self):
        return choice(self.cellmap.keys())

    def rand_square(self):
        return randint(0, len(BIG_COORD)-1)

    def num_squares(self):
        return len(BIG_COORD)

    def edges(self, square_num):
        "Return a list of edges for the particular sq number"
        (x_offset, y_offset) = get_LL_corner(square_num)

        bottom = [(x_offset + x, y_offset) for x in range(SQUARE_SIZE)]
        top = [(x_offset + x, y_offset + SQUARE_SIZE - 1) for x in range(SQUARE_SIZE)]
        left = [(x_offset, y_offset + y) for y in range(1, SQUARE_SIZE - 1)]
        right = [(x_offset + SQUARE_SIZE - 1, y_offset + y) for y in range(1, SQUARE_SIZE - 1)]

        return bottom + top + left + right

    def is_on_square(self, square_num, coord):
        (x, y) = coord
        (x_corner, y_corner) = get_LL_corner(square_num)
        return x_corner <= x < x_corner + SQUARE_SIZE and y_corner <= y < y_corner + SQUARE_SIZE


##
## square cell primitives
##
def neighbors(coord):
    "Returns a list of the four neighboring tuples at a given coordinate"
    (x,y) = coord

    coords = [ (0, 1), (1, 0), (0, -1), (-1, 0) ]

    return [(x+dx, y+dy) for (dx,dy) in coords]

def touch_neighbors(coord):
    "Returns a list of the eight neighboring tuples at a given coordinate"
    (x,y) = coord

    coords = [ (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1) ]

    return [(x+dx, y+dy) for (dx,dy) in coords]

def square_in_line(coord, direction, distance=0):
    """
    Returns the coord and all pixels in the direction
    along the distance
    """
    return [square_in_direction(coord, direction, x) for x in range(distance)]

def square_in_direction(coord, direction, distance=1):
    """
    Returns the coordinates of the cell in a direction from a given cell.
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
    (big_x, big_y) = BIG_COORD[square_num]
    return (big_x * SQUARE_SIZE, big_y * SQUARE_SIZE)

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
