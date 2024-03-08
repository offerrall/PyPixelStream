from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.metrics import dp

from config.colors import colors


def set_simple_popup(title: str,
                     text: str,
                     text_align: str = 'center',
                     size_hint: tuple = (None, None),
                     size: tuple = (dp(300), dp(100)),
                     color_separator: tuple = colors['selected']
                     ):
    """
    Set a simple popup with a title and a message
    """
    pop = Popup(title=title,
                title_align=text_align,
                content=Label(text=text),
                size_hint=size_hint, size=size,
                separator_color=color_separator)
    pop.open()