from numpy import ndarray


class SendDevice():
    def __init__(self, name: str, ip: str, port: int, is_active: bool = True) -> None:
        self.name: str = name
        self.ip: str = ip
        self.port: int = port
        self.is_active: bool = is_active

    
    def send_image(self, image: ndarray) -> None:
        print(f"Sending image to {self.name} at {self.ip}:{self.port}")