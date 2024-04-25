import numpy as np
from random import randint
from time import time

from ...source import Source

class RandomChase(Source):
    def __init__(self,
                 name: str,
                 order: int,
                 width: int,
                 height: int,
                 orientation: str = 'vertical',
                 fps: int = 60
                ):
        super().__init__(name, order, width, height)
        self.properties['fps'] = fps
        self.properties['orientation'] = orientation
        self.last_frame_time = 0
        self.edit_if = ['width', 'height', 'orientation']
        self.reset()
    
    def reset(self) -> None:
        self.frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.frame[:] = 0

    def get_rgb(self) -> np.ndarray:
        r = randint(0, 255) if randint(0, 5) == 0 else self.frame[0, 0, 0]
        g = randint(0, 255) if randint(0, 5) == 0 else self.frame[0, 0, 1]
        b = randint(0, 255) if randint(0, 5) == 0 else self.frame[0, 0, 2]
        return [r, g, b]

    def _horizontal_create_frame(self) -> None:
        self.frame[1:] = self.frame[:-1]
        self.frame[0, :] = self.get_rgb()

    def _vertical_create_frame(self) -> None:
        self.frame[:, 1:] = self.frame[:, :-1]
        self.frame[:, 0] = self.get_rgb()

    def update(self) -> None:

        if self.properties.cache:
            for prop in self.properties.cache:
                if prop in self.edit_if:
                    self.reset()
                    break
            self.properties.reset_cache()

        if time() - self.last_frame_time > 1 / self.properties['fps']:
            self.last_frame_time = time()

            try:
                if self.properties['orientation'] == 'horizontal':
                    self._horizontal_create_frame()
                elif self.properties['orientation'] == 'vertical':
                    self._vertical_create_frame()
            except IndexError:
                self.reset()

    def create_frame(self) -> None:
        pass
