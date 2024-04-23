from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.properties import BooleanProperty

from engine_2d.engine import Engine
from engine_2d.send import SendDevice

from random import randint

class SendFooter(BoxLayout):
    """
    Footer of the sends list, with the buttons to add, remove, move up and move down
    """
    engine: Engine = ObjectProperty(None)
    change_callback: callable = ObjectProperty(None)
    mode_is_selected: bool = BooleanProperty(False)
    send_scroll: BoxLayout = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_mode()

    def set_mode(self):
        atm_selected_send = self.get_atm_selected_send()
        self.mode_is_selected = atm_selected_send is not None

    def get_atm_selected_send(self):
        atm_send = None
        scroll = self.send_scroll.ids.send_scroll
        
        for child in scroll.children:
            if child.is_selected:
                atm_send = child.send
                break

        return atm_send
    
    def add_send(self):
        rand_name = f"test{randint(0, 1000)}"
        test_send = SendDevice(rand_name, "192.168.1.102", 8888, order=1000, is_active=True)
        self.engine.sends_devices.append(test_send)
        self.engine.order_sends()
        self.change_callback()
        self.send_scroll.select_send(test_send)
        self.set_mode()
    
    def remove_send(self):
        if not self.mode_is_selected:
            return
        
        atm = self.get_atm_selected_send()
        self.engine.sends_devices.remove(atm)
        self.engine.order_sends()
        self.change_callback()
        self.set_mode()
    
    def move_send_up(self):
        if not self.mode_is_selected:
            return
        
        atm = self.get_atm_selected_send()
        atm.order -= 1.5
        self.engine.order_sends()
        self.change_callback()
    
    def move_send_down(self):
        if not self.mode_is_selected:
            return
        
        atm = self.get_atm_selected_send()
        atm.order += 1.5
        self.engine.order_sends()
        self.change_callback()
        
    
