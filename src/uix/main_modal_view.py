from kivy.uix.modalview import ModalView
from kivy.properties import StringProperty, DictProperty, ListProperty, ObjectProperty

class MainModalView(ModalView):
    """
    This class is a base class for all modal views.
    """
    title = StringProperty("")
    custom_pos_hint = DictProperty({"center_x": 0.5, "y": 0})
    custom_size_hint = ListProperty([1, 0.5])
    widget_content = ObjectProperty(None)
    dimiss_function = ObjectProperty(None)
    icon = StringProperty("")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.widget_content:
            self.ids.main_modal_box.add_widget(self.widget_content)
    
    def on_dismiss(self):
        if self.dimiss_function:
            try:
                self.dimiss_function(self)
            except:
                self.dimiss_function()