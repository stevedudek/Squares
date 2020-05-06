"""
Reworking LED code to use a Pixel class

A LED-contraption object, like a Square, is composed of Pixel objects
A Pixel holds only 1 LED
A Pixel knows coordinates: (x, y) coordinate, (strip, LED) coordinate, DMX address
              colors: current-frame color, next-frame color, interp color, (x2 if dual channel)
Pulling the layout logic out of Processing and into this class
"""
import color as color_func
import square as square_func

# Convert (x, y) coordinate into LED position. Includes buffer LEDs.
LED_LOOKUP = [
  [144, 141, 140, 137, 136, 133, 132, 129, 128, 125, 124, 122],  # 12
  [143, 142, 139, 138, 135, 134, 131, 130, 127, 126, 123, 121],  # 11
  [98, 100, 101, 104, 105, 108, 109, 112, 113, 116, 117, 120],  # 10
  [97, 99, 102, 103, 106, 107, 110, 111, 114, 115, 118, 119],  # 9
  [96, 93, 92, 89, 88, 85, 84, 81, 80, 77, 76, 74],  # 8
  [95, 94, 91, 90, 87, 86, 83, 82, 79, 78, 75, 73],  # 7
  [50, 52, 53, 56, 57, 60, 61, 64, 65, 68, 69, 72],  # 6
  [49, 51, 54, 55, 58, 59, 62, 63, 66, 67, 70, 71],  # 5
  [48, 45, 44, 41, 40, 37, 36, 33, 32, 29, 28, 26],  # 4
  [47, 46, 43, 42, 39, 38, 35, 34, 31, 30, 27, 25],  # 3
  [2, 4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24],  # 2
  [1, 3, 6, 7, 10, 11, 14, 15, 18, 19, 22, 23]   # 1
]


class Pixel(object):
    """
    Pixel colors are hsv [0-255] triples (very simple)
    """
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.s, self.led = self.get_led()
        self.curr_frame = color_func.almost_black()
        self.next_frame = color_func.black()
        self.interp_frame = color_func.black()

    def get_coord(self):
        return self.x, self.y  # For squares, coordinate is just (x, y)

    def get_universe_index(self):
        """Return a tuple of (universe, index)"""
        return self.s + 1, self.led * 3

    def cell_exists(self):
        return self.led != -1

    def has_changed(self):
        return color_func.are_different(self.curr_frame, self.next_frame)

    def set_color(self, color):
        self.next_frame = color

    def set_next_frame(self, color):
        self.next_frame = color

    def set_curr_frame(self, color):
        self.curr_frame = color

    def interpolate_frame(self, fraction):
        interp_frame = color_func.interp_color(self.curr_frame, self.next_frame, fraction)
        self.interp_frame = interp_frame

    def set_black(self):
        self.set_color(color_func.black())

    def force_black(self):
        self.curr_frame = color_func.almost_black()
        self.set_black()

    def push_next_to_current_frame(self):
        self.curr_frame = self.next_frame

    def get_led(self):
        """Convert (x, y) coordinate to (strip, led) coordinate"""
        strip, led = -1, -1  # default not found

        for strip_num, big_coord in enumerate(square_func.BIG_COORD):
            big_x, big_y = big_coord
            ll_x, ll_y = big_x * square_func.SQUARE_SIZE, big_y * square_func.SQUARE_SIZE  # ll = lower-left corner of the display
            if ll_x <= self.x < (ll_x + square_func.SQUARE_SIZE) and ll_y <= self.y < (ll_y + square_func.SQUARE_SIZE):
                strip = strip_num
                led = LED_LOOKUP[self.x - ll_x][self.y - ll_y]  # May need to swap these

        return strip, led
