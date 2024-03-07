from kivy.uix.screenmanager import ScreenManager
from kivy.properties import ObjectProperty

from uix.content.template import TemplateScreen
from uix.content.sources.footer import SourcesFooter
from uix.content.sources.scroll import SourcesScroll
from uix.content.scenes.footer import ScenesFooter
from uix.content.scenes.scroll import ScenesScroll
from uix.content.config.config_content import ConfigContent

from engine_2d.engine import Engine

class ContentScreenManager(ScreenManager):
    
    engine: Engine = ObjectProperty(None)
    video_player = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.scenes_screen = TemplateScreen(name='Screens', title='Screen')
        self.scenes_footer = ScenesFooter(engine=self.engine)
        self.scenes_scroll = ScenesScroll(engine=self.engine, video_player=self.video_player)
        self.scenes_footer.change_callback = self.scenes_scroll.update
        self.scenes_screen.ids.screen_footer.add_widget(self.scenes_footer)
        self.scenes_screen.ids.screen_content.add_widget(self.scenes_scroll)

        self.layers_screen = TemplateScreen(name='Layers', title='Layers')
        self.layers_footer = SourcesFooter(engine=self.engine)
        self.layers_scroll = SourcesScroll(engine=self.engine, video_player=self.video_player)
        self.layers_footer.change_callback = self.layers_scroll.update
        self.layers_footer.new_source_callback = self.layers_scroll.sync_selected_from_source
        self.scenes_scroll.update_callback = self.layers_scroll.update
        self.layers_scroll.change_selected_callback = self.layers_footer.set_mode
        self.layers_screen.ids.screen_footer.add_widget(self.layers_footer)
        self.layers_screen.ids.screen_content.add_widget(self.layers_scroll)
        
        self.config_screen = TemplateScreen(name='Config', title='Config')
        self.config_content = ConfigContent(engine=self.engine,
                                            video_player=self.video_player)
        self.config_screen.ids.screen_content.add_widget(self.config_content)
        
        self.add_widget(self.layers_screen)
        self.add_widget(self.scenes_screen)
        self.add_widget(self.config_screen)
        
        self.current = 'Layers'