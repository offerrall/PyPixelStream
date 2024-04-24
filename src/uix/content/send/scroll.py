from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy.uix.behaviors import ButtonBehavior

from engine_2d.engine import Engine
from engine_2d.send import SendDevice

class SendItem(ButtonBehavior, BoxLayout):
    engine: Engine = ObjectProperty(None)
    send: SendDevice = ObjectProperty(None)
    is_selected: bool = BooleanProperty(False)
    is_visible: bool = BooleanProperty(True)
    press_callback: callable = ObjectProperty(None)

    def on_press(self):
        if self.press_callback:
            self.press_callback(self)

    def edit(self):
        if not self.is_selected and self.press_callback:
            self.press_callback(self)
            return
        
        print("Edit send")
    
    def view(self):
        self.send.is_active = not self.send.is_active
        self.is_visible = self.send.is_active

class SendScroll(BoxLayout):
    engine: Engine = ObjectProperty(None)
    change_selected_callback: callable = ObjectProperty(None)

    def select_send(self, send: SendDevice):
        for child in self.ids.send_scroll.children:
            if child.send == send:
                child.is_selected = True
            else:
                child.is_selected = False
    
    def get_atm_selected_send(self):
        atm_send = None
        
        for child in self.ids.send_scroll.children:
            if child.is_selected:
                atm_send = child.send
                break
        
        return atm_send
    
    def update(self):
        atm_selected_send = self.get_atm_selected_send()
        self.ids.send_scroll.clear_widgets()
        
        for send in self.engine.sends_devices:
            send_item = SendItem(engine=self.engine,
                                 send=send,
                                 press_callback=self.sync_selected)
            send_item.is_visible = send.is_active
            self.ids.send_scroll.add_widget(send_item)
        
        if atm_selected_send:
            self.select_send(atm_selected_send)
        
    def sync_selected(self, send_item: SendItem):
        check_already_selected = send_item.is_selected

        for child in self.ids.send_scroll.children:
            child.is_selected = False
        
        send_item.is_selected = not check_already_selected

        if self.change_selected_callback:
            self.change_selected_callback()