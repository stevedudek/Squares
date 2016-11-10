from HelperFunctions import *
from square import *


def create_snake_model(squaremodel):
    return SnakeModel(squaremodel)


class SnakeModel(object):
    def __init__(self, squaremodel):
        # similar to the square Model
        # this model contains a dictionary of square coordinates
        # coordinates are the keys
        # the values are the presence of a snake:
        # 0 = no snake
        # number = snake ID

        self.square = squaremodel
        self.snakemap = {}  # Dictionary of snake square

        # Transfer regular squaremodel to the snakemmap
        # And clear (set to 0) all of the snake square

        for coord in self.square.all_cells():
            self.snakemap[coord] = 0  # No snake

    def get_snake_value(self, coord, default=None):
        "Returns the snake value for a coordinate. Return 'default' if not found"
        return self.snakemap.get(coord, default)

    def put_snake_value(self, coord, snakeID):
        "Puts the snakeID in the snake square"
        self.snakemap[coord] = snakeID

    def is_open_square(self, coord):
        "Returns True if the square is open. Also makes sure square is on the board"
        return self.square.cell_exists(coord) and self.get_snake_value(coord) == 0

    def get_valid_directions(self, coord):
        return [d for d in range(0, maxDir, 2) if self.is_open_square(square_in_direction(coord, d, 1))]

    def get_open_spots(self, coord):
        return [cell for cell in neighbors(coord) if self.is_open_square(cell)]

    def pick_open_square(self):
        opensquares = [coord for coord in self.snakemap.keys() if self.is_open_square(coord)]
        return choice(opensquares) if opensquares else False

    def remove_snake_path(self, snakeID):
        "In the snake map, changes all square with snakeID back to 0. Kills the particular snake path"
        for coord in self.snakemap.keys():
            if self.get_snake_value(coord) == snakeID:
                self.put_snake_value(coord, 0)
                ## Activate the line below for quite a different effect
                self.square.set_cell(coord, [0, 0, 0])  # Turn path back to black

    def __repr__(self):
        return str(self.lifemap)


class Snake(object):
    def __init__(self, squaremodel, maincolor, snakeID, startpos):
        self.square = squaremodel
        self.color = randColorRange(maincolor, 80)
        self.snakeID = snakeID  # Numeric ID
        self.pos = startpos  # Starting position
        self.dir = randStraightDir()
        self.pathlength = 0
        self.alive = True

    def draw_snake(self):
        self.square.set_cell(self.pos, gradient_wheel(self.color, 1.0 - (self.pathlength / 200.0)))
        self.pathlength += 1


class Snakes(object):
    def __init__(self, squaremodel):
        self.name = "Snakes"
        self.square = squaremodel
        self.snakemap = create_snake_model(squaremodel)
        self.nextSnakeID = 0
        self.livesnakes = {}  # Dictionary that holds Snake objects. Key is snakeID.
        self.speed = randint(1, 5) / 10.0
        self.maincolor = randColor()
        self.num_snakes = randint(1 * self.square.squares, 4 * self.square.squares)

    def count_snakes(self):
        return len([(id,s) for id, s in self.livesnakes.iteritems() if s.alive])

    def next_frame(self):

        self.square.clear()

        while (True):

            # Check how many snakes are in play
            # If no snakes, add one. Otherwise if snakes < 4, add more snakes randomly
            while self.count_snakes() < self.num_snakes:
                startpos = self.snakemap.pick_open_square()
                if startpos:  # Found a valid starting position
                    self.nextSnakeID += 1
                    self.snakemap.put_snake_value(startpos, self.nextSnakeID)
                    newsnake = Snake(self.square, randColorRange(self.maincolor, 400), self.nextSnakeID, startpos)
                    self.livesnakes[self.nextSnakeID] = newsnake

            for id, s in self.livesnakes.iteritems():
                if s.alive:

                    s.draw_snake()  # Draw the snake head

                    # Try to move the snake
                    nextpos = square_in_direction(s.pos, s.dir, 1)  # Get the coord of where the snake will go
                    if self.snakemap.is_open_square(nextpos):  # Is the new spot open?
                        s.pos = nextpos  # Yes, update snake position
                        self.snakemap.put_snake_value(s.pos, s.snakeID)  # Put snake on the virtual snake map
                    else:
                        dirs = self.snakemap.get_valid_directions(s.pos)  # Blocked, check possible directions
                        if len(self.snakemap.get_open_spots(s.pos)) > 0:  # Are there other places to go?
                            s.dir = choice(dirs)  # Yes, pick a random new direction
                            s.pos = square_in_direction(s.pos, s.dir, 1)
                            self.snakemap.put_snake_value(s.pos, s.snakeID)
                        else:  # No directions available
                            s.alive = False  # Kill the snake
                            self.snakemap.remove_snake_path(s.snakeID)  # Snake is killed

            yield self.speed