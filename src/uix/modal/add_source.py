from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import ButtonBehavior
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty

from uix.simple_popup import set_simple_popup
from uix.source_propertys import SourceProperties

from engine_2d.engine import Engine
from engine_2d.sources import (get_source_type_list,
                               get_media_source_type_list,
                               get_text_source_type_list,
                               get_effect_source_type_list)
from engine_2d.source import Source


class SourceTypeSelector(ButtonBehavior, BoxLayout):
    text = StringProperty("")
    is_selected = BooleanProperty(False)
    list_sources = ObjectProperty(None)
    press_callback = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def on_release(self, *args):
        if not self.is_selected:
            self.is_selected = True
            if self.press_callback:
                self.press_callback(self)

class AddSourceModal(BoxLayout):
    """
    Modal for adding a new source
    """
    engine: Engine = ObjectProperty(None)
    add_source_callback: callable = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = None
        self.set_buttons_source_type()

        for source_type_button in self.ids.buttons_type_selector.children:
            if source_type_button.is_selected:
                self.manage_buttons_source_type(source_type_button)
                break
    
    def manage_buttons_source_type(self, source_type_button: SourceTypeSelector):
        self.ids.box_source_properties.clear_widgets()
        for button in self.ids.buttons_type_selector.children:
            if button != source_type_button:
                button.is_selected = False
        
        self.ids.source_type_spinner.text = "Select Layer Type"
        self.ids.source_type_spinner.values = list(source_type_button.list_sources.keys())

    def set_buttons_source_type(self):
        self.ids.buttons_type_selector.clear_widgets()
        self.source = None
        media_button = SourceTypeSelector(text="Media",
                                          list_sources=get_media_source_type_list(),
                                          press_callback=self.manage_buttons_source_type)
        media_button.is_selected = True
        text_button = SourceTypeSelector(text="Text",
                                         list_sources=get_text_source_type_list(),
                                         press_callback=self.manage_buttons_source_type)
        effect_button = SourceTypeSelector(text="Effect",
                                           list_sources=get_effect_source_type_list(),
                                           press_callback=self.manage_buttons_source_type)
        self.ids.buttons_type_selector.add_widget(media_button)
        self.ids.buttons_type_selector.add_widget(text_button)
        self.ids.buttons_type_selector.add_widget(effect_button)

    def get_source_type(self):
        source: Source = get_source_type_list()[self.ids.source_type_spinner.text]
        return source

    def get_new_name(self):
        new_name = self.ids.source_type_spinner.text
        while True:
            if self.engine.atm_scene.check_name_exists(new_name):
                new_name += " copy"
            else:
                break
        return new_name
    
    def get_default_size(self):
        engine_background_size = self.engine.background.shape
        x = engine_background_size[1]
        y = engine_background_size[0]
        return x, y

    def update_properties(self):
        try:
            self.ids.box_source_properties.clear_widgets()
            self.source = None

            default_size = self.get_default_size()
            source = self.get_source_type()(name=self.get_new_name(),
                                            order=1_000_000,
                                            width=default_size[0],
                                            height=default_size[1])
            common_properties = SourceProperties(engine=self.engine, source=source)
            self.ids.box_source_properties.add_widget(common_properties)
            self.ids.box_source_properties.height = common_properties.size_height
            self.source = source
        except Exception as e:
            pass
    
    def add_source(self):

        if self.ids.source_type_spinner.text == "Select Layer Type":
            set_simple_popup("Attention", "Select Layer type")
            return
        
        if self.add_source_callback:
            self.add_source_callback(self.source)

        self.parent.parent.parent.dismiss()
