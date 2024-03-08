from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, BooleanProperty

from uix.main_modal_view import MainModalView
from uix.modal.add_source import AddSourceModal

from engine_2d.engine import Engine

class SourcesFooter(BoxLayout):
    """
    Footer of the sources list, with the buttons to add, remove, move up and move down the sources
    """
    engine: Engine = ObjectProperty(None)
    change_callback: callable = ObjectProperty(None)
    mode_is_selected: bool = BooleanProperty(False)
    new_source_callback: callable = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_mode()

    def set_mode(self):
        atm_selected_source = self.get_atm_selected_source()
        self.mode_is_selected = atm_selected_source is not None

    def get_atm_selected_source(self):
        atm_scene = self.engine.atm_scene
        if not atm_scene:
            return None
        
        selected_source = None
        for source in atm_scene.sources:
            if source.is_selected:
                selected_source = source
                break
        
        return selected_source

    def add_source_callback(self, source):
        while True:
            try:
                self.engine.atm_scene.add_source(source)
                break
            except ValueError as e:
                source.name = f"{source.name} copy"

        if self.change_callback:
            self.change_callback()
        if self.new_source_callback:
            self.new_source_callback(source)

    def add_source(self):
        cont_source = AddSourceModal(engine=self.engine,
                                    add_source_callback=self.add_source_callback)
        new_source_modal = MainModalView(title="Add New Layer",
                                        widget_content=cont_source)
        new_source_modal.open()
    
    def remove_source(self):
        source = self.get_atm_selected_source()
        if source:
            self.engine.atm_scene.remove_source(source)
            if self.change_callback:
                self.change_callback()
    
    def move_source_up(self):
        source = self.get_atm_selected_source()
        if source:
            source.order += 1.5
            self.engine.atm_scene.update_order()
            if self.change_callback:
                self.change_callback()
    
    def move_source_down(self):
        source = self.get_atm_selected_source()
        if source:
            source.order -= 1.5
            self.engine.atm_scene.update_order()
            if self.change_callback:
                self.change_callback()