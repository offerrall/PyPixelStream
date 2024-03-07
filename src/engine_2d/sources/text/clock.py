from datetime import datetime

from .text import Text


class Clock(Text):
    def __init__(self,
                 name: str,
                 order: int,
                 width: int,
                 height: int,
                 hours: bool = True,
                 minutes: bool = True,
                 seconds: bool = True,
                 font: str = "xsans",
                 color: tuple[int, int, int] = (255, 255, 255),
                 background_color: tuple[int, int, int] = None):
        super().__init__(name, order, width, height,
                         text="00:00:00",
                         text_from_file=None,
                         font=font, color=color, background_color=background_color)
        self.properties['hours'] = hours
        self.properties['minutes'] = minutes
        self.properties['seconds'] = seconds

    def get_current_time(self) -> str:
        format_time = ""
        if self.properties['hours']:
            format_time += "%H:"
        if self.properties['minutes']:
            format_time += "%M:"
        if self.properties['seconds']:
            format_time += "%S"
        if format_time == "":
            return ""
        if format_time[-1] == ":":
            format_time = format_time[:-1]
        return datetime.now().strftime(format_time)

    def update(self) -> None:
        self.properties['text'] = self.get_current_time()
        super().update()