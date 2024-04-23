from kivy.config import Config
from kivy.utils import platform

if not platform in ('android', 'ios'):
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.core.window import Window
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

from uix.main.main import MainContainer
from config.load_kv import load_kv_files
from ws2812b.numpy_to_led import send_image_via_ws

class Main(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_container = MainContainer() # This is the main container for the application
        self.add_widget(self.main_container)
        self.atm_frame = 0

        Clock.schedule_once(self.update)
        Window.bind(on_request_close=self.on_request_close)

    def send_image(self, image):
        """
        This function sends an image to the led panel.
        """
        # send_image_via_ws(image, self.atm_frame)
        self.atm_frame += 1
        if self.atm_frame == 201:
            self.atm_frame = 0

    def update(self, dt):
        """
        This calls update on the engine and updates the video feed.
        """
        self.main_container.engine.update() 
        self.main_container.interactive_resize_video.set_frame(self.main_container.engine.background)
        self.send_image(self.main_container.engine.background)
        Clock.schedule_once(self.update)

    def on_request_close(self, *args):
        """
        This ensures that changes are saved before closing the application and disconnects sources.
        Prevents some threads from running in the background.
        """
        for scene in self.main_container.engine.scenes:
            scene.save(self.main_container.engine.path_scenes)
            for source in scene.sources:
                source.disconnect()

class MyApp(App):
    def build(self):
        return Main()

if __name__ == '__main__':
    load_kv_files()
    MyApp().run()