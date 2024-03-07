import numpy as np
from time import time

from ...source import Source

class Rainbow(Source):
    def __init__(self,
                 name: str,
                 order: int,
                 width: int,
                 height: int,
                 fps: int = 60):
        super().__init__(name, order, width, height)
        
        self.properties['fps'] = fps
        self.current_hue = 0
        self.last_frame_time = 0
        self.reset()

    def reset(self) -> None:
        self.frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.current_hue = 0
        self.update_rainbow()

    def update(self) -> None:
        force_reset = False
        
        edit_if = ['width', 'height']
        for prop in self.properties.cache:
            if prop in edit_if:
                self.reset()
                self.properties.reset_cache()
                force_reset = True
                break

        if time() - self.last_frame_time > 1 / self.properties['fps'] or force_reset:
            self.last_frame_time = time()
            self.create_frame()

    def create_frame(self) -> None:
        self.update_rainbow()

    def update_rainbow(self):
        self.current_hue = (self.current_hue + 1) % 360
        hues = (self.current_hue + np.arange(self.height)) % 360
        
        colors = np.array([self.hue_to_rgb(hue) for hue in hues])
        
        self.frame[:] = colors[:, np.newaxis, :]

    def hue_to_rgb(self, hue):
        h = hue / 60.0
        c = 255
        x = c * (1 - abs(h % 2 - 1))
        
        if h < 1:
            r, g, b = c, x, 0
        elif h < 2:
            r, g, b = x, c, 0
        elif h < 3:
            r, g, b = 0, c, x
        elif h < 4:
            r, g, b = 0, x, c
        elif h < 5:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        
        return int(r), int(g), int(b)