import numpy as np
from time import time

from ...source import Source

class GameOfLife(Source):
    def __init__(self,
                 name: str,
                 order: int,
                 width: int,
                 height: int,
                 color: tuple[int, int, int] = (255, 255, 255),
                 background: tuple[int, int, int] = (0, 0, 0),
                 background_transparent: bool = False,
                 fps: int = 60
                ):
        super().__init__(name, order, width, height)
        self.properties['color'] = color
        self.properties['background'] = background
        self.properties['background_transparent'] = background_transparent
        self.properties['fps'] = fps
        self.last_frame_time = 0
        self.previous_grid = None
        self.grid_before_last = None
        self.edit_if = ['width', 'height', 'background_transparent']
        self.reset()
        
    def reset(self) -> None:
        self.mask = None
        self.grid = np.random.randint(2, size=(self.height, self.width), dtype=np.uint8)
        self.previous_grid = np.zeros_like(self.grid)
        self.grid_before_last = np.zeros_like(self.grid)
        self.create_frame()

    def update(self) -> None:
        
        if self.properties.cache:
            for prop in self.properties.cache:
                if prop in self.edit_if:
                    self.reset()
                    break
            self.properties.reset_cache()

        if time() - self.last_frame_time > 1 / self.properties['fps']:
            self.last_frame_time = time()
            self.next_generation()
            if np.array_equal(self.grid, self.previous_grid):
                self.reset()
            elif np.array_equal(self.grid, self.grid_before_last):
                self.reset()
            elif not np.any(self.grid):
                self.reset()
            self.grid_before_last = self.previous_grid.copy()
            self.previous_grid = self.grid.copy()

    def next_generation(self) -> None:
        neighbor_count = sum(np.roll(np.roll(self.grid, i, 0), j, 1)
                             for i in (-1, 0, 1) for j in (-1, 0, 1)
                             if (i != 0 or j != 0))
        self.grid = ((self.grid == 1) & ((neighbor_count == 2) | (neighbor_count == 3))) | \
                    ((self.grid == 0) & (neighbor_count == 3))
        self.create_frame()

    def create_frame(self) -> None:
        if not self.properties['background_transparent']:
            color_array = np.array(self.properties['color'], dtype=np.uint8)
            background_array = np.array(self.properties['background'], dtype=np.uint8)
            self.frame = np.where(self.grid[..., None], color_array, background_array)
        else:
            self.frame = np.where(self.grid[..., None], self.properties['color'], 0)
            self.mask = self.grid.astype(np.uint8)

