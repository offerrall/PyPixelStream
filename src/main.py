from kivy.config import Config
from kivy.utils import platform
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.label import Label

from uix.main.main import MainContainer
from config.load_kv import load_kv_files

if platform not in ('android', 'ios'):
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

class Main(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_container = MainContainer()  # This is the main container for the application
        self.add_widget(self.main_container)

        # FPS Label
        self.fps_label = Label(size_hint=(None, None), size=(100, 50), pos_hint={'x': 0.9, 'top': 1})
        self.add_widget(self.fps_label)

        # Schedule update methods
        Clock.schedule_once(self.update)
        Clock.schedule_interval(self.update_fps, 1.0)  # Update FPS every second
        Window.bind(on_request_close=self.on_request_close)

    def update(self, dt):
        """
        This calls update on the engine and updates the video feed.
        """
        self.main_container.engine.update()
        self.main_container.interactive_resize_video.set_frame(self.main_container.engine.background)
        Clock.schedule_once(self.update)

    def update_fps(self, dt):
        """
        Update the FPS label once every second.
        """
        fps = Clock.get_fps()  # Get the current FPS
        self.fps_label.text = f"FPS: {fps:.0f}"

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
