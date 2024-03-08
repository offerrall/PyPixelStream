from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty



class TemplateScreen(Screen):
    """Is a base class for each item in the navigation bar, more info in the .kv file"""
    title = StringProperty('')