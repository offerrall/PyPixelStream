from kivy.uix.camera import Camera
from numpy import full, uint8, rot90
from kivy.utils import platform

from ...image_operations.image_operations import texture_to_np_array, nearest_neighbor_resize_vectorized
from ...text import set_text_to_frame
from ...source import Source

class WebCam(Source):
    
        def __init__(self,
                    name: str,
                    order: int,
                    width: int,
                    height: int,
                    camera_index: int = 0):
            super().__init__(name, order, width, height)
            self.properties['camera_index'] = camera_index
            self.camera = None

        def init_camera(self) -> None:
            self.camera = Camera(play=True,
                                 index=self.properties['camera_index'],
                                 resolution=(640, 480))
        
        def update_frame(self) -> None:
            if not self.camera:
                self.init_camera()
    
            if self.camera.texture:
                frame, _ = texture_to_np_array(self.camera.texture)
                if platform == "macosx":
                    # Mac OS X returns the frame in the wrong orientation so we need to rotate it
                    frame = rot90(frame, 3)

                self.frame = nearest_neighbor_resize_vectorized(frame, self.width, self.height)

        def update(self) -> None:
            try:
                self.update_frame()
            except TypeError:
                error = "No camera\ndetected"
                self.frame = full((self.height, self.width, 3), (0, 0, 0), dtype=uint8)
                self.mask = None
                set_text_to_frame(error, self.frame, self.mask, "xsans", (255, 255, 255))
        
        def disconnect(self) -> None:
            if self.camera:
                self.camera.play = False
                self.camera = None