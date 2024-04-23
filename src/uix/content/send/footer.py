from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty

from engine_2d.engine import Engine
from engine_2d.send import SendDevice

class SendFooter(BoxLayout):
    """
    Footer of the sends list, with the buttons to add, remove, move up and move down
    """
    engine: Engine = ObjectProperty(None)
    change_callback: callable = ObjectProperty(None)
    mode_is_selected: bool = BooleanProperty(False)

    def add_send(self):
        print("Add send")
        test_send = SendDevice("test", "192.168.1.102", 8888)
        self.engine.sends_devices.append(test_send)
        self.change_callback()
    
    def remove_send(self):
        if not self.mode_is_selected:
            return
    
    def move_send_up(self):
        if not self.mode_is_selected:
            return
    
    def move_send_down(self):
        if not self.mode_is_selected:
            return
    
