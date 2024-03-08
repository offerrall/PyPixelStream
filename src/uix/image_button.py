from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.properties import ObjectProperty


class ImageButton(ButtonBehavior, Image):
    """
    Custom widget that combines an image and a button.
    """
    press_callback = ObjectProperty(None)

    def on_press(self):
        if self.press_callback:
            self.press_callback()