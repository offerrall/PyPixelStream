from numpy import full, uint8

from ...source import Source
from ...text import set_text_to_frame
from ...image_operations.image_operations import (kivy_read_image,
                                                          nearest_neighbor_resize_vectorized,
                                                          resize_mask_nearest_neighbor)

class Image(Source):

    def __init__(self,
                 name: str,
                 order: int,
                 width: int,
                 height: int,
                 image_path: str = ""):
        super().__init__(name, order, width, height)
        self.properties['image_path'] = image_path

    def update(self) -> None:
        if self.properties.cache:
            edit_if = ['image_path', 'width', 'height']

            for prop in self.properties.cache:
                if prop in edit_if:
                    self.create_image()
                    break

            self.properties.reset_cache()

    def no_image(self, text: str = "No image\nSelected") -> None:
        self.frame = full((self.height,
                           self.width, 3),
                           (0, 0, 0),
                           dtype=uint8)
        self.mask = None
        set_text_to_frame(text, self.frame, self.mask, "xsans", (255, 255, 255))

    def create_image(self) -> None:
        if self.properties['image_path'] == "":
            self.no_image()
            return
        
        try:
            frame, mask = kivy_read_image(self.properties['image_path'], alpha=True)
        except:
            self.no_image(f"File\nnot\nfound")
            self.properties['image_path'] = ""
            return
        
        if frame.shape[0] > self.height or frame.shape[1] > self.width:
            frame = nearest_neighbor_resize_vectorized(frame, self.width, self.height)
        self.frame = frame

        if mask.all():
            self.mask = None
            return

        if mask.shape[0] > self.height or mask.shape[1] > self.width:
            mask = resize_mask_nearest_neighbor(mask, self.width, self.height)

        self.frame = frame
        self.mask = mask
