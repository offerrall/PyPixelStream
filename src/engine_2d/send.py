from numpy import ndarray

class SendDevice():
    """
    A send device is a device that sends the image to the different outputs.
    In the ./senders/ folder there are the different senders that can be used.
    """
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
        self.internal_id: str | None = None
    
    def send_frame(self, frame: ndarray) -> None:
        raise NotImplementedError