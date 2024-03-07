from kivy.uix.video import Video as VideoKivy
from numpy import full, uint8
from os.path import exists

from ...source import Source
from ...text import set_text_to_frame
from ...image_operations.image_operations import texture_to_np_array, nearest_neighbor_resize_vectorized


class Video(Source):

    def __init__(self,
                 name: str,
                 order: int,
                 width: int,
                 height: int,
                 video_volume: bool = False,
                 video_path: str = ""):
        super().__init__(name, order, width, height)
        self.properties['video_path'] = video_path
        self.properties['video_volume'] = video_volume
        self.video_kivy = None
        
        if not exists(video_path):
            self.not_video()
            self.properties['video_path'] = ""

    def init_video(self) -> None:
        try:
            self.video_kivy = VideoKivy(source=self.properties['video_path'], state='play', volume=int(self.properties['video_volume']))
            return True
        except:
            self.not_video()
            self.properties['video_path'] = ""
            return False

    def set_volume(self, volume: float) -> None:
        if self.video_kivy:
            self.video_kivy.volume = volume

    def not_video(self, text: str = "No video\nSelected") -> None:
        self.frame = full((self.height,
                           self.width, 3),
                           (0, 0, 0),
                           dtype=uint8)
        self.mask = None
        set_text_to_frame(text, self.frame, self.mask, "xsans", (255, 255, 255))

    def update_frame(self) -> None:
        if not self.properties['video_path']:
            self.not_video()
            return
        
        if not self.mask is None:
            self.mask = None
        if not self.video_kivy:
            check = self.init_video()
            if not check:
                return

        if not self.video_kivy.state == 'play':
            self.video_kivy.state = 'play'

        if self.video_kivy.texture:
            self.frame, _ = texture_to_np_array(self.video_kivy.texture)
            self.frame = nearest_neighbor_resize_vectorized(self.frame, self.width, self.height)

    def update(self) -> None:
        if self.properties.cache:
            
            if "video_volume" in self.properties.cache:
                self.set_volume(int(self.properties['video_volume']))

            edit_if = ['video_path']

            for prop in self.properties.cache:
                if prop in edit_if:
                    self.init_video()
                    break

            self.properties.reset_cache()
        
        self.update_frame()

    def disconnect(self) -> None:
        if self.video_kivy:
            self.video_kivy.unload()
        self.video_kivy = None

            
            