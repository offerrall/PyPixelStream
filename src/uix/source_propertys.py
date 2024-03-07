from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from kivy.metrics import dp

from uix.propertys import *
from uix.simple_popup import set_simple_popup

from engine_2d.engine import Engine
from engine_2d.source import Source
from engine_2d.text import get_fonts

from utils.cryptocurrency.cryptocurrency import get_only_name_list, get_fiat_list

def get_source_properties(source: Source):
    class_name = source.__class__.__name__

    dict_source_functions = {
        "SolidColor": set_solid_color_properties,
        "GameOfLife": set_game_of_life_properties,
        "Gradient": set_gradient_properties,
        "Image": set_image_properties,
        "GIF": set_gif_properties,
        "RandomChase": set_random_chase_properties,
        "ScreenCapture": set_screen_capture_properties,
        "Video": set_video_properties,
        "WebCam": set_webcam_properties,
        "Text": set_text_properties,
        "Clock": set_clock_properties,
        "Stopwatch": set_stopwatch_properties,
        "Timer": set_timer_text_properties,
        "Date": set_date_text_properties,
        "SystemMonitor": set_system_monitor_properties,
        "CryptoPrice": set_crypto_price_properties,
        "SnowFall": set_snow_fall_effect_properties,
        "Rainbow": set_rainbow_effect_properties,
        "ColorFrizzles": set_color_frizzles_effect_properties,
        "AudioVisualizer": set_audio_visualizer_properties,
        "RainbowTwister": set_rainbow_twister_properties
    }
    try:
        return dict_source_functions[class_name]
    except KeyError:
        return no_set_properties
    
class SourceProperties(BoxLayout):
    engine: Engine = ObjectProperty(None)
    source: Source = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.last_valid_name = self.source.name
        self.ids.layer_name_input.text = self.source.name
        self.size_height = get_source_properties(self.source)(self.source, self.ids.source_properties) + dp(30)
    
    def update_name(self):
        atm_scene = self.engine.atm_scene
        if atm_scene.check_name_exists(self.ids.layer_name_input.text, strip=False) or self.ids.layer_name_input.text == "":
            if self.ids.layer_name_input.text != self.source.name:
                if self.ids.layer_name_input.text == "":
                    set_simple_popup("Error", "Name is empty")
                else:
                    set_simple_popup("Error", f"Name {self.ids.layer_name_input.text} already exists")
            self.ids.layer_name_input.text = self.last_valid_name
            return
        
        self.last_valid_name = self.ids.layer_name_input.text
        self.source.name = self.ids.layer_name_input.text

def no_set_properties(source, properties_scrollview):
    return dp(0)

def set_rainbow_twister_properties(source, properties_scrollview):
    height = dp(30)

    box_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=height)
    box_layout.add_widget(PropertySlider(source=source,
                                        property_name="fps",
                                        property_label_text="FPS",
                                        property_min=1,
                                        property_max=60))
    properties_scrollview.add_widget(box_layout)

    return height

def set_audio_visualizer_properties(source, properties_scrollview):
    height = dp(120)

    box_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=height)
    box_layout.add_widget(PropertyColor(source=source,
                                        property_name="color",
                                        property_label_text="Color"))
    box_layout.add_widget(PropertySpinner(source=source,
                                        property_name="mode",
                                        property_label_text="Mode",
                                        values=["fft", "waveform"]))
    box_layout.add_widget(PropertyBoolean(source=source,
                                        property_name="transparent_background",
                                        property_label_text="Transparent Background"))
    box_layout.add_widget(PropertySlider(source=source,
                                        property_name="fps",
                                        property_label_text="FPS",
                                        property_min=1,
                                        property_max=60))
    properties_scrollview.add_widget(box_layout)

    return height

def set_gif_properties(source, properties_scrollview):
    height = dp(30)

    box_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=height)
    box_layout.add_widget(PropertyFilepath(source=source,
                                            property_name="path",
                                            property_label_text="GIF Path",
                                            title_filechooser="Select a GIF",
                                            filters_filechooser=['*.gif']))
    properties_scrollview.add_widget(box_layout)

    return height

def set_color_frizzles_effect_properties(source, properties_scrollview):
    height = dp(60)

    box_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=height)
    box_layout.add_widget(PropertySlider(source=source,
                                        property_name="fps",
                                        property_label_text="FPS",
                                        property_min=1,
                                        property_max=60))
    box_layout.add_widget(PropertyBoolean(source=source,
                                        property_name="transparent_background",
                                        property_label_text="Transparent Background"))
    properties_scrollview.add_widget(box_layout)

    return height

def set_webcam_properties(source, properties_scrollview):
    height = dp(0)
    return height

def set_rainbow_effect_properties(source, properties_scrollview):
    height = dp(30)

    box_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=height)
    box_layout.add_widget(PropertySlider(source=source,
                                        property_name="fps",
                                        property_label_text="FPS",
                                        property_min=1,
                                        property_max=60))
    properties_scrollview.add_widget(box_layout)
    return height

def set_snow_fall_effect_properties(source, properties_scrollview):
    height = dp(150)

    box_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=height)
    box_layout.add_widget(PropertyColor(source=source,
                                        property_name="snow_color",
                                        property_label_text="Snow Color"))
    box_layout.add_widget(PropertyColor(source=source,
                                        property_name="background_color",
                                        property_label_text="Background Color"))
    box_layout.add_widget(PropertyBoolean(source=source,
                                        property_name="transparent_background",
                                        property_label_text="Transparent Background"))
    box_layout.add_widget(PropertySlider(source=source,
                                        property_name="fps",
                                        property_label_text="FPS",
                                        property_min=1,
                                        property_max=60))
    box_layout.add_widget(PropertySlider(source=source,
                                        property_name="snowflake_chance",
                                        property_label_text="Snowflake Chance",
                                        property_min=1,
                                        property_max=99))
    properties_scrollview.add_widget(box_layout)

    return height

def set_screen_capture_properties(source, properties_scrollview):
    height = dp(30)

    monitor_list = source.get_indexs()
    box_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=height)
    box_layout.add_widget(PropertySlider(source=source,
                                            property_name="monitor",
                                            property_label_text="Monitor",
                                            property_min=0,
                                            property_max=len(monitor_list)-1))
    properties_scrollview.add_widget(box_layout)

    return height

def set_image_properties(source, properties_scrollview):
    height = dp(30)

    box_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=height)
    box_layout.add_widget(PropertyFilepath(source=source,
                                            property_name="image_path",
                                            property_label_text="Image Path",
                                            title_filechooser="Select an Image",
                                            filters_filechooser=['*.png', '*.jpg', '*.jpeg', '*.gif']))
    properties_scrollview.add_widget(box_layout)

    return height

def set_random_chase_properties(source, properties_scrollview):
    height = dp(60)

    box_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=height)
    box_layout.add_widget(PropertySlider(source=source,
                                            property_name="fps",
                                            property_label_text="FPS",
                                            property_min=1,
                                            property_max=60))
                                            
    box_layout.add_widget(PropertySpinner(source=source,
                                            property_name="orientation",
                                            property_label_text="Orientation",
                                            values=["horizontal", "vertical"]))
    properties_scrollview.add_widget(box_layout)

    return height

def set_solid_color_properties(source, properties_scrollview):
    height = dp(30)

    box_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=height)
    box_layout.add_widget(PropertyColor(source=source,
                                        property_name="color",
                                        property_label_text="Color"))
    properties_scrollview.add_widget(box_layout)

    return height

def set_game_of_life_properties(source, properties_scrollview):
    height = dp(120)

    box_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=height)
    box_layout.add_widget(PropertyColor(source=source,
                                        property_name="color",
                                        property_label_text="Color"))
    box_layout.add_widget(PropertyColor(source=source,
                                        property_name="background",
                                        property_label_text="Background"))
    box_layout.add_widget(PropertyBoolean(source=source,
                                          property_name="background_transparent",
                                          property_label_text="Transparent Background"))
    box_layout.add_widget(PropertySlider(source=source,
                                            property_name="fps",
                                            property_label_text="FPS",
                                            property_min=1,
                                            property_max=60))
    properties_scrollview.add_widget(box_layout)

    return height

def set_gradient_properties(source, properties_scrollview):
    height = dp(90)

    box_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=height)
    box_layout.add_widget(PropertyColor(source=source,
                                        property_name="start_color",
                                        property_label_text="Start Color"))
    box_layout.add_widget(PropertyColor(source=source,
                                        property_name="end_color",
                                        property_label_text="End Color"))
    box_layout.add_widget(PropertySpinner(source=source,
                                          property_name="gradient_type",
                                          property_label_text="Gradient Type",
                                          values=["linear", "radial", "centered_linear", "linear_vertical"]))
    
    properties_scrollview.add_widget(box_layout)

    return height

def set_video_properties(source, properties_scrollview):
    height = dp(60)

    box_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=height)
    box_layout.add_widget(PropertyFilepath(source=source,
                                           property_name="video_path",
                                           property_label_text="Video Path",
                                           title_filechooser="Select a Video",
                                           filters_filechooser=['*.mp4', '*.avi', '*.mkv', '*.gif']))
    box_layout.add_widget(PropertyBoolean(source=source,
                                          property_name="video_volume",
                                          property_label_text="Video Volume"))
    properties_scrollview.add_widget(box_layout)

    return height


def set_text_properties(source, properties_scrollview):
    height = dp(120)
    box_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=height)

    box_layout.add_widget(PropertySpinner(source=source,
                                          property_name="font",
                                          property_label_text="Font",
                                          values=get_fonts()))
    box_layout.add_widget(PropertyTextInput(source=source,
                                            property_name="text",
                                            property_label_text="Text"))
    box_layout.add_widget(PropertyColor(source=source,
                                        property_name="color",
                                        property_label_text="Text Color"))
    box_layout.add_widget(PropertyFilepath(source=source,
                                            property_name="text_from_file",
                                            property_label_text="Text from File",
                                            title_filechooser="Select a File",
                                            filters_filechooser=['*.txt']))
    properties_scrollview.add_widget(box_layout)

    return height


def set_crypto_price_properties(source, properties_scrollview):
    height = dp(180)

    box_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=height)

    box_layout.add_widget(PropertySpinner(source=source,
                                            property_name="font",
                                            property_label_text="Font",
                                            values=get_fonts()))
    box_layout.add_widget(PropertyColor(source=source,
                                            property_name="color",
                                            property_label_text="Text Color"))
    box_layout.add_widget(PropertySpinner(source=source,
                                            property_name="crypto_name",
                                            property_label_text="Cripto Name",
                                            values=get_only_name_list()))
    box_layout.add_widget(PropertySpinner(source=source,
                                            property_name="fiat",
                                            property_label_text="Fiat",
                                            values=get_fiat_list()))
    box_layout.add_widget(PropertyBoolean(source=source,
                                            property_name="show_symbol",
                                            property_label_text="Show Symbol"))
    box_layout.add_widget(PropertyBoolean(source=source,
                                            property_name="show_fiat",
                                            property_label_text="Show Fiat"))
    
    properties_scrollview.add_widget(box_layout)

    return height

def set_clock_properties(source, properties_scrollview):
    height = dp(150)
    box_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=height)

    box_layout.add_widget(PropertySpinner(source=source,
                                            property_name="font",
                                            property_label_text="Font",
                                            values=get_fonts()))
    box_layout.add_widget(PropertyColor(source=source,
                                            property_name="color",
                                            property_label_text="Text Color"))
    box_layout.add_widget(PropertyBoolean(source=source,
                                          property_name="hours",
                                            property_label_text="Hours"))
    box_layout.add_widget(PropertyBoolean(source=source,
                                            property_name="minutes",
                                                property_label_text="Minutes"))
    box_layout.add_widget(PropertyBoolean(source=source,
                                            property_name="seconds",
                                                property_label_text="Seconds"))
                                        
    properties_scrollview.add_widget(box_layout)

    return height

def set_stopwatch_properties(source, properties_scrollview):
    height = dp(210)

    box_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=height)

    box_layout.add_widget(PropertyBooleanButton(source=source,
                                            property_name="reset",
                                            property_label_text="Reset"))
    box_layout.add_widget(PropertyBoolean(source=source,
                                            property_name="pause",
                                            property_label_text="Pause"))
    box_layout.add_widget(PropertySpinner(source=source,
                                            property_name="font",
                                            property_label_text="Font",
                                            values=get_fonts()))
    box_layout.add_widget(PropertyColor(source=source,
                                            property_name="color",
                                            property_label_text="Text Color"))
    box_layout.add_widget(PropertyBoolean(source=source,
                                          property_name="hours",
                                            property_label_text="Hours"))
    box_layout.add_widget(PropertyBoolean(source=source,
                                            property_name="minutes",
                                                property_label_text="Minutes"))
    box_layout.add_widget(PropertyBoolean(source=source,
                                            property_name="seconds",
                                                property_label_text="Seconds"))                    
    properties_scrollview.add_widget(box_layout)

    return height

def set_timer_text_properties(source, properties_scrollview):
    height = dp(240)

    box_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=height)
    box_layout.add_widget(PropertyTimeSelector(source=source,
                                            property_name="duration",
                                            property_label_text="Duration"))
    box_layout.add_widget(PropertyBooleanButton(source=source,
                                            property_name="reset",
                                            property_label_text="Reset"))
    box_layout.add_widget(PropertyBoolean(source=source,
                                            property_name="pause",
                                            property_label_text="Pause"))
    box_layout.add_widget(PropertySpinner(source=source,
                                            property_name="font",
                                            property_label_text="Font",
                                            values=get_fonts()))
    box_layout.add_widget(PropertyColor(source=source,
                                            property_name="color",
                                            property_label_text="Text Color"))
    box_layout.add_widget(PropertyBoolean(source=source,
                                            property_name="hours",
                                            property_label_text="Hours"))
    box_layout.add_widget(PropertyBoolean(source=source,
                                            property_name="minutes",
                                            property_label_text="Minutes"))
    box_layout.add_widget(PropertyBoolean(source=source,
                                            property_name="seconds",
                                            property_label_text="Seconds"))
    
    properties_scrollview.add_widget(box_layout)

    return height

def set_date_text_properties(source, properties_scrollview):
    height = dp(180)
    box_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=height)

    box_layout.add_widget(PropertySpinner(source=source,
                                            property_name="font",
                                            property_label_text="Font",
                                            values=get_fonts()))
    box_layout.add_widget(PropertyColor(source=source,
                                            property_name="color",
                                            property_label_text="Text Color"))

    box_layout.add_widget(PropertyBoolean(source=source,
                                            property_name="european_format",
                                            property_label_text="European Format"))

    box_layout.add_widget(PropertyBoolean(source=source,
                                            property_name="day",
                                            property_label_text="Day"))
    box_layout.add_widget(PropertyBoolean(source=source,
                                            property_name="month",
                                            property_label_text="Month"))
    box_layout.add_widget(PropertyBoolean(source=source,
                                            property_name="year",
                                            property_label_text="Year"))
    
    properties_scrollview.add_widget(box_layout)

    return height

def set_system_monitor_properties(source, properties_scrollview):
    height = dp(210)
    box_layout = BoxLayout(orientation="vertical", size_hint_y=None, height=height)
    box_layout.add_widget(PropertySlider(source=source,
                                            property_name="fps",
                                            property_label_text="FPS",
                                            property_min=1,
                                            property_max=60))

    box_layout.add_widget(PropertySpinner(source=source,
                                            property_name="font",
                                            property_label_text="Font",
                                            values=get_fonts()))
    box_layout.add_widget(PropertyColor(source=source,
                                            property_name="color",
                                            property_label_text="Text Color"))
    
    box_layout.add_widget(PropertyBoolean(source=source,
                                            property_name="name_resourse",
                                            property_label_text="Name"))

    box_layout.add_widget(PropertyBoolean(source=source,
                                            property_name="cpu",
                                            property_label_text="CPU"))
    box_layout.add_widget(PropertyBoolean(source=source,
                                            property_name="ram",
                                            property_label_text="RAM"))
    box_layout.add_widget(PropertyBoolean(source=source,
                                          property_name="disk",
                                          property_label_text="Disk"))
    
    properties_scrollview.add_widget(box_layout)

    return height