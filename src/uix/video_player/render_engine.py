from kivy.uix.widget import Widget
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle
from kivy.graphics.instructions import InstructionGroup

from numpy import ndarray

class VideoRender(Widget):
    """
    This class is a widget that renders a video frame.
    Is the father of the class InteractiveVideoRender
    """
    def __init__(self, size: tuple[int, int], **kwargs):
        super(VideoRender, self).__init__(**kwargs)
        self.set_size(size)

    def set_size(self, size: tuple[int, int]) -> None:
        self.canvas.clear()
        
        self._size = size

        w, h = self._size
        self._tex_rgb = Texture.create(size=(w, h), colorfmt='rgb')
        self._tex_rgb.mag_filter = 'nearest'
        self._tex_rgb.uvsize = (1, -1)
        self._tex_rgb.uvpos = (0, 1)

        self._rectangle_group = InstructionGroup()
        self._rectangle_group.add(Rectangle(size=self.size, texture=self._tex_rgb))

        self.canvas.add(self._rectangle_group)
        self.bind(size=self._update_rectangle_size)
    
    def get_image_position_and_size(self):
        if self.width > 0 and self.height > 0:
            try:
                aspect_ratio = self._tex_rgb.size[0] / float(self._tex_rgb.size[1])
            except ZeroDivisionError:
                aspect_ratio = 1
            if self.width / self.height > aspect_ratio:
                rect_height = self.height
                rect_width = rect_height * aspect_ratio
                rect_x = (self.width - rect_width) / 2
                rect_y = 0
            else:
                rect_width = self.width
                rect_height = rect_width / aspect_ratio
                rect_x = 0
                rect_y = (self.height - rect_height) / 2
            rect_pos = (rect_x, rect_y)
            rect_size = (rect_width, rect_height)
        else:
            rect_pos = (0, 0)
            rect_size = (1, 1)

        return rect_pos, rect_size

    def _update_rectangle_size(self, instance, value):
        self._rectangle_group.clear()

        rect_pos, rect_size = self.get_image_position_and_size()
        self._rectangle_group.add(
            Rectangle(pos=rect_pos, size=rect_size, texture=self._tex_rgb))

    def set_frame(self, rgb_data: ndarray):
        self._tex_rgb.blit_buffer(
            rgb_data.tobytes(), colorfmt='rgb', bufferfmt='ubyte')

        self.canvas.remove(self._rectangle_group)
        self._rectangle_group.clear()
        self._update_rectangle_size(None, None)
        self.canvas.add(self._rectangle_group)