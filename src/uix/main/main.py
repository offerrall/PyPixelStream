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
        self.engine = Engine()
        
        if not self.engine.scenes:
            self.engine.add_scene(Scene("Screen"))
        
        self.interactive_resize_video = InteractiveResizeVideoRender(size=self.engine.size,
                                                                     source_list=self.engine.atm_scene.sources)
        self.content_screen_manager = ContentScreenManager(engine=self.engine,
                                                           video_player=self.interactive_resize_video)

        self.ids.video_player_container.add_widget(self.interactive_resize_video)
        self.ids.content.add_widget(self.content_screen_manager)
        self.ids.nav_bar.content_screen_manager = self.content_screen_manager