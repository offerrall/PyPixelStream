from kivy.graphics import Color, Line, InstructionGroup, Rectangle
from kivy.metrics import dp

from .interactive_video import InteractiveVideoRender
from engine_2d.source import Source


class InteractiveResizeVideoRender(InteractiveVideoRender):
    """
    This class is a widget that renders a video frame and allows the user to interact with the sources.
    """
    def __init__(self,
                 size: tuple[int, int],
                 source_list: list[Source],
                 selection_color: tuple[int, int, int] = (255, 0, 0),
                 **kwargs):
        super().__init__(size, source_list, selection_color, **kwargs)
        self.corner_size = dp(10)
        self._resize_mode = None

        self.corner_names = [
            "bottom_left",
            "bottom_right",
            "top_left",
            "top_right"
        ]

        self.corner_selection_boxes = {}

    def _create_selection_box(self, pos, size):
        selection_box = InstructionGroup()
        selection_box.add(Color(*self.selection_color))

        points = [
            [pos[0], pos[1], pos[0] + size[0], pos[1]],
            [pos[0], pos[1], pos[0], pos[1] + size[1]],
            [pos[0] + size[0], pos[1], pos[0] + size[0], pos[1] + size[1]],
            [pos[0], pos[1] + size[1], pos[0] + size[0], pos[1] + size[1]]
        ]
        for point in points:
            selection_box.add(Line(points=point, width=dp(2)))

        corners = [
            [pos[0], pos[1]],
            [pos[0] + size[0] - self.corner_size, pos[1]],
            [pos[0], pos[1] + size[1] - self.corner_size],
            [pos[0] + size[0] - self.corner_size, pos[1] + size[1] - self.corner_size]
        ]

        for i, corner in enumerate(corners):
            self.corner_selection_boxes[self.corner_names[i]] = Rectangle(pos=corner, size=(self.corner_size, self.corner_size))
            selection_box.add(self.corner_selection_boxes[self.corner_names[i]])

        return selection_box

    def on_touch_down(self, touch):
        if self.selected_source:
            for corner_name, corner_rect in self.corner_selection_boxes.items():
                if (corner_rect.pos[0] <= touch.x <= corner_rect.pos[0] + self.corner_size and
                    corner_rect.pos[1] <= touch.y <= corner_rect.pos[1] + self.corner_size):
                    self._resize_mode = corner_name
                    return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self._resize_mode is not None and self.selected_source:
            touch_x, touch_y = self._get_scaled_touch_position(touch)

            new_width = self.selected_source.width
            new_height = self.selected_source.height

            if "left" in self._resize_mode:
                delta_x = int(self.selected_source.x - touch_x)
                new_width += delta_x
                if new_width < 1:
                    delta_x += 1 - new_width
                    new_width = 1
                self.selected_source.x -= int(delta_x)

            if "right" in self._resize_mode:
                new_width = max(int(touch_x - self.selected_source.x), 1)

            if "top" in self._resize_mode:
                delta_y = int(self.selected_source.y - touch_y)
                new_height += delta_y
                if new_height < 1:
                    delta_y += 1 - new_height
                    new_height = 1
                self.selected_source.y -= int(delta_y)

            if "bottom" in self._resize_mode:
                new_height = max(int(touch_y - self.selected_source.y), 1)

            self.selected_source.set_height_and_width(new_height, new_width)
            self._refresh_selection_box()
            return True

        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        self._resize_mode = None
        return super().on_touch_up(touch)