from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior

from engine_2d.engine import Engine

from uix.main_modal_view import MainModalView
from uix.modal.edit_scene import EditSceneModal
from uix.modal.filters import FiltersModal, FiltersFooter

class SceneItem(ButtonBehavior, BoxLayout):
    name = StringProperty("")
    press_callback = ObjectProperty(None)
    duplicate_callback = ObjectProperty(None)
    edit_callback = ObjectProperty(None)
    is_selected = BooleanProperty(False)
    view_filters_callback = ObjectProperty(None)

    def on_press(self):
        if not self.is_selected:
            self.select()

        if self.press_callback:
            self.press_callback(self)
    
    def view_filters(self):
        if self.is_selected:
            if self.view_filters_callback:
                self.view_filters_callback(self)
            return
        if self.press_callback:
            self.press_callback(self)
    
    def duplicate(self):
        if self.is_selected:
            if self.duplicate_callback:
                self.duplicate_callback(self)
            return
        if self.press_callback:
            self.press_callback(self)

    def edit(self):
        if self.is_selected:
            if self.edit_callback:
                self.edit_callback(self)
            return
        if self.press_callback:
            self.press_callback(self)
            
    def deselect(self):
        self.is_selected = False

    def select(self):
        self.is_selected = True

class ScenesScroll(BoxLayout):
    engine: Engine = ObjectProperty(None)
    video_player = ObjectProperty(None)
    update_callback: callable = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scene_items = []
        self.update()

    def duplicate_scene(self, scene_item: SceneItem):
        self.engine.duplicate_scene(self.engine.get_scene(scene_item.name))
        self.update()

    def manage_selection(self, scene_item: SceneItem):
        for item in self.scene_items:
            if item != scene_item:
                item.deselect()
            else:
                item.select()
                if self.engine.atm_scene != self.engine.get_scene(scene_item.name):
                    self.engine.set_scene(self.engine.get_scene(scene_item.name))
                    self.video_player.change_source_list(self.engine.atm_scene.sources)
                    if self.update_callback:
                        self.update_callback()

    def edit_scene_post(self, name: str):
        self.engine.atm_scene.name = name
        self.update()

    def edit_scene(self, scene_item: SceneItem):
        content = EditSceneModal(engine=self.engine,
                                 placeholder_text=scene_item.name,
                                 name_callback=self.edit_scene_post)
        new_scene_modal = MainModalView(title="Edit Screen",
                                        widget_content=content)
        
        new_scene_modal.open()

    def view_filters(self, scene_item: SceneItem):
        scene = self.engine.get_scene(scene_item.name)
        filters_footer = FiltersFooter(filters_list=scene.filters)
        cont_filters = FiltersModal(filters_list=scene.filters)
        cont_filters.ids.footer.add_widget(filters_footer)
        cont_filters.change_callback = filters_footer.update_mode
        filters_footer.change_callback = cont_filters.update_list
        filters_modal = MainModalView(title="Filters",
                                          widget_content=cont_filters)
        filters_modal.open()
    
    def update(self):
        self.ids.scenes_scroll.clear_widgets()
        self.scene_items = []
        for scene in self.engine.scenes:
            is_selected = self.engine.atm_scene == scene
            scene_item = SceneItem(name=scene.name,
                                   is_selected=is_selected,
                                   view_filters_callback=self.view_filters,
                                   press_callback=self.manage_selection,
                                   edit_callback=self.edit_scene,
                                   duplicate_callback=self.duplicate_scene)
            if is_selected:
                self.video_player.change_source_list(scene.sources)
                if self.update_callback:
                    self.update_callback()
            self.scene_items.append(scene_item)
            self.ids.scenes_scroll.add_widget(scene_item)