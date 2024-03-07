from .text import Text

from datetime import datetime

class Date(Text):
    def __init__(self,
                 name: str,
                 order: int,
                 width: int,
                 height: int,
                 european_format: bool = True,
                 year: bool = True,
                 month: bool = True,
                 day: bool = True,
                 font: str = "xsans",
                 color: tuple[int, int, int] = (255, 255, 255),
                 background_color: tuple[int, int, int] = None):
        super().__init__(name, order, width, height,
                         text="",
                         text_from_file=None,
                         font=font, color=color, background_color=background_color)
        self.properties['year'] = year
        self.properties['month'] = month
        self.properties['day'] = day
        self.properties['european_format'] = european_format
        self.update_date_text()

    def update_date_text(self):
        if self.properties['european_format']:
            date_format = ""
            if self.properties['day']:
                date_format += "%d/"
            if self.properties['month']:
                date_format += "%m/"
            if self.properties['year']:
                date_format += "%Y"
        else:
            date_format = ""
            if self.properties['year']:
                date_format += "%Y/"
            if self.properties['month']:
                date_format += "%m/"
            if self.properties['day']:
                date_format += "%d"
        
        date_format = date_format.rstrip("/-")
        
        current_date = datetime.now().strftime(date_format)
        self.properties['text'] = current_date

    def update(self) -> None:
        self.update_date_text()
        super().update()