from numpy import ndarray, abs, clip, uint8

from ..filter import Filter

class ChromaKey(Filter):
    def __init__(self,
                 name: str = "chroma_key",
                 order: int = 0,
                 target_color: tuple[int, int, int] = (0, 255, 0),
                 tolerance: int = 1):
        super().__init__(name, order)
        self.properties["target_color"] = target_color
        self.properties["tolerance"] = tolerance

    def apply(self,
              frame: ndarray,
              mask: ndarray | None = None
              ) -> tuple[ndarray, ndarray]:
        target_r, target_g, target_b = self.properties["target_color"]
        frame_r, frame_g, frame_b = frame[:,:,0], frame[:,:,1], frame[:,:,2]

        mask_r = abs(frame_r - target_r) < self.properties["tolerance"]
        mask_g = abs(frame_g - target_g) < self.properties["tolerance"]
        mask_b = abs(frame_b - target_b) < self.properties["tolerance"]

        chroma_key_mask = ~(mask_r & mask_g & mask_b)

        if mask is not None:
            combined_mask = mask & chroma_key_mask
        else:
            combined_mask = chroma_key_mask

        return frame, combined_mask.astype(uint8)