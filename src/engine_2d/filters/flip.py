from numpy import ndarray

from ..filter import Filter

class Flip(Filter):
    
    def __init__(self,
                 name: str = "flip",
                 order: int = 0,
                 flip_x: bool = False,
                 flip_y: bool = False):
            super().__init__(name, order)
            self.properties["flip_x"] = flip_x
            self.properties["flip_y"] = flip_y
            
    def apply(self, frame: ndarray, mask: ndarray | None = None) -> tuple[ndarray, ndarray]:

        if self.properties["flip_x"]:
            frame = frame[:, ::-1]
            if mask is not None:
                mask = mask[:, ::-1]
        if self.properties["flip_y"]:
            frame = frame[::-1, :]
            if mask is not None:
                mask = mask[::-1, :]
        return frame, mask