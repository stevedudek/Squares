from HelperFunctions import*
from square import*
from color import random_color, random_color_range

class Ball(object):
    def __init__(self, squaremodel, maincolor):
        self.square = squaremodel
        self.color = random_color_range(maincolor, 0.1)
        self.pos = self.square.rand_cell()
        self.size = randint(5,8)	# Random ball size
        self.dir = rand_dir()		# Direction of ball's travel
        self.life = randint(50,200)	# how long a ball is around

    def decrease_life(self):
        if self.life > 0:
            self.life -= 1
            return True
        else:
            return False

    def draw_ball(self):
        for i in range(self.size-3):
            intensity =(i+1) / (self.size - 3.0)
            self.square.set_cells(square_shape(square_in_direction(self.pos,1, i), self.size),
                gradient_wheel(self.color, 0.6 * intensity))

    def move_ball(self):
        squares = 20
        while (squares > 0):
            newspot = square_in_direction(self.pos, self.dir, 2)	# Where is the ball going?
            if self.square.cell_exists(newspot):	# Is new spot off the board?
                self.pos = newspot	# On board. Update spot
                return
            else:
                squares -= 1
                self.dir = rand_dir()	# Off board. Pick a new direction
        self.life = 0	# Ball is stuck - kill it
        return


class Rings(object):
    def __init__(self, squaremodel):
        self.name = "Rings"        
        self.square = squaremodel
        self.balls = []	# List that holds Balls objects
        self.speed = 0.14
        self.maincolor =  rand_color()

    def next_frame(self):

        while (True):

            # Check how many balls are in play
            # If no balls, add one. Otherwise if balls < 8, add more balls randomly
            while len(self.balls) < 8:
                newball = Ball(self.square, self.maincolor)
                self.balls.append(newball)

            # Black the screen
            self.square.black_all_cells()

            # Draw all the balls
            # Increase the size of each drop - kill a drop if at full size
            for b in self.balls:
                b.draw_ball()
                b.move_ball()
                if b.decrease_life() == False:
                    self.balls.remove(b)

            yield self.speed  	# random time set in init function


