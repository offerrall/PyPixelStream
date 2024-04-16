from numpy import ndarray, roll

from ..filter import Filter

class WrapAroundShift(Filter):
    def __init__(self,
                 name: str = "wrap_around_shift",
                 order: int = 0,
                 shift_x: int = 1,
                 shift_y: int = 1):
        super().__init__(name, order)
        self.properties["shift_x"] = shift_x
        self.properties["shift_y"] = shift_y

        self.accumulated_shift_x = 0
        self.accumulated_shift_y = 0
        self.edit_if = ['shift_x', 'shift_y']

    def reset(self):
        self.accumulated_shift_x = 0
        self.accumulated_shift_y = 0

    def apply(self, frame: ndarray, mask: ndarray | None = None) -> tuple[ndarray, ndarray]:

        if self.properties.cache:
            for prop in self.properties.cache:
                if prop in self.edit_if:
                    self.reset()
                    break

            self.properties.reset_cache()

        self.accumulated_shift_x += self.properties["shift_x"] / 10
        self.accumulated_shift_y += self.properties["shift_y"] / 10
        
        frame_height, frame_width = frame.shape[:2]
        self.accumulated_shift_x %= frame_width
        self.accumulated_shift_y %= frame_height

        accumulated_shift_x = int(self.accumulated_shift_x)
        accumulated_shift_y = int(self.accumulated_shift_y)
        
        shifted_frame = roll(frame, shift=(accumulated_shift_y, accumulated_shift_x), axis=(0, 1))
        if mask is not None:
            shifted_mask = roll(mask, shift=(accumulated_shift_y, accumulated_shift_x), axis=(0, 1))
        else:
            shifted_mask = None

        return shifted_frame, shifted_mask