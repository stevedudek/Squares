"""
Reworking LED code to use a Pixel class

A LED-contraption object, like a Square, is composed of Pixel objects
A Pixel knows its color, state, current frame, and next frame
"""


class Pixel(object):
    """
    Pixel colors are hsv [0-255] triples (very simple)
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.curr_frame = (0,0,0)
        self.next_frame = (0,0,0)

    def get_coord(self):
        return self.x, self.y

    def get_next_color(self):
        return self.next_frame

    def has_changed(self):
        return not (self.curr_frame[0] == self.next_frame[0] and
                    self.curr_frame[1] == self.next_frame[1] and
                    self.curr_frame[2] == self.next_frame[2])

    def set_next_frame(self, color):
        self.next_frame = color

    def set_curr_frame(self, color):
        self.curr_frame = color

    def set_black(self):
        self.next_frame = (0,0,0)

    def force_black(self):
        self.curr_frame = (0,0,1)
        self.set_black()

    def update_frame(self):
        self.set_curr_frame(color=self.next_frame)