import numpy as np
from time import time

from ...source import Source

class RainbowTwister(Source):
    def __init__(self,
                 name: str,
                 order: int,
                 width: int,
                 height: int,
                 fps: int = 60):
        super().__init__(name, order, width, height)
        self.properties['fps'] = fps
        self.last_time = time()
        self.edit_if = ['width', 'height']
        self.initialize_effect()

    def initialize_effect(self):
        self.t = 0
        self.scaleXY = 4
        self.center_x = self.width // 2
        self.center_y = self.height // 2
        x = np.linspace(-self.center_x, self.center_x, self.width)
        y = np.linspace(-self.center_y, self.center_y, self.height)
        xv, yv = np.meshgrid(x, y, sparse=False, indexing='xy')
        self.noise3d_angle = (128 * (np.arctan2(yv, xv) / np.pi) + 128).astype(np.uint8) % 256
        self.noise3d_radius = (np.hypot(xv, yv)).astype(np.uint8) % 256

    def get_next_frame(self):
        self.t += 1
        hue = (self.noise3d_angle * self.scaleXY - self.t + self.noise3d_radius * self.scaleXY) % 256
        saturation = np.full_like(hue, 255)
        value = np.full_like(hue, 255)
        
        frame = self.hsv_to_rgb(hue, saturation, value)
        self.frame = frame.reshape(self.height, self.width, 3)

    def update(self):
        force_update = False
        if self.properties.cache:
            for prop in self.properties.cache:
                if prop in self.edit_if:
                    self.initialize_effect()
                    force_update = True
                    break

            self.properties.reset_cache()
        
        if time() - self.last_time > 1 / self.properties['fps'] or force_update:
            self.get_next_frame()
            self.last_time = time()

    def hsv_to_rgb(self, h, s, v):
        h = h / 256.0 * 360
        s = s / 255.0
        v = v / 255.0
        
        c = v * s
        x = c * (1 - np.abs(((h / 60) % 2) - 1))
        m = v - c
        
        zeros = np.zeros_like(h)
        r, g, b = np.select(
            [
                h < 60, h < 120, h < 180, h < 240, h < 300, h >= 300
            ],
            [
                (c, x, zeros),
                (x, c, zeros),
                (zeros, c, x),
                (zeros, x, c),
                (x, zeros, c),
                (c, zeros, x)
            ],
            default=(zeros, zeros, zeros)
        )
        
        r, g, b = ((r + m) * 255, (g + m) * 255, (b + m) * 255)
        return np.stack((r, g, b), axis=-1).astype(np.uint8)
