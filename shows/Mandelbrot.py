from HelperFunctions import*
from color import change_color


class Mandelbrot(object):
    def __init__(self, squaremodel):
        self.name = "Mandelbrot"
        self.square = squaremodel
        self.color = rand_color()
        self.maxiter = 80
        self.speed = 0.1
        # self.center = ( -0.745428, 0.113009)
        # self.center = (-1.25066,  0.02012)
        self.center = (-0.235125, 0.827215)
        self.counter = 0

    def next_frame(self):

        while True:
            fractal = self.mandelbrot_set(self.calc_edges(self.counter, self.center), self.square.width, self.square.height, self.maxiter)

            for x in range(self.square.width):
                for y in range(self.square.height):
                    value = fractal[x,y]
                    color = change_color(self.color, value * 20) if value < self.maxiter else (0, 0, 0)
                    self.square.set_cell((x,y), color)

            self.counter += 1

            yield self.speed  	# random time set in init function

    def mandelbrot(self, z, maxiter):
        c = z
        for n in range(maxiter):
            if abs(z) > 2:
                return n
            z = z * z + c
        return maxiter

    def mandelbrot_set(self, edges, width, height, maxiter):
        xmin, xmax, ymin, ymax = edges
        r1 = [xmin + (i * (xmax - xmin) / float(width - 1)) for i in range(width)]
        r2 = [ymin + (i * (ymax - ymin) / float(height - 1)) for i in range(height)]
        z = {}

        for i in range(width):
            for j in range(height):
                z[i,j] = self.mandelbrot(r1[i] + 1j * r2[j], maxiter)
        return z

    def calc_edges(self, t, center):
        converge = pow(1.0 - (float(t) / (t + 1)), 2)
        (x,y) = center
        return (x - (converge * 1.25), x + (converge * 1.25), y - (converge * 1.25), y + (converge * 1.25))