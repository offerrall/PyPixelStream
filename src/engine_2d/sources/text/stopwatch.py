import time

from .text import Text

class Stopwatch(Text):
    def __init__(self,
                 name: str,
                 order: int,
                 width: int,
                 height: int,
                 hours: bool = True,
                 minutes: bool = True,
                 seconds: bool = True,
                 reset: bool = False,
                 pause: bool = False,
                 font: str = "xsans",
                 color: tuple[int, int, int] = (255, 255, 255),
                 background_color: tuple[int, int, int] = None):
        super().__init__(name, order, width, height,
                         text="00:00:00",
                         text_from_file=None,
                         font=font, color=color, background_color=background_color)
        self.start_time = time.time()

        self.properties['hours'] = hours
        self.properties['minutes'] = minutes
        self.properties['seconds'] = seconds
        self.properties['reset'] = reset
        self.properties['pause'] = pause

    def get_elapsed_time(self) -> str:
        elapsed_time = int(time.time() - self.start_time)
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)

        return hours, minutes, seconds

    def get_elapsed_time_str(self) -> str:
        hours, minutes, seconds = self.get_elapsed_time()

        time_str = ""
        if self.properties['hours']:
            time_str += f"{hours:02d}:"
        if self.properties['minutes']:
            time_str += f"{minutes:02d}:"
        if self.properties['seconds']:
            time_str += f"{seconds:02d}"

        if time_str and time_str[-1] == ":":
            time_str = time_str[:-1]

        return time_str

    def update(self) -> None:

        check_update = True

        if self.properties['pause']:
            check_update = False
            elapsed_time = self.get_elapsed_time()
            self.start_time = time.time() - (elapsed_time[0] * 3600 + elapsed_time[1] * 60 + elapsed_time[2])

        if self.frame is None:
            check_update = True

        if self.properties['reset']:
            self.start_time = time.time()
            self.properties['reset'] = False
            check_update = True
        
        for prop in self.properties.cache:
            if prop in ['hours', 'minutes', 'seconds']:
                check_update = True
                self.properties.reset_cache()
                break
        
        if check_update:
            self.properties['text'] = self.get_elapsed_time_str()
        super().update()