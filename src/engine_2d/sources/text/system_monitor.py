import time
import psutil

from .text import Text

class SystemMonitor(Text):
    def __init__(self,
                 name: str,
                 order: int,
                 width: int,
                 height: int,
                 font: str = "xsans",
                 fps: int = 10,
                 name_resourse: bool = True,
                 cpu: bool = True,
                 ram: bool = False,
                 disk: bool = False,
                 color: tuple[int, int, int] = (255, 255, 255),
                 background_color: tuple[int, int, int] = None):
        
        super().__init__(name, order, width, height,
                         text="",
                         text_from_file=None,
                         font=font, color=color, background_color=background_color)
        self.properties['fps'] = fps
        self.properties['cpu'] = cpu
        self.properties['ram'] = ram
        self.properties['disk'] = disk
        self.properties['name_resourse'] = name_resourse
        self.last_update = time.time()
        self.update_system_monitor_text()

    def _get_cpu_usage(self) -> float:
        return psutil.cpu_percent()
    
    def _get_ram_usage(self) -> float:
        return psutil.virtual_memory().percent
    
    def _get_disk_usage(self) -> float:
        return psutil.disk_usage('/').percent

    def update_system_monitor_text(self):
        text = ""
        if self.properties['cpu']:
            if self.properties['name_resourse']:
                text += "CPU: "
            text += f"{self._get_cpu_usage():.1f}%\n\n"
        if self.properties['ram']:
            if self.properties['name_resourse']:
                text += "RAM: "
            text += f"{self._get_ram_usage():.1f}%\n\n"
        if self.properties['disk']:
            if self.properties['name_resourse']:
                text += "Disk: "
            text += f"{self._get_disk_usage():.1f}%\n\n"

        self.properties['text'] = text[:-2]
    
    def update(self) -> None:
        
        if time.time() - self.last_update > 1 / self.properties['fps']:
            self.last_update = time.time()
            self.update_system_monitor_text()
    
        super().update()