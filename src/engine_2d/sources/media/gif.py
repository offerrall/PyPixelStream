from PIL import Image, ImageSequence
import time
from numpy import asarray, full, uint8

from ...source import Source
from ...text import set_text_to_frame
from ...image_operations.image_operations import (nearest_neighbor_resize_vectorized,
                                                 resize_mask_nearest_neighbor)

class GIF(Source):
    def __init__(self,
                 name: str,
                 order: int,
                 width: int,
                 height: int,
                 path: str = ""):
        super().__init__(name, order, width, height)
        self.properties['path'] = path
        self.frames = []

    def reset(self):
        self.mask = None
        self.frame = None
        self.frames = []
        self.durations = []
        self.current_frame = 0
        self.last_update_time = time.time()
        self.frame_duration_seconds = 0
    
    def load_frames(self) -> bool:
        try:
            with Image.open(self.properties['path']) as img:
                self.original_width, self.original_height = img.size
                for frame in ImageSequence.Iterator(img):
                    self.frames.append(frame.copy())
                    self.durations.append(frame.info['duration'] / 1000.0)
            return True
        except:
            self.no_gif()
            return False

    def get_next_frame(self, force_update: bool=False):
        current_time = time.time()
        time_elapsed_since_last_update = current_time - self.last_update_time

        if time_elapsed_since_last_update >= self.frame_duration_seconds or force_update:
            if self.current_frame >= len(self.frames):
                self.current_frame = 0

            frame = self.frames[self.current_frame]
            self.frame_duration_seconds = self.durations[self.current_frame]
            self.current_frame += 1
            self.last_update_time = current_time
            return frame
        else:
            return None

    def disconnect(self) -> None:
        self.reset()
    
    def no_gif(self, text: str = "No gif\nSelected") -> None:
        self.properties['path'] = ""
        self.frame = full((self.height,
                           self.width, 3),
                           (0, 0, 0),
                           dtype=uint8)
        self.mask = None
        set_text_to_frame(text, self.frame, self.mask, "xsans", (255, 255, 255))
    
    def update(self):
        force_update = False
        if self.properties.cache:
            edit_if = ['path']
            force_if = ['width', 'height']

            for prop in self.properties.cache:
                if prop in edit_if:
                    self.reset()
                    force_update = True
                    break
                elif prop in force_if:
                    force_update = True
                    break

            self.properties.reset_cache()
        
        if not self.properties['path']:
            self.no_gif()
            return
        
        if not self.frames:
            check = self.load_frames()
            if not check:
                return
        
        frame = self.get_next_frame(force_update=force_update)
        mask = None
        if frame is not None:
            if frame.mode == 'RGBA':
                frame_array = asarray(frame)
                mask = frame_array[:, :, 3]
                frame_array = frame_array[:, :, :3]
            elif frame.mode != 'RGB':
                frame = frame.convert('RGB')
                frame_array = asarray(frame)
            else:
                frame_array = asarray(frame)

            resized_frame = nearest_neighbor_resize_vectorized(frame_array, self.width, self.height)
            
            if mask is not None:
                resized_mask = resize_mask_nearest_neighbor(mask, self.width, self.height)
                self.mask = resized_mask
            
            self.frame = resized_frame