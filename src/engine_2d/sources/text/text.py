from numpy import full, uint8

from ...source import Source
from ...text import convert_text_to_image

class Text(Source):

    def __init__(self,
                 name: str,
                 order: int,
                 width: int,
                 height: int,
                 text: str = "Text",
                 text_from_file: str | None = None,
                 font: str = "xsans",
                 color: tuple[int, int, int] = (255, 255, 255),
                 background_color: tuple[int, int, int] = None):
        super().__init__(name, order, width, height)
        self.properties['text'] = text
        self.properties['font'] = font
        self.properties['color'] = color
        self.properties['text_from_file'] = text_from_file
        self.properties['background_color'] = background_color
        self.cache_txt_text = None

    def create_text(self) -> None:
        text = self.properties['text']
        if self.properties['text_from_file'] is not None:
            text += self.read_from_file(self.properties['text_from_file'])
        
        frame, mask = convert_text_to_image(text,
                                            self.properties['font'],
                                            self.properties['color'],
                                            self.properties['background_color'])
        background = full((self.height, self.width, 3), (0, 0, 0), dtype=uint8)
        cut1 = frame.shape[0]
        cut2 = frame.shape[1]

        if cut1 > self.height:
            cut1 = self.height
        
        if cut2 > self.width:
            cut2 = self.width

        background[:cut1, :cut2] = frame[:cut1, :cut2]
        mask_background = full((self.height, self.width), False, dtype=bool)
        mask_background[:cut1, :cut2] = mask[:cut1, :cut2]

        self.frame = background
        self.mask = mask_background

    def read_from_file(self, file: str) -> None:
        try:
            with open(file, 'r') as file:
                return file.read()
        except:
            self.properties['text_from_file'] = None
            return ""
    
    def check_if_text_from_file_changed(self) -> bool:
        if self.properties['text_from_file'] is None:
            return False
        cont = self.read_from_file(self.properties['text_from_file'])
        if cont != self.cache_txt_text:
            self.cache_txt_text = cont
            return True
        return False

    def update(self) -> None:
        if self.frame is None:
            self.create_text()
            return
        if self.properties['text_from_file'] is not None:
            if self.check_if_text_from_file_changed():
                self.create_text()
                return
        if self.properties.cache:
            edit_if = ['text', 'font', 'color', 'background_color', 'width', 'height', 'text_from_file']
            for prop in self.properties.cache:
                if prop in edit_if:
                    self.create_text()
                    break
            self.properties.reset_cache()
