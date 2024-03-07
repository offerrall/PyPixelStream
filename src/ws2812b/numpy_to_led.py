import numpy as np
from time import sleep
import socket


def panel_to_strip(panel: np.ndarray) -> np.ndarray:
    """
    This function takes a 16x16 panel and returns a 256x1 strip in the correct order
    The panel as connected to the LED strip is ordered in a zigzag pattern, like this:
    0  1  2  3  4  5  6
    13 12 11 10 9  8  7
    14 15 16 17 18 19 20
    27 26 25 24 23 22 21
    """
    reordered_image = np.copy(panel)
    height, width, _ = panel.shape

    for y in range(height):
        if y % 2 != 0:
            reordered_image[y] = panel[y][::-1]

    return reordered_image.flatten()

def image_to_panels(image: np.ndarray) -> np.ndarray:
    """
    This function takes a image and returns a list of 16x16 panels.
    Example a 48x32 image will return a list of 6 panels, each one of 16x16 pixels in the order:
    0 1 2
    3 4 5
    """
    res_x, res_y = image.shape[0], image.shape[1]
    panels = []
    
    for i in range(0, res_x, 16):
        for j in range(0, res_y, 16):
            panels.append(image[i:i+16, j:j+16])
    panels = [np.flipud(panel) for panel in panels]
    return panels

def send_image_via_ws(image: np.ndarray) -> None:

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip = "192.168.1.105" # tmp ip
    port = 8888 # tmp port
    chunks_num = 4
    panels = image_to_panels(image)
    panels_strip_ = [panel_to_strip(panel) for panel in panels]
    panels_strip_ = np.concatenate(panels_strip_)
    
    chunk_size = int(len(panels_strip_) / chunks_num)
    chunks = [panels_strip_[i:i+chunk_size] for i in range(0, len(panels_strip_), chunk_size)]
    
    
    for i in range(chunks_num):
        packet = i.to_bytes(1, 'big')
        packet += chunks[i].tobytes()
        sock.sendto(packet, (ip, port))
        sleep(0.002)
    
    
    
        