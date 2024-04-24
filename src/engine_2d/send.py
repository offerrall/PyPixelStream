from numpy import ndarray

class SendDevice():
    def __init__(self,
                 name: str,
                 order: int = 0,
                 resolution: tuple[int, int] = (0, 0),
                 is_active: bool = True,
                 position: tuple[int, int] = (0, 0)) -> None:
        self.name: str = name
        self.is_active: bool = is_active
        self.order: int = order
        self.resolution: tuple[int, int] = resolution
        self.position: tuple[int, int] = position
    
    def send_frame(self, frame: ndarray) -> None:
        raise NotImplementedError

class WonderLand3d4832Device(SendDevice):
    def __init__(self,
                    name: str,
                    order: int = 0,
                    is_active: bool = True,
                    ip: str = '',
                    port: int = 0) -> None:
        resu = (48, 32)
        super().__init__(name, order, resu, is_active)
        self.ip: str = ip
        self.port: int = port
        
    def send_frame(self, frame: ndarray) -> None:
        pass