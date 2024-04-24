from kivy.uix.boxlayout import BoxLayout

from uix.video_player.interactive_resize_video import InteractiveResizeVideoRender
from uix.content.screen_manager import ContentScreenManager

from engine_2d.scene import Scene
from engine_2d.engine import Engine

class MainContainer(BoxLayout):
    """
    Main container for the application
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.version = "0.1"
        self.engine = Engine() # This is the main engine for the application
        
        if not self.engine.scenes:
            self.engine.add_scene(Scene("Screen"))
        
        # interactive_resize_video is the main video player
        self.interactive_resize_video = InteractiveResizeVideoRender(size=self.engine.size, 
                                                                     source_list=self.engine.atm_scene.sources)
        self.interactive_resize_video.sends_list = self.engine.sends_devices
        # content_screen_manager is the main screen manager
        self.content_screen_manager = ContentScreenManager(engine=self.engine,
                                                           video_player=self.interactive_resize_video)

        self.ids.video_player_container.add_widget(self.interactive_resize_video)
        self.ids.content.add_widget(self.content_screen_manager)
        # nav_bar is the main navigation bar, declared in the kv file
        self.ids.nav_bar.content_screen_manager = self.content_screen_manager