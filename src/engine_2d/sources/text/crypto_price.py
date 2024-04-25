import time
from threading import Thread

from utils.cryptocurrency.cryptocurrency import get_cripto_price, get_cripto_list, cripto_to_symbol
from .text import Text

class CryptoPrice(Text):
    def __init__(self,
                 name: str,
                 order: int,
                 width: int,
                 height: int,
                 crypto_name: str = "bitcoin",
                 fiat: str = "eur",
                 font: str = "xsans",
                 show_symbol: bool = True,
                 show_fiat: bool = True,
                 color: tuple[int, int, int] = (255, 255, 255),
                 background_color: tuple[int, int, int] = None):
        super().__init__(name, order, width, height,
                         text="",
                         text_from_file=None,
                         font=font, color=color, background_color=background_color)
        self.properties['crypto_name'] = crypto_name
        self.properties['fiat'] = fiat
        self.properties['show_symbol'] = show_symbol
        self.properties['show_fiat'] = show_fiat
        self.last_price = None
        self.last_fiat = None
        self.last_update_time = None
        self.edit_if = ['crypto_name', 'fiat']

    def _update_info(self):
        try:
            self.last_price = get_cripto_price(self.properties['crypto_name'], self.properties['fiat'])
            self.last_fiat = self.properties['fiat']
        except Exception as e:
            self.last_price = "Waiting..."

    def update_info(self):
        thread = Thread(target=self._update_info)
        thread.start()

    def update_crypto_price(self):
        price = self.last_price
        name_symbol = cripto_to_symbol(self.properties['crypto_name'])
        text = ""
        if self.properties['show_symbol']:
            text += f"{name_symbol.upper()}: "
        text += f"{price}"
        if self.properties['show_fiat']:
            text += f" {self.properties['fiat'].upper()}"
        self.properties['text'] = text

    def update(self) -> None:
        update = False
        if self.last_update_time is None or time.time() - self.last_update_time > 60:
            self.last_update_time = time.time()
            update = True
        
        for prop in self.properties.cache:
            if prop in self.edit_if:
                update = True
                break
        
        if update:
            self.update_info()
            self.properties.reset_cache()
        
        self.update_crypto_price()

        super().update()