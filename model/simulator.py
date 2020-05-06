"""
Simulator sends colors to the Processing visualizer
Simulator use its own 1 Square model composed of pixels to keep track of simulator current and next frames
All the simulator logic is here
On the receiving end, Processing does no calculations, just turning on squarees with colors as the messages arrive
Sending simulator frame rate is in go_dmx.py, ChannelRunner.__init__():
  self.simulator = SimulatorModel(frame_rate=10, hostname="localhost", port=4444) if has_simulator else None
Frame rate will throttle how fast Processing gets updates, but should not affect LED lighting,
unless the Processing drawing is slow and expensive

"""
import datetime
import socket

from square import Square
import color as color_func


class SimulatorModel(object):
    def __init__(self, frame_rate, hostname="localhost", port=4444):
        self.frame_rate = frame_rate
        self.last_update = datetime.datetime.now()
        self.next_update = self._get_next_update()
        self.server = (hostname, port)
        self.sock = None
        self.square_model = Square()  # This square model of pixels is unique to the Simulator
        self.connect()

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.server)

    def _get_next_update(self):
        return self.last_update + datetime.timedelta(seconds=1.0 / self.frame_rate)

    def _needs_update(self):
        """Does the Simulator need updating?"""
        return datetime.datetime.now() > self.next_update

    def set(self, coord, color):
        """Set the coord's next_frame to color"""
        self.square_model.set_cell(coord, color)

    def go(self):
        """If the frame is up, push all changed pixels to the simulator"""
        if self._needs_update():
            self._send_pixels()
            self.square_model.push_next_to_current_frame()
            self.last_update = datetime.datetime.now()
            self.next_update = self._get_next_update()

    def _send_pixels(self):
        """Send all of the changed pixels to the visualizer"""
        for pixel in self.square_model.all_onscreen_pixels():
            if pixel.has_changed():
                x, y = pixel.get_coord()
                hue, sat, val = pixel.next_frame
                hsv_int = color_func.color_to_int(hue, sat, val)

                msg = "{},{},{}".format(x, y, hsv_int)
                msg += "\n"
                # print(msg)
                self.sock.sendto(msg.encode(), self.server)
