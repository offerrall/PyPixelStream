from numpy import ndarray, uint8

from ..image_operations.image_operations import (kivy_read_image,
                                                 nearest_neighbor_resize_vectorized,
                                                 resize_mask_nearest_neighbor)

from ..filter import Filter

class WhiteMask(Filter):
    def __init__(self,
                 name: str = "white_mask",
                 order: int = 0,
                 image_path: str = "",
                 invert: bool = False):
        super().__init__(name, order)
        self.properties["image_path"] = image_path
        self.properties["invert"] = invert
        self.cache_mask = None
    
    def create_mask(self, frame: ndarray, mask: ndarray | None = None) -> ndarray:
        try:
            img = kivy_read_image(self.properties["image_path"], alpha=False)
        except:
            self.properties["image_path"] = ""
            return None
        img_array = img[0]
        if img_array.shape[0] > frame.shape[0] or img_array.shape[1] > frame.shape[1]:
            img_array = nearest_neighbor_resize_vectorized(img_array, frame.shape[1], frame.shape[0])
        
        white_mask = (img_array[:, :, 0] == 255) & (img_array[:, :, 1] == 255) & (img_array[:, :, 2] == 255)
        white_mask = white_mask.astype(uint8) * 255

        if self.properties["invert"]:
            white_mask = ~white_mask

        return white_mask

    def apply(self, frame: ndarray, mask: ndarray | None = None) -> tuple[ndarray, ndarray]:
        if self.properties["image_path"] == "":
            return frame, mask
        
        force_update = False
        if self.properties.cache:
            edit_if = ['image_path', 'invert']

            for prop in self.properties.cache:
                if prop in edit_if:
                    force_update = True
                    break

            self.properties.reset_cache()
        
        if not self.cache_mask is None:
            if frame.shape[0] != self.cache_mask.shape[0] or frame.shape[1] != self.cache_mask.shape[1]:
                force_update = True
        
        if self.cache_mask is None or force_update:
            self.cache_mask = self.create_mask(frame, mask)
            if self.cache_mask is None:
                return frame, mask
        
        if mask is None:
            mask = self.cache_mask
        else:
            mask = mask & self.cache_mask

        return frame, mask

