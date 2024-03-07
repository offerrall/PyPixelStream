from .grayscale import Grayscale
from .wrap_around import WrapAroundShift
from .circle import CircleMask
from .brightness_contrast import BrightnessContrast
from .chromakey import ChromaKey
from .mask import WhiteMask
from .flip import Flip


def get_filters_list():
    dict_of_filters = {
        "Grayscale": Grayscale,
        "Brightness Contrast": BrightnessContrast,
        "Chroma Key": ChromaKey,
        "Circle Mask": CircleMask,
        "Wrap Around": WrapAroundShift,
        "White Mask": WhiteMask,
        "Flip": Flip
    }
    return dict_of_filters