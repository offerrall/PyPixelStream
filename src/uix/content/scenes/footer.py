from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from engine_2d.engine import Engine
from engine_2d.scene import Scene

from uix.main_modal_view import MainModalView
from uix.modal.add_scene import AddSceneModal
from uix.simple_popup import set_simple_popup

class ScenesFooter(BoxLayout):
    
    engine: Engine = ObjectProperty(None)
    change_callback: callable = ObjectProperty(None)

    def add_scene_post(self, name: str):
        new_scene = Scene(name, order=len(self.engine.scenes) + 1)
        self.engine.add_scene(new_scene)
        self.engine.set_scene(new_scene)
        if self.change_callback:
            self.change_callback()

    def add_scene(self):
        content = AddSceneModal(engine=self.engine, name_callback=self.add_scene_post)
        new_scene_modal = MainModalView(title="Add Screen",
                                        widget_content=content)
        
        new_scene_modal.open()
    
    def remove_scene(self):
        if len(self.engine.scenes) == 1:
            set_simple_popup("Alert", "You can't remove the last scene")
            return
        scene = self.engine.atm_scene
        if scene:
            new_selected_scene_index = scene.order - 1
            if new_selected_scene_index < 0:
                new_selected_scene_index = 0

            self.engine.remove_scene(scene)
            self.engine.set_scene(self.engine.scenes[new_selected_scene_index])
            if self.change_callback:
                self.change_callback()
    
    def move_scene_up(self):
        scene = self.engine.atm_scene
        if scene:
            scene.order -= 1.5
            self.engine.order()
            if self.change_callback:
                self.change_callback()
    
    def move_scene_down(self):
        scene = self.engine.atm_scene
        if scene:
            scene.order += 1.5
            self.engine.order()
            if self.change_callback:
                self.change_callback()

