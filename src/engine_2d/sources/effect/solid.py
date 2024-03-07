from numpy import full, uint8, ndarray

from ...source import Source

class SolidColor(Source):

    def __init__(self,
                 name: str,
                 order: int,
                 width: int,
                 height: int,
                 color: tuple[int, int, int] = (0, 0, 255)):
        super().__init__(name, order, width, height)
        self.properties['color'] = color

    def create_solid_color(self) -> None:
        self.frame = full((self.height,
                           self.width, 3),
                           self.properties['color'],
                           dtype=uint8)

    def update(self) -> None:

        if self.properties.cache:
            edit_if = ['color', 'width', 'height']

            for prop in self.properties.cache:
                if prop in edit_if:
                    self.create_solid_color()
                    break

            self.properties.reset_cache()