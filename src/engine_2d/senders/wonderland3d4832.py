from numpy import ndarray, array, flipud, concatenate, zeros
import socket
from time import sleep

from ..send import SendDevice

class WonderLand3d4832Device(SendDevice):
    def __init__(self,
                    name: str,
                    order: int = 0,
                    is_active: bool = True,
                    ip: str = '',
                    port: int = 0,
                    x: int = 0,
                    y: int = 0) -> None:
        width = 48
        height = 32
        super().__init__(name, order, width, height, is_active, x, y)
        self.ip: str = ip
        self.port: int = port
        self.frame_num: int = 0
        self.internal_frame_buffer = zeros((32, 48, 3), dtype='uint8')

    def panel_to_strip(self, panel: ndarray) -> ndarray:
        """
        This function takes a 16x16 panel and returns a 256x1 strip in the correct order
        The panel as connected to the LED strip is ordered in a zigzag pattern, like this:
        0  1  2  3  4  5  6
        13 12 11 10 9  8  7
        14 15 16 17 18 19 20
        27 26 25 24 23 22 21
        """
        panel[1::2] = panel[1::2, ::-1]
        return panel.ravel()

    def image_to_panels(self, image: ndarray) -> ndarray:
        """
        This function takes a image and returns a list of 16x16 panels.
        Example a 48x32 image will return a list of 6 panels, each one of 16x16 pixels in the order:
        0 1 2
        3 4 5
        """
        return array([flipud(image[i:i+16, j:j+16])
                      for i in range(0, image.shape[0], 16)
                      for j in range(0, image.shape[1], 16)])

    def send_image_via_ws(self, image: ndarray) -> None:
        """
        This function sends an image to the device via UDP.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        chunks_num = 4
        panels = self.image_to_panels(image)
        panels_strip_ = [self.panel_to_strip(panel) for panel in panels]
        panels_strip_ = concatenate(panels_strip_)

        chunk_size = int(len(panels_strip_) / chunks_num)
        chunks = [panels_strip_[i:i+chunk_size] for i in range(0, len(panels_strip_), chunk_size)]
        
        for i in range(chunks_num):
            packet = self.frame_num.to_bytes(1, 'big')
            packet += i.to_bytes(1, 'big')
            packet += chunks[i].tobytes()
            sock.sendto(packet, (self.ip, self.port))
            sleep(0.002)
        
        self.frame_num += 1
        if self.frame_num == 201:
            self.frame_num = 0

    def send_frame(self, frame: ndarray) -> None:
        """
        Updates the internal frame buffer with the new frame and sends it to the device.
        The frame is cropped to the device size and position.
        """
        self.internal_frame_buffer.fill(0)
        frame_width, frame_height = frame.shape[1], frame.shape[0]
        device_width, device_height = self.width, self.height
        left = max(0, self.x)
        right = min(frame_width, self.x + device_width)
        top = max(0, self.y)
        bottom = min(frame_height, self.y + device_height)

        if right > left and bottom > top:
            frame_slice = frame[top:bottom, left:right]

            buffer_x1 = max(0, -self.x)
            buffer_y1 = max(0, -self.y)
            buffer_x2 = buffer_x1 + (right - left)
            buffer_y2 = buffer_y1 + (bottom - top)

            self.internal_frame_buffer[buffer_y1:buffer_y2, buffer_x1:buffer_x2] = frame_slice

        try:
            self.send_image_via_ws(self.internal_frame_buffer)
        except Exception as e:
            print(f"Error sending frame to device {self.name}: {e}")
