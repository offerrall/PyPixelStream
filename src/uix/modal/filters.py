from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ObjectProperty

from uix.simple_popup import set_simple_popup
from uix.main_modal_view import MainModalView
from uix.filter_propertys import FilterProperties

from engine_2d.serialize.serialize import filter_to_dict, dict_to_filter
from engine_2d.filter import FiltersList, Filter
from engine_2d.filters import get_filters_list

class ModifyFilterModal(BoxLayout):
    filters_list: FiltersList = ObjectProperty(None)
    filter: Filter = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        commun_properties = FilterProperties(filter_list=self.filters_list,
                                             filter=self.filter)
        self.ids.modify_filter_modal_content.add_widget(commun_properties)
        self.ids.modify_filter_modal_content.height = commun_properties.size_height
        
class AddFilterModal(BoxLayout):
    """
    Modal for adding a new filter
    """
    add_filter_callback: callable = ObjectProperty(None)
    filters_list: FiltersList = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.filter_type_spinner.values = list(get_filters_list().keys())
        self.filter = None
    
    def get_filter_type(self):
        filter: Filter = get_filters_list()[self.ids.filter_type_spinner.text]
        return filter
    
    def get_new_name(self):
        new_name = self.ids.filter_type_spinner.text
        while True:
            if self.filters_list.check_name_exists(new_name):
                new_name += " copy"
            else:
                break
        return new_name
    
    def update_properties(self):
        self.ids.box_filter_properties.clear_widgets()
        self.filter = None
        filter = self.get_filter_type()(name=self.get_new_name(),
                                        order=1_000_000)
        common_properties = FilterProperties(filter_list=self.filters_list, filter=filter)
        self.ids.box_filter_properties.add_widget(common_properties)
        self.ids.box_filter_properties.height = common_properties.size_height
        self.filter = filter
    
    def add_filter(self):
        
        if self.ids.filter_type_spinner.text == "Select Filter Type":
            set_simple_popup("Attention", "Select Filter type")
            return
        
        if self.filters_list.check_name_exists(self.filter.name):
            set_simple_popup("Error", f"Name {self.filter.name} already exists")
            return
        
        if self.add_filter_callback:
            self.add_filter_callback(self.filter)
        
        self.parent.parent.parent.dismiss()
    

class FilterItem(ButtonBehavior, BoxLayout):
    filter: Filter = ObjectProperty(None)
    filters_list: FiltersList = ObjectProperty(None)
    is_selected: bool = ObjectProperty(False)
    is_visible: bool = ObjectProperty(True)
    duplicate_callback: callable = ObjectProperty(None)
    edit_callback: callable = ObjectProperty(None)
    press_callback: callable = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_visible = self.filter.is_visible

    def on_press(self):
        if self.press_callback:
            self.press_callback(self)

    def view(self):
        self.filter.is_visible = not self.filter.is_visible
        self.is_visible = self.filter.is_visible
    
    def duplicate(self):
        if not self.is_selected and self.press_callback:
            self.press_callback(self)
            return

        if self.duplicate_callback:
            self.duplicate_callback(self)
    
    def edit_finish(self):
        if self.edit_callback:
            self.edit_callback()
    
    def edit(self):
        if not self.is_selected and self.press_callback:
            self.press_callback(self)
            return
    
        cont_filter = ModifyFilterModal(filter=self.filter,
                                        filters_list=self.filters_list)
        
        new_filter_modal = MainModalView(title="Modify Filter",
                                        widget_content=cont_filter,
                                        dimiss_function=self.edit_finish)
        new_filter_modal.open()
        

class FiltersModal(BoxLayout):
    filters_list: FiltersList = ObjectProperty(None)
    change_callback: callable = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.update_list()
    
    def duplicate_filter(self, filter_item: FilterItem):
        new_name = f"{filter_item.filter.name} copy"
        
        while self.filters_list.check_name_exists(new_name):
            new_name = f"{new_name} copy"
        
        copy_filter = dict_to_filter(filter_to_dict(filter_item.filter))
        copy_filter.name = new_name
        copy_filter.order = filter_item.filter.order + 1.5
        self.filters_list.add(copy_filter)
        self.update_list()
    
    def sync_selected(self, filter_item: FilterItem):
        for child in self.ids.filters_scroll.children:
            if child is filter_item:
                continue
            child.is_selected = False
        filter_item.is_selected = not filter_item.is_selected
        if self.change_callback:
            self.change_callback(self)
    
    def update_list(self):
        atm_selected_filter = None
        for child in self.ids.filters_scroll.children:
            if child.is_selected:
                atm_selected_filter = child.filter
                break
        
        self.ids.filters_scroll.clear_widgets()
        for f in self.filters_list.filters[::-1]:
            filter_item = FilterItem(filter=f,
                                     filters_list=self.filters_list,
                                     press_callback=self.sync_selected,
                                     edit_callback=self.update_list,
                                     duplicate_callback=self.duplicate_filter)
            if f == atm_selected_filter:
                filter_item.is_selected = True
            self.ids.filters_scroll.add_widget(filter_item)
        
        if self.change_callback:
            self.change_callback(self)
            

class FiltersFooter(BoxLayout):
    filters_list: FiltersList = ObjectProperty(None)
    atm_filter: FilterItem = ObjectProperty(None)
    mode_is_selected: bool = ObjectProperty(False)
    change_callback: callable = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def update_mode(self, filter_modal: FiltersModal):
        mode = False
        for child in filter_modal.ids.filters_scroll.children:
            if child.is_selected:
                self.atm_filter = child.filter
                mode = True
                break
        self.mode_is_selected = mode
    
    def add_filter_callback(self, filter):
        self.filters_list.add(filter)
        if self.change_callback:
            self.change_callback()
    
    def add_filter(self):
        cont_filter = AddFilterModal(add_filter_callback=self.add_filter_callback,
                                    filters_list=self.filters_list)
        new_filter_modal = MainModalView(title="Add New Filter",
                                        widget_content=cont_filter)
        new_filter_modal.open()
    
    def remove_filter(self):
        if not self.mode_is_selected:
            return
        
        self.filters_list.remove(self.atm_filter.name)
        
        if self.change_callback:
            self.change_callback()
    
    def move_filter_up(self):
        if not self.mode_is_selected:
            return
        
        self.atm_filter.order += 1.5
        self.filters_list.sort()
        
        if self.change_callback:
            self.change_callback()
    
    def move_filter_down(self):
        if not self.mode_is_selected:
            return
        
        self.atm_filter.order -= 1.5
        self.filters_list.sort()
        
        if self.change_callback:
            self.change_callback()
        