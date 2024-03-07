from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import ButtonBehavior


class ItemNavBar(ButtonBehavior, BoxLayout):
    text = StringProperty('')
    icon = StringProperty('')
    icon_selected = StringProperty('')
    is_selected = BooleanProperty(False)
    selected_change = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_release(self):
        self.is_selected = True
        self.selected_change(self)