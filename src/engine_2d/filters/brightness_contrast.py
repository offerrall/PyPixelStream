from numpy import ndarray, clip, uint8

from ..filter import Filter

class BrightnessContrast(Filter):
    def __init__(self,
                 name: str = "brightness contrast",
                 order: int = 0,
                 brightness: float = 0.0,
                 contrast: float = 1.0):
        super().__init__(name, order)
        self.properties["brightness"] = brightness
        self.properties["contrast"] = contrast

    def apply(self,
              frame: ndarray,
              mask: ndarray | None = None
              ) -> tuple[ndarray, ndarray]:

        cont = self.properties["contrast"] / 100
        bright = self.properties["brightness"] / 100
        adjusted = frame * (cont + 1.0) - cont + bright * 255
        adjusted = clip(adjusted, 0, 255).astype(uint8)

        return adjusted, mask