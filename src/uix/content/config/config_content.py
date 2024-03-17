from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from engine_2d.engine import Engine
from uix.simple_popup import set_simple_popup

from uix.video_player.interactive_resize_video import InteractiveResizeVideoRender

class ConfigContent(BoxLayout):
    """
    Content of the config section
    """
    engine: Engine = ObjectProperty(None)
    video_player: InteractiveResizeVideoRender = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max_resolution = (1920, 1080)
        self.started = False
        resolution = self.engine.size
        self.ids.resolution_x.text = str(resolution[0])
        self.ids.resolution_y.text = str(resolution[1])
        self.resolution = resolution
        self.started = True
    
    def update_resolution(self):
        if not self.started:
            return
        x = self.ids.resolution_x.text
        y = self.ids.resolution_y.text
        
        if x == '' or y == '':
            self.ids.resolution_x.text = str(self.resolution[0])
            self.ids.resolution_y.text = str(self.resolution[1])
            set_simple_popup('Error', 'Resolution cannot be empty')
            return
        
        x = int(x)
        y = int(y)
        
        if x > self.max_resolution[0] or y > self.max_resolution[1]:
            self.ids.resolution_x.text = str(self.resolution[0])
            self.ids.resolution_y.text = str(self.resolution[1])
            set_simple_popup('Error', f'Max resolution is {self.max_resolution[0]}x{self.max_resolution[1]}')
            return
        
        
        self.resolution = (x, y)
        self.engine.set_background(self.resolution)
        self.video_player.set_size(self.resolution)