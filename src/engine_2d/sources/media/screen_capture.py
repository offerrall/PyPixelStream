from mss import mss
import numpy as np
from threading import Thread

from ...source import Source
from ...image_operations.image_operations import nearest_neighbor_resize_vectorized, convert_bgra_to_rgb

class ScreenCapture(Source):

    def __init__(self, name: str, order: int, width: int, height: int, monitor: int = 1):
        super().__init__(name, order, width, height)
        self.properties['monitor'] = monitor
        self.state = "inactive"
        self.thread = None

    def get_indexs(self) -> list:
        with mss() as sct:
            monitors = sct.monitors
        return monitors

    def _get_frame(self):
        with mss() as sct:
            while self.state == "active":
                frame = sct.grab(sct.monitors[self.properties['monitor']])
                frame_array = np.array(frame)
                frame_array = frame_array[..., :3]
                if frame_array.shape[0] != self.height or frame_array.shape[1] != self.width:
                    frame_array = nearest_neighbor_resize_vectorized(frame_array, self.width, self.height)
                self.frame = convert_bgra_to_rgb(frame_array)

    def update(self) -> None:
        if self.state == "inactive":
            self.connect()

    def connect(self) -> None:
        self.state = "active"
        self.thread = Thread(target=self._get_frame)
        self.thread.start()

    def disconnect(self) -> None:
        self.state = "inactive"
        if self.thread is not None:
            self.thread.join()
            self.thread = None
