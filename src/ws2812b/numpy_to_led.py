import numpy as np
from time import sleep
import socket
import timeit


def panel_to_strip(panel: np.ndarray) -> np.ndarray:
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

def image_to_panels(image: np.ndarray) -> np.ndarray:
    """
    This function takes a image and returns a list of 16x16 panels.
    Example a 48x32 image will return a list of 6 panels, each one of 16x16 pixels in the order:
    0 1 2
    3 4 5
    """
    return np.array([np.flipud(image[i:i+16, j:j+16])
                     for i in range(0, image.shape[0], 16)
                     for j in range(0, image.shape[1], 16)])

def send_image_via_ws(image: np.ndarray, frame_num: int) -> None:
    """
    This is a temporary function to send an image to the led panel
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip = "192.168.0.102" # tmp ip
    port = 8888 # tmp port
    chunks_num = 4
    panels = image_to_panels(image)
    panels_strip_ = [panel_to_strip(panel) for panel in panels]
    panels_strip_ = np.concatenate(panels_strip_)

    chunk_size = int(len(panels_strip_) / chunks_num)
    chunks = [panels_strip_[i:i+chunk_size] for i in range(0, len(panels_strip_), chunk_size)]
    
    for i in range(chunks_num):
        packet = frame_num.to_bytes(1, 'big')
        packet += i.to_bytes(1, 'big')
        packet += chunks[i].tobytes()
        sock.sendto(packet, (ip, port))
        sleep(0.002)