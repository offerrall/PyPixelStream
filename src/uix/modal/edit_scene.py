from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty

from uix.simple_popup import set_simple_popup
from engine_2d.engine import Engine


class EditSceneModal(BoxLayout):
    """
    Modal for editing a scene
    """
    engine: Engine = ObjectProperty(None)
    placeholder_text = StringProperty("Screen name")
    name_callback: callable = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.scene_name.text = self.engine.atm_scene.name

    def edit_scene(self, name: str):
        name = name.strip()
        if name == "":
            set_simple_popup(title="Attention",
                           text="Screen name cannot be empty")
            return

        try:
            self.engine.check_scene_name(name)
        except ValueError:
            set_simple_popup(title="Attention",
                           text=f"'{name}' name already exists")
            return
        
        if self.name_callback:
            self.name_callback(name)
        
        self.parent.parent.parent.dismiss()