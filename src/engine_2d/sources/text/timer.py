import time

from .text import Text

class Timer(Text):
    def __init__(self,
                 name: str,
                 order: int,
                 width: int,
                 height: int,
                 duration: int = 60,
                 pause: bool = False,
                 hours: bool = True,
                 minutes: bool = True,
                 seconds: bool = True,
                 font: str = "xsans",
                 color: tuple[int, int, int] = (255, 255, 255),
                 background_color: tuple[int, int, int] = None):
        super().__init__(name, order, width, height,
                         text="",
                         text_from_file=None,
                         font=font, color=color, background_color=background_color)
        self.end_time = time.time() + duration
        self.properties['duration'] = duration
        self.properties['hours'] = hours
        self.properties['minutes'] = minutes
        self.properties['seconds'] = seconds
        self.properties['reset'] = False
        self.properties['pause'] = pause
        self.time_in_pause = 0
        self.pause_at = 0
        self.update_timer_text()
    
    def update_timer_text(self):
        remaining_time = self.end_time - time.time()
        if remaining_time < 0:
            remaining_time = 0
        
        remaining_time += self.time_in_pause

        hours, remainder = divmod(int(remaining_time), 3600)
        minutes, seconds = divmod(remainder, 60)
        formated_time = ""
        if self.properties['hours']:
            formated_time += f"{hours:02d}:"
        if self.properties['minutes']:
            formated_time += f"{minutes:02d}:"
        if self.properties['seconds']:
            formated_time += f"{seconds:02d}"
        self.properties['text'] = formated_time

    def pause(self):
        self.pause_at = time.time()
    
    def resume(self):
        if self.pause_at:
            self.time_in_pause += time.time() - self.pause_at  
    
    def update(self) -> None:
        if self.properties["reset"]:
            self.end_time = time.time() + self.properties['duration']
            self.properties["reset"] = False
        
        if self.properties.cache:
            if 'duration' in self.properties.cache:
                self.end_time = time.time() + self.properties['duration']
            
            if 'pause' in self.properties.cache:
                if self.properties['pause']:
                    self.pause()
                else:
                    self.resume()
            
            self.properties.reset_cache()
        
        if not self.properties['pause']:
            self.update_timer_text()
        super().update()
