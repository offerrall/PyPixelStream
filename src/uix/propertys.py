from kivy.uix.boxlayout import BoxLayout
from kivy.uix.colorpicker import ColorPicker
from kivy.properties import ObjectProperty

from uix.main_modal_view import MainModalView
from uix.utils import rgb_to_kivy_color, kivy_color_to_rgb

from plyer import filechooser

from engine_2d.source import Source


class BoxProperty(BoxLayout):
    source: Source = ObjectProperty(None)
    property_name = ObjectProperty(None)
    property_label_text = ObjectProperty(None)

class PropertySlider(BoxProperty):
    property_min = ObjectProperty(None)
    property_max = ObjectProperty(None)
    step = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.step is None:
            self.ids.slider.step = 1
        self.ids.slider.value = self.source.properties[self.property_name]
        self.update_property()
    
    def update_property(self):
        self.source.properties[self.property_name] = int(self.ids.slider.value)
        formated_name = self.property_name.capitalize().replace("_", " ")
        self.property_label_text = f"{formated_name} {self.source.properties[self.property_name]}"

class PropertyTimeSelector(BoxProperty):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        time = self.source.properties[self.property_name]
        hours = time // 3600
        minutes = (time % 3600) // 60
        seconds = time % 60

        self.ids.hour_spinner.text = str(hours)
        self.ids.minute_spinner.text = str(minutes)
        self.ids.second_spinner.text = str(seconds)
    
    def update_property(self):
        hours = int(self.ids.hour_spinner.text)
        minutes = int(self.ids.minute_spinner.text)
        seconds = int(self.ids.second_spinner.text)

        self.source.properties[self.property_name] = hours * 3600 + minutes * 60 + seconds

class PropertySpinner(BoxProperty):
    values = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.spinner.values = self.values
        self.ids.spinner.text = self.source.properties[self.property_name]
    
    def update_property(self):
        self.source.properties[self.property_name] = self.ids.spinner.text

class PropertyTextInput(BoxProperty):
    property_value = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.text_input.text = self.source.properties[self.property_name]
    
    def update_property(self):
        self.source.properties[self.property_name] = self.ids.text_input.text

class PropertyBoolean(BoxProperty):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.switch.active = self.source.properties[self.property_name]
    
    def update_property(self):
        self.source.properties[self.property_name] = self.ids.switch.active

class PropertyBooleanButton(BoxProperty):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def update_property(self):
        self.source.properties[self.property_name] = True

class PropertyFilepath(BoxProperty):
    title_filechooser = ObjectProperty(None)
    filters_filechooser = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.source.properties[self.property_name] is None or self.source.properties[self.property_name] == "":
            self.ids.filepath_label.text = f"No file selected"
        else:
            path = self.source.properties[self.property_name]
            path_formatted = path if len(path) < 10 else f"...{path[-10:]}"
            self.ids.filepath_label.text = f"Path: {path_formatted}"

    def open_filechooser(self):
        filters = [(f, f) for f in self.filters_filechooser] if self.filters_filechooser else []
        path = filechooser.open_file(title=self.title_filechooser, filters=filters)
        
        if not path:
            return
        
        path = path[0]
        self.source.properties[self.property_name] = path
        path_formatted = path if len(path) < 10 else f"...{path[-10:]}"
        self.ids.filepath_label.text = f"Path: {path_formatted}"

class PropertyColor(BoxProperty):
    color_kivy = ObjectProperty((1, 1, 1, 1))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color_kivy = rgb_to_kivy_color(self.source.properties[self.property_name])
    
    def update_color(self, instance, value):
        rgb = kivy_color_to_rgb(value)
        self.source.properties[self.property_name] = rgb
        self.color_kivy = rgb_to_kivy_color(rgb)

    def open_color_picker(self):
        atm_color = self.source.properties[self.property_name]
        color_picker = ColorPicker(color=rgb_to_kivy_color(atm_color))
        color_picker.bind(color=self.update_color)
        title = f"{self.source.name} - {self.property_label_text}"
        modal = MainModalView(title=title,
                              widget_content=color_picker)
        modal.open()