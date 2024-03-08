from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

class NavBar(BoxLayout):
    """
    Main navigation bar for the application
    """
    content_screen_manager = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def change_screen(self, item_nav_bar):
        for child in self.children:
            if child != item_nav_bar:
                child.is_selected = False
        
        if self.content_screen_manager:
            self.content_screen_manager.current = item_nav_bar.text