ignore_audio = False

try:
    from .media.audio import AudioVisualizer
except ImportError:
    ignore_audio = True
    print("Audio Visualizer is only available on Windows")
    print("If you are on Windows, make sure you have installed pyaudiowpatch")
    print("https://github.com/s0d3s/PyAudioWPatch/")

from .effect.solid import SolidColor
from .effect.color_frizzles import ColorFrizzles
from .effect.rainbow import Rainbow
from .effect.game_of_life import GameOfLife
from .effect.gradient import Gradient
from .effect.snow_fall import SnowFall
from .effect.random_chase import RandomChase
from .effect.rainbow_twister import RainbowTwister

from .media.image import Image
from .media.gif import GIF
from .media.screen_capture import ScreenCapture
from .media.video import Video
from .media.webcam import WebCam

from .text.text import Text
from .text.clock import Clock
from .text.stopwatch import Stopwatch
from .text.system_monitor import SystemMonitor
from .text.timer import Timer
from .text.date import Date
from .text.crypto_price import CryptoPrice

def get_source_type_list():
    media = get_media_source_type_list()
    text = get_text_source_type_list()
    effect = get_effect_source_type_list()
    return {**media, **text, **effect}

def get_media_source_type_list():
    dict_source_type = {
        "Image": Image,
        "GIF": GIF,
        "Video": Video,
        "WebCam": WebCam,
        "Screen Capture": ScreenCapture,
    }
    
    if not ignore_audio:
        dict_source_type["Audio Visualizer"] = AudioVisualizer
    
    return dict_source_type

def get_text_source_type_list():
    dict_source_type = {
        "Text": Text,
        "Clock": Clock,
        "Stopwatch": Stopwatch,
        "Timer": Timer,
        "Date": Date,
        "System Monitor": SystemMonitor,
        "Crypto Price": CryptoPrice
    }
    return dict_source_type

def get_effect_source_type_list():
    dict_source_type = {
        "Solid Color": SolidColor,
        "Gradient": Gradient,
        "Random Chase": RandomChase,
        "Game of Life": GameOfLife,
        "Snow Fall": SnowFall,
        "Rainbow": Rainbow,
        "Color Frizzles": ColorFrizzles,
        "Rainbow Twister": RainbowTwister
    }
    return dict_source_type