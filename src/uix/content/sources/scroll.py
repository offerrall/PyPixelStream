from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior

from engine_2d.engine import Engine
from engine_2d.source import Source

from uix.video_player.interactive_resize_video import InteractiveResizeVideoRender
from uix.main_modal_view import MainModalView
from uix.modal.modify_source import ModifySourceModal
from uix.modal.filters import FiltersModal, FiltersFooter

class SourcesItem(ButtonBehavior, BoxLayout):
    engine: Engine = ObjectProperty(None)
    source: Source = ObjectProperty(None)
    update_callback: callable = ObjectProperty(None)
    press_callback = ObjectProperty(None)
    duplicate_callback = ObjectProperty(None)
    is_selected = BooleanProperty(False)
    is_visible = BooleanProperty(True)
    is_selectable = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_selectable = self.source.is_selectable
        self.is_visible = self.source.is_visible

    def on_press(self):
        if self.press_callback:
            self.press_callback(self)

    def edit(self):
        if not self.is_selected and self.press_callback:
            self.press_callback(self)
            return
        
        cont_source = ModifySourceModal(source=self.source,
                                        engine=self.engine)
        
        new_source_modal = MainModalView(title="Modify Layer",
                                        widget_content=cont_source,
                                        dimiss_function=self.update_callback)
        new_source_modal.open()
    
    def duplicate(self):
        if not self.is_selected and self.press_callback:
            self.press_callback(self)
            return
        
        if self.duplicate_callback:
            self.duplicate_callback(self)
    
    def view_filters(self):
        if not self.is_selected and self.press_callback:
            self.press_callback(self)
            return

        filters_footer = FiltersFooter(filters_list=self.source.filters)
        
        cont_filters = FiltersModal(filters_list=self.source.filters)
        cont_filters.ids.footer.add_widget(filters_footer)
        cont_filters.change_callback = filters_footer.update_mode
        filters_footer.change_callback = cont_filters.update_list     
        filters_modal = MainModalView(title="Filters",
                                          widget_content=cont_filters)
        
        filters_modal.open()
    
    def view(self):
        self.source.is_visible = not self.source.is_visible
        self.is_visible = self.source.is_visible

    def lock(self):
        self.source.is_selectable = not self.source.is_selectable
        self.is_selectable = self.source.is_selectable


class SourcesScroll(BoxLayout):
    engine: Engine = ObjectProperty(None)
    video_player: InteractiveResizeVideoRender = ObjectProperty(None)
    change_selected_callback: callable = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.video_player.selection_callback = self.sync_selected_from_video
        self.video_player.deselect_callback = self.sync_deselected_from_video
        self.update()
    
    def sync_selected_from_video(self, source: Source):
        for child in self.ids.sources_scroll.children:
            child.is_selected = False
            if child.source == source:
                child.is_selected = True
        
        if self.change_selected_callback:
            self.change_selected_callback()
    
    def sync_selected_from_source(self, source: Source):
        for child in self.ids.sources_scroll.children:
            child.is_selected = False
            if child.source == source:
                child.is_selected = True
                self.video_player.select_source(source, callback=False)
        
        if self.change_selected_callback:
            self.change_selected_callback()

    def sync_deselected_from_video(self):
        for child in self.ids.sources_scroll.children:
            child.is_selected = False
        
        if self.change_selected_callback:
            self.change_selected_callback()

    def sync_selected(self, source_item: SourcesItem):
        self.video_player.deselect_source(callback=False)
        check_already_selected = source_item.is_selected

        for child in self.ids.sources_scroll.children:
            child.is_selected = False
        
        source_item.is_selected = not check_already_selected
        if source_item.is_selected:
            self.video_player.select_source(source_item.source, callback=False)
        
        if self.change_selected_callback:
            self.change_selected_callback()

    def duplicate_source(self, source_item: SourcesItem):
        self.engine.atm_scene.duplicate_source(source_item.source)
        self.update()

    def update(self):
        self.ids.sources_scroll.clear_widgets()

        sources = self.engine.atm_scene.sources

        atm_source = self.video_player.selected_source
        check_atm_source = False
        if sources:
            for source in sources[::-1]:
                layer_item = SourcesItem(source=source,
                                         engine=self.engine,
                                         update_callback=self.update,
                                         press_callback=self.sync_selected,
                                         duplicate_callback=self.duplicate_source)
                layer_item.is_selected = source.is_selected
                if source == atm_source:
                    check_atm_source = True
                if source.is_selected:
                    self.video_player.select_source(source, callback=False)
                self.ids.sources_scroll.add_widget(layer_item)
        
        if not check_atm_source:
            self.video_player.deselect_source(callback=False)
        
        if self.change_selected_callback:
            self.change_selected_callback()