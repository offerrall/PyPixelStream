from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from engine_2d.source import Source
from engine_2d.engine import Engine
from uix.source_propertys import SourceProperties

class ModifySourceModal(BoxLayout):
    source: Source = ObjectProperty(None)
    engine: Engine = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        commun_properties = SourceProperties(engine=self.engine, source=self.source)
        self.ids.modify_source_modal_content.add_widget(commun_properties)
        self.ids.modify_source_modal_content.height = commun_properties.size_height