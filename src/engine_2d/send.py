from numpy import ndarray

class SendDevice():
    def __init__(self,
                 name: str,
                 order: int,
                 width: int,
                 height: int,
                 is_active: bool = True,
                 x: int = 0,
                 y: int = 0) -> None:
        self.name: str = name
        self.is_active: bool = is_active
        self.order: int = order
        self.width: int = width
        self.height: int = height
        self.x: int = x
        self.y: int = y
    
    def send_frame(self, frame: ndarray) -> None:
        raise NotImplementedError

class WonderLand3d4832Device(SendDevice):
    def __init__(self,
                    name: str,
                    order: int = 0,
                    is_active: bool = True,
                    ip: str = '',
                    port: int = 0,
                    x: int = 0,
                    y: int = 0) -> None:
        width = 48
        height = 32
        super().__init__(name, order, width, height, is_active, x, y)
        self.ip: str = ip
        self.port: int = port
        
    def send_frame(self, frame: ndarray) -> None:
        pass