import numpy as np
import pyaudiowpatch as pyaudio
from threading import Thread
from time import time

from ...text import set_text_to_frame
from ...source import Source

class AudioVisualizer(Source):
    def __init__(self,
                 name: str,
                 order: int,
                 width: int,
                 height: int,
                 color: tuple[int, int, int] = (0, 255, 0),
                 mode: str = 'fft',
                 fps: int = 60,
                 transparent_background: bool = False):
        super().__init__(name, order, width, height)
        self.properties['color'] = color
        self.properties['transparent_background'] = transparent_background
        self.properties['mode'] = mode
        self.properties['fps'] = fps
        self.last_time_updated = 0
        self.reset()
        self.p = None
        self.stream = None
        self.last_data = None
        self.thread = None
        self.stop_thread = False
        self.no_audio = False
        self.edit_if = ['width', 'height']

    def set_not_audio_text(self) -> None:
        error = "No audio\ndetected"
        set_text_to_frame(error, self.frame, self.mask, "xsans", (255, 255, 255))

    def init_audio(self):
        
        self.p = pyaudio.PyAudio()
        try:
            wasapi_info = self.p.get_host_api_info_by_type(pyaudio.paWASAPI)
            default_speakers = self.p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
        except OSError:
            self.p.terminate()
            self.p = None
            self.no_audio = True
            return
        
        if not default_speakers["isLoopbackDevice"]:
            for loopback in self.p.get_loopback_device_info_generator():
                if default_speakers["name"] in loopback["name"]:
                    default_speakers = loopback
                    break

        self.stream = self.p.open(format=pyaudio.paInt16,
                                    channels=default_speakers["maxInputChannels"],
                                    rate=int(default_speakers["defaultSampleRate"]),
                                  input=True,
                                  frames_per_buffer=1024,
                                  input_device_index=default_speakers["index"])
        
        self.stop_thread = False
        self.thread = Thread(target=self.read_audio)
        self.thread.start()
        
    def read_audio(self):
        while not self.stop_thread:
            self.last_data = np.fromstring(self.stream.read(1024), dtype=np.int16)

    def reset(self) -> None:
        self.frame = np.zeros((self.height, self.width, 3), dtype=np.uint8)

    def update(self) -> None:
        if self.p is None and not self.no_audio:
            self.init_audio()
        
        forced_update = False
        if self.properties.cache:
            for prop in self.properties.cache:
                if prop in self.edit_if:
                    self.reset()
                    forced_update = True
                    break

            self.properties.reset_cache()
        
        if time() - self.last_time_updated > 1 / self.properties['fps'] or forced_update:
            self.last_time_updated = time()
            self.create_frame()

    def create_frame(self) -> None:

        if self.no_audio:
            self.set_not_audio_text()
            return

        data = self.last_data
        if data is None:
            return

        if self.properties['mode'] == 'waveform':
            self.waveform_vu(data)
        else:
            self.fft_vu(data)
        
        if self.properties['transparent_background']:
            self.mask = np.all(self.frame == self.properties['color'], axis=2)
        else:
            self.mask = None

    def disconnect(self) -> None:
        self.stop_thread = True
        if self.thread is not None:
            self.thread.join()
        self.thread = None
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        if self.p is not None:
            self.p.terminate()
        self.p = None

    def waveform_vu(self, data: np.ndarray) -> None:
        self.frame[:] = 0
        color = self.properties['color']

        center_height = self.height // 2
        scale_factor = (self.height // 2) / (2**15)

        for i in range(min(len(data), self.width)):
            normalized_sample = int((data[i] * scale_factor))
            
            y_start = center_height - normalized_sample
            y_end = center_height + normalized_sample

            y_start = max(0, y_start)
            y_end = min(self.height, y_end)

            if y_start < y_end:
                self.frame[y_start:y_end, i] = color

    def fft_vu(self, data: np.ndarray) -> None:
        fft_result = np.fft.fft(data)
        magnitudes = np.abs(fft_result)
        
        max_magnitude = max(magnitudes.max(), 1)
        normalized_magnitudes = np.interp(magnitudes, (0, max_magnitude), (0, self.height))
        
        num_frequencies = len(normalized_magnitudes)
        
        bar_width = max(1, self.width // num_frequencies)
        
        self.frame[:] = 0
        
        for i, magnitude in enumerate(normalized_magnitudes):
            bar_height = int(magnitude)
            
            x_start = i * bar_width
            x_end = x_start + bar_width
            
            for x in range(x_start, min(x_end, self.width)):
                y_start = max(0, self.height - bar_height)
                self.frame[y_start:self.height, x] = self.properties['color']