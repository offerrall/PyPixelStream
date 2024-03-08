from .grayscale import Grayscale
from .wrap_around import WrapAroundShift
from .circle import CircleMask
from .brightness_contrast import BrightnessContrast
from .chromakey import ChromaKey
from .mask import WhiteMask
from .flip import Flip


def get_filters_list():
    """
    To add a new filter, you have to import it in this file and add it,
    then in uix.filter_propertys you can define the properties of the filter to be able to modify it from the app.
    """
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