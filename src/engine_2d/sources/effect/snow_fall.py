import numpy as np
from random import randint
from time import time

from ...source import Source

class SnowFall(Source):
    def __init__(self,
                 name: str,
                 order: int,
                 width: int,
                 height: int,
                 snow_color: tuple[int, int, int] = (255, 255, 255),
                 background_color: tuple[int, int, int] | None = (255, 0, 0),
                 transparent_background: bool = True,
                 fps: int = 60,
                 snowflake_chance: int = 60):
        super().__init__(name, order, width, height)

        self.properties['snow_color'] = snow_color
        self.properties['background_color'] = background_color
        self.properties['transparent_background'] = transparent_background
        self.properties['fps'] = fps
        self.properties['snowflake_chance'] = snowflake_chance

        self.last_frame_time = 0
        self.reset()

    def reset(self) -> None:
        self.frame = np.full((self.height, self.width, 3), self.properties['background_color'], dtype=np.uint8)
        self.mask = None

    def update(self) -> None:

        edit_if = ['snow_color', 'background_color', 'transparent_background', 'width', 'height']
        force_reset = False

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

        snow_color = np.array(self.properties['snow_color'], dtype=np.uint8)
        background_color = np.array(self.properties['background_color'], dtype=np.uint8)

        if np.all(self.frame == snow_color):
            self.reset()

        snowflake_chance = self.properties['snowflake_chance']
        new_snowflakes = np.random.randint(1, snowflake_chance + 1, (1, self.width)) == 1
        self.frame[0, new_snowflakes[0]] = snow_color

        for y in range(self.height - 2, -1, -1):
            snow_here = np.all(self.frame[y, :] == snow_color, axis=-1)
            no_snow_below = ~np.all(self.frame[y + 1, :] == snow_color, axis=-1)
            can_move_down = snow_here & no_snow_below
            self.frame[y + 1, can_move_down] = snow_color
            self.frame[y, can_move_down] = background_color

        if self.properties['transparent_background']:
            self.mask = np.all(self.frame == snow_color, axis=-1)