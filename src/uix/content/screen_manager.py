from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty

from uix.content.template import TemplateScreen
from uix.content.sources.footer import SourcesFooter
from uix.content.sources.scroll import SourcesScroll
from uix.content.scenes.footer import ScenesFooter
from uix.content.scenes.scroll import ScenesScroll
from uix.content.send.footer import SendFooter
from uix.content.send.scroll import SendScroll
from uix.content.config.config_content import ConfigContent
from uix.video_player.interactive_resize_video import InteractiveResizeVideoRender

from engine_2d.engine import Engine

class ContentScreenManager(ScreenManager):
    """
    Screen manager for the content of the application, all the screens are added here
    """
    engine: Engine = ObjectProperty(None)
    video_player: InteractiveResizeVideoRender = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create the screens
        self.scenes_screen = TemplateScreen(name='Screens', title='Screens')
        self.scenes_footer = ScenesFooter(engine=self.engine)
        self.scenes_scroll = ScenesScroll(engine=self.engine, video_player=self.video_player)
        self.scenes_footer.change_callback = self.scenes_scroll.update
        self.scenes_screen.ids.screen_footer.add_widget(self.scenes_footer)
        self.scenes_screen.ids.screen_content.add_widget(self.scenes_scroll)

        # Create the layers screen
        self.layers_screen = TemplateScreen(name='Layers', title='Layers')
        self.layers_footer = SourcesFooter(engine=self.engine)
        self.layers_scroll = SourcesScroll(engine=self.engine, video_player=self.video_player)
        self.layers_footer.change_callback = self.layers_scroll.update
        self.layers_footer.new_source_callback = self.layers_scroll.sync_selected_from_source
        self.scenes_scroll.update_callback = self.layers_scroll.update
        self.layers_scroll.change_selected_callback = self.layers_footer.set_mode
        self.layers_screen.ids.screen_footer.add_widget(self.layers_footer)
        self.layers_screen.ids.screen_content.add_widget(self.layers_scroll)
        
        # Create the send screen
        self.send_screen = TemplateScreen(name='Send', title='Send Devices')
        self.send_scroll = SendScroll(engine=self.engine)
        self.send_footer = SendFooter(engine=self.engine, send_scroll=self.send_scroll)
        self.send_footer.change_callback = self.send_scroll.update
        self.video_player.deselect_send_callback = self.send_scroll.deselect_send
        self.send_scroll.deselect_send_callback = self.video_player.deselect_send
        self.send_scroll.change_selected_callback = self.send_footer.set_mode
        self.send_scroll.selected_send_callback = self.video_player.select_send
        self.send_screen.ids.screen_footer.add_widget(self.send_footer)
        self.send_screen.ids.screen_content.add_widget(self.send_scroll)

        # Create the config screen
        self.config_screen = TemplateScreen(name='Config', title='Config')
        self.config_content = ConfigContent(engine=self.engine,
                                            video_player=self.video_player)
        self.config_screen.ids.screen_content.add_widget(self.config_content)
        
        self.add_widget(self.layers_screen)
        self.add_widget(self.scenes_screen)
        self.add_widget(self.send_screen)
        self.add_widget(self.config_screen)
        
        self.current = 'Layers'