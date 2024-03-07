from numpy import ndarray, repeat

from ..filter import Filter

class Grayscale(Filter):
    def __init__(self,
                 name: str = "grayscale",
                 order: int = 0):
        super().__init__(name, order)

    def apply(self,
              frame: ndarray,
              mask: ndarray | None = None
              ) -> tuple[ndarray, ndarray]:
        gray = frame.mean(axis=2, keepdims=True)
        frame = repeat(gray, 3, axis=2)

        return frame, mask