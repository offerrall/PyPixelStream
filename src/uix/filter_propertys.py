from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.metrics import dp

from uix.propertys import *
from uix.simple_popup import set_simple_popup
from engine_2d.filter import FiltersList, Filter


def get_filter_properties(filter: Filter) -> callable:
    """
    This function returns the function to set the properties of a filter.
    """
    class_name = filter.__class__.__name__

    dict_filter_functions = {
        "Grayscale": set_grayscale_properties,
        "BrightnessContrast": set_brightness_contrast_properties,
        "ChromaKey": set_chroma_key_properties,
        "CircleMask": set_circle_mask_properties,
        "WrapAroundShift": set_wrap_around_shift_properties,
        "WhiteMask": set_white_mask_properties,
        "Flip": set_flip_properties,
    }
    
    try:
        return dict_filter_functions[class_name]
    except KeyError:
        return no_set_properties

class FilterProperties(BoxLayout):
    filter_list: FiltersList = ObjectProperty(None)
    filter: Filter = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_height = dp(0)
        self.last_valid_name = self.filter.name
        self.ids.filter_name_input.text = self.filter.name
        self.size_height = get_filter_properties(self.filter)(self.filter, self.ids.filter_properties) + dp(30)

    def update_name(self):
        if self.filter_list.check_name_exists(self.ids.filter_name_input.text) or self.ids.filter_name_input.text == "":
            if self.ids.filter_name_input.text != self.filter.name:
                if self.ids.filter_name_input.text == "":
                    set_simple_popup("Error", "Name is empty")
                else:
                    set_simple_popup("Error", f"Name {self.ids.filter_name_input.text} already exists")
            self.ids.filter_name_input.text = self.last_valid_name
            return
        
        self.last_valid_name = self.ids.filter_name_input.text
        self.filter.name = self.ids.filter_name_input.text

def no_set_properties(filter: Filter, properties_scrollview: BoxLayout) -> float:
    return dp(0)

def set_flip_properties(filter: Filter, properties_scrollview: BoxLayout) -> float:
    height = dp(60)

    box_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=height)
    box_layout.add_widget(PropertyBoolean(source=filter,
                                            property_name="flip_x",
                                            property_label_text="Flip X"))
    box_layout.add_widget(PropertyBoolean(source=filter,
                                            property_name="flip_y",
                                            property_label_text="Flip Y"))
    properties_scrollview.add_widget(box_layout)

    return height

def set_white_mask_properties(filter: Filter, properties_scrollview: BoxLayout) -> float:
    height = dp(60)

    box_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=height)
    box_layout.add_widget(PropertyFilepath(source=filter,
                                            property_name="image_path",
                                            property_label_text="Image Path"))
    box_layout.add_widget(PropertyBoolean(source=filter,
                                            property_name="invert",
                                            property_label_text="Invert"))
    properties_scrollview.add_widget(box_layout)

    return height

def set_grayscale_properties(filter: Filter, properties_scrollview: BoxLayout) -> float:
    height = dp(0)
    return height

def set_wrap_around_shift_properties(filter: Filter, properties_scrollview: BoxLayout) -> float:
    height = dp(60)

    box_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=height)
    box_layout.add_widget(PropertySlider(source=filter,
                                            property_name="shift_x",
                                            property_label_text="X",
                                            property_min=-10,
                                            property_max=10,
                                            step=1))
    box_layout.add_widget(PropertySlider(source=filter,
                                            property_name="shift_y",
                                            property_label_text="Y",
                                            property_min=-10,
                                            property_max=10,
                                            step=1))
    properties_scrollview.add_widget(box_layout)

    return height

def set_circle_mask_properties(filter: Filter, properties_scrollview: BoxLayout) -> float:
    height = dp(60)
    
    box_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=height)
    box_layout.add_widget(PropertySlider(source=filter,
                                            property_name="radius",
                                            property_label_text="Radius",
                                            property_min=1,
                                            property_max=100))
    
    box_layout.add_widget(PropertyBoolean(source=filter,
                                            property_name="invert",
                                            property_label_text="Invert"))
    
    properties_scrollview.add_widget(box_layout)
    return height

def set_brightness_contrast_properties(filter: Filter, properties_scrollview: BoxLayout) -> float:
    height = dp(60)

    box_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=height)
    box_layout.add_widget(PropertySlider(source=filter,
                                            property_name="brightness",
                                            property_label_text="Brightness",
                                            property_min=-100,
                                            property_max=100,
                                            step=1))
    box_layout.add_widget(PropertySlider(source=filter,
                                            property_name="contrast",
                                            property_label_text="Contrast",
                                            property_min=0,
                                            property_max=100,
                                            step=1))
    properties_scrollview.add_widget(box_layout)

    return height

def set_chroma_key_properties(filter: Filter, properties_scrollview: BoxLayout) -> float:
    height = dp(30)
    
    box_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=height)
    box_layout.add_widget(PropertyColor(source=filter,
                                        property_name="target_color",
                                        property_label_text="Target Color"))

    properties_scrollview.add_widget(box_layout)
    
    return height