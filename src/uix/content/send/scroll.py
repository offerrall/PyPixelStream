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

    def edit(self):
        print(f"Edit {self.send.name}")
    
    def view(self):
        print(f"View {self.send.name}")

class SendScroll(BoxLayout):
    engine: Engine = ObjectProperty(None)

    def update(self):
        print("Update send scroll")
        self.clear_widgets()
        
        for send in self.engine.sends_devices:
            print(f"Send {send.name}")
            send_item = SendItem(engine=self.engine, send=send)
            self.ids.send_scroll.add_widget(send_item)
        
