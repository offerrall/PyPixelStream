import numpy as np
from time import time
import colorsys

from ...source import Source


class ColorFrizzles(Source):
    def __init__(self,
                 name: str,
                 order: int,
                 width: int,
                 height: int,
                 fps: int = 60,
                 transparent_background: bool = True,
                 ):
        
        super().__init__(name, order, width, height)
        self.properties['fps'] = fps
        self.properties['transparent_background'] = transparent_background
        self.last_frame_time = 0
        self.edit_if = ['width', 'height', 'transparent_background']
        self.reset()

    def reset(self):
        self.frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.mask = None

    def update(self):
        force_update = False
        if self.properties.cache:
            for prop in self.properties.cache:
                if prop in self.edit_if:
                    self.reset()
                    force_update = True
                    break

            self.properties.reset_cache()

        current_time = time()
        if current_time - self.last_frame_time > 1 / self.properties['fps'] or force_update:
            self.last_frame_time = current_time
            self.draw()

    def fade_to_black_by(self, amount=16):
        fade_value = 1 - amount / 255
        self.frame = (self.frame * fade_value).astype(np.uint8)

    def beatsin8(self, beats_per_minute, lowest, highest):
        time = self.last_frame_time
        scale = highest - lowest
        beat = np.sin(time * np.pi * beats_per_minute / 30)
        return int(((beat + 1) / 2) * scale + lowest)

    def draw(self):
        self.fade_to_black_by(16)

        for i in range(8, 0, -1):
            x = self.beatsin8(12 + i, 0, self.width - 1)
            y = self.beatsin8(15 - i, 0, self.height - 1)
            self.add_color(x, y, self.hsv_to_rgb(self.beatsin8(12, 0, 255), 255, 255))

            if self.width > 24 or self.height > 24:
                self.add_color(x + 1, y, self.hsv_to_rgb(self.beatsin8(12, 0, 255), 255, 255))
                self.add_color(x - 1, y, self.hsv_to_rgb(self.beatsin8(12, 0, 255), 255, 255))
                self.add_color(x, y + 1, self.hsv_to_rgb(self.beatsin8(12, 0, 255), 255, 255))
                self.add_color(x, y - 1, self.hsv_to_rgb(self.beatsin8(12, 0, 255), 255, 255))
        if self.properties['transparent_background']:
            self.mask = self.frame[:, :, 0] != 0

    def add_color(self, x, y, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.frame[y, x] = np.clip(self.frame[y, x] + color, 0, 255)

    def hsv_to_rgb(self, h, s, v):
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h/255.0, s/255.0, v/255.0))
