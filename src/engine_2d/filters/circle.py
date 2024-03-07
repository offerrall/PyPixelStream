from numpy import ndarray, ogrid, sqrt

from ..filter import Filter

class CircleMask(Filter):
    def __init__(self,
                 name: str = "circle_mask",
                 order: int = 0,
                 radius: int = 10,
                 invert: bool = False):
        super().__init__(name, order)
        self.properties["radius"] = radius
        self.properties["invert"] = invert
        self.last_mask = None
        self.last_frame_shape = None

    def apply(self, frame: ndarray, mask: ndarray | None = None) -> tuple[ndarray, ndarray]:

        force_edit = False
        if self.properties.cache:
            edit_if = ['radius', 'invert']

            for prop in self.properties.cache:
                if prop in edit_if:
                    force_edit = True
                    break

            self.properties.reset_cache()

        current_frame_shape = frame.shape[:2]

        if self.last_frame_shape != current_frame_shape or force_edit:
            center = (frame.shape[1] // 2, frame.shape[0] // 2)
            radius = self.properties["radius"]
            Y, X = ogrid[:frame.shape[0], :frame.shape[1]]
            dist_from_center = sqrt((X - center[0])**2 + (Y - center[1])**2)
            circle_mask = dist_from_center <= radius
            if self.properties["invert"]:
                circle_mask = ~circle_mask
            self.last_mask = circle_mask
            self.last_frame_shape = current_frame_shape
        else:
            circle_mask = self.last_mask

        if mask is not None:
            combined_mask = mask & circle_mask
        else:
            combined_mask = circle_mask

        return frame, combined_mask