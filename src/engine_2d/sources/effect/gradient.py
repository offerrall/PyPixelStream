import numpy as np

from ...source import Source

class Gradient(Source):

    def __init__(self,
                 name: str,
                 order: int,
                 width: int,
                 height: int,
                 start_color: tuple[int, int, int] = (0, 0, 0),
                 end_color: tuple[int, int, int] = (255, 255, 255),
                 gradient_type: str = 'linear'):
        super().__init__(name, order, width, height)
        self.properties['start_color'] = start_color
        self.properties['end_color'] = end_color
        self.properties['gradient_type'] = gradient_type

    def update(self) -> None:
        if self.properties.cache:
            edit_if = ['start_color', 'end_color', 'gradient_type', 'width', 'height']

            for prop in self.properties.cache:
                if prop in edit_if:
                    self.create_gradient()
                    break

            self.properties.reset_cache()

    def create_gradient(self) -> None:
        gradient_type = self.properties['gradient_type']
        if gradient_type == 'linear':
            self.create_linear_gradient()
        if gradient_type == 'linear_vertical':
            self.create_linear_vertical_gradient()
        elif gradient_type == 'radial':
            self.create_radial_gradient()
        elif gradient_type == 'centered_linear':
            self.create_centered_linear_gradient()

    def create_linear_vertical_gradient(self):
        start_color = np.array(self.properties['start_color'])
        end_color = np.array(self.properties['end_color'])
        gradient = np.linspace(start_color, end_color, self.height)[:, np.newaxis, :]
        self.frame = np.repeat(gradient, self.width, axis=1).astype(np.uint8)

    def create_linear_gradient(self):
        start_color = np.array(self.properties['start_color'])
        end_color = np.array(self.properties['end_color'])
        gradient = np.linspace(start_color, end_color, self.width)[np.newaxis, :, :]
        self.frame = np.repeat(gradient, self.height, axis=0).astype(np.uint8)

    def create_radial_gradient(self):
        y, x = np.ogrid[-self.height / 2: self.height / 2, -self.width / 2: self.width / 2]
        radius = np.sqrt(x**2 + y**2)
        max_radius = np.sqrt((self.width / 2)**2 + (self.height / 2)**2)
        normalized_radius = radius / max_radius
        start_color = np.array(self.properties['start_color'])
        end_color = np.array(self.properties['end_color'])
        gradient = start_color * (1 - normalized_radius[:, :, np.newaxis]) + end_color * normalized_radius[:, :, np.newaxis]
        self.frame = np.clip(gradient, 0, 255).astype(np.uint8)

    def create_centered_linear_gradient(self):
        center_x = self.width / 2
        distance_from_center = np.abs(np.linspace(-center_x, center_x, self.width))
        normalized_distance = distance_from_center / center_x
        start_color = np.array(self.properties['start_color'])[:, np.newaxis]
        end_color = np.array(self.properties['end_color'])[:, np.newaxis]
        gradient = (start_color * (1 - normalized_distance) + end_color * normalized_distance).T
        self.frame = np.repeat(gradient[np.newaxis, :, :], self.height, axis=0).astype(np.uint8)
