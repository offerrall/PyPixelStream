from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.metrics import dp
from engine_2d.engine import Engine
from engine_2d.senders.wonderland3d4832 import WonderLand3d4832Device

from uix.simple_popup import set_simple_popup

class WonderLand3d4832(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def check_name(self, text: TextInput):
        if len(text.text) > 10:
            text.text = text.text[:10]

    def check_ip_piece(self, text: TextInput):
        try:
            ip_piece = int(text.text)
        except:
            text.text = '0'
            return
        if ip_piece > 255:
            text.text = '255'
    
    def check_port(self, text: TextInput):
        try:
            port = int(text.text)
        except:
            text.text = '0'
            return
        if port > 65535:
            text.text = '65535'

class EditWonderLand3d4832(BoxLayout):
    device: WonderLand3d4832Device = ObjectProperty(None)
    change_data_callback: callable = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        menu = self.ids.box_send_properties.children[0]
        menu.ids.sends_name.text = self.device.name
        ip = self.device.ip.split('.')
        menu.ids.ip_one.text = ip[0]
        menu.ids.ip_two.text = ip[1]
        menu.ids.ip_three.text = ip[2]
        menu.ids.ip_four.text = ip[3]
        menu.ids.port.text = str(self.device.port)
    
    def edit_send(self):
        atm_type = self.ids.box_send_properties.children[0].ids
        ip = f"{atm_type.ip_one.text}.{atm_type.ip_two.text}.{atm_type.ip_three.text}.{atm_type.ip_four.text}"
        port = atm_type.port.text
        name = atm_type.sends_name.text
        name = name.replace(' ', '')
        if name == '':
            set_simple_popup('Error', 'Please enter a name.')
            return
        self.device.name = name
        self.device.ip = ip
        self.device.port = int(port)
        self.parent.parent.parent.dismiss()
        self.change_data_callback()

class AddSendModal(BoxLayout):
    engine: Engine = ObjectProperty(None)
    add_send_callback: callable = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        types_modal = ['WonderLand3d4832']
        self.ids.send_type_spinner.values = types_modal
        self.atm_type = None

    def update_properties(self):
        atm_name = self.ids.send_type_spinner.text

        if atm_name == 'WonderLand3d4832':
            self.ids.box_send_properties.clear_widgets()
            type_device = WonderLand3d4832()
            self.ids.box_send_properties.add_widget(type_device)
            self.ids.box_send_properties.height = dp(90)
            self.atm_type = type_device
        
    def add_send(self):
        if self.atm_type is None:
            set_simple_popup('Error', 'Please select a type of send.')
            return
        
        if self.atm_type.__class__.__name__ == 'WonderLand3d4832':
            name = self.atm_type.ids.sends_name.text
            if name == '':
                set_simple_popup('Error', 'Please enter a name.')
                return
            atm_type = self.atm_type.ids
            ip = f"{atm_type.ip_one.text}.{atm_type.ip_two.text}.{atm_type.ip_three.text}.{atm_type.ip_four.text}"
            port = self.atm_type.ids.port.text

            device = WonderLand3d4832Device(name, ip=ip, port=int(port))
            self.add_send_callback(device)
            self.parent.parent.parent.dismiss()