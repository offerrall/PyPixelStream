from numpy import ndarray

from .cached_dict import CachedDict
from .filter import FiltersList

class Source:

    def __init__(self,
                 name: str,
                 order: int,
                 width: int,
                 height: int):

        self.name: str = name
        self.order: int = order
        self.width: int = width 
        self.height: int = height
        self.x: int = 0
        self.y: int = 0
        self.is_visible: bool = True
        self.is_selectable: bool = True
        self.is_selected: bool = False
        self.mask: ndarray | None = None
        self.frame: ndarray | None = None
        self.properties: CachedDict = CachedDict()
        self.filters: FiltersList = FiltersList()
    
    def set_height_and_width(self, height: int, width: int) -> None:
        atm_size = self.width, self.height
        if atm_size == (width, height):
            return
        self.properties['width'] = width
        self.properties['height'] = height
        self.height = height
        self.width = width
    
    def set_position(self, position: tuple[int, int]) -> None:
        self.x = position[0]
        self.y = position[1]
        self.properties['position'] = position
    
    def set_visible(self, visible: bool) -> None:
        self.is_visible = visible
        self.properties['visible'] = visible
    
    def set_selectable(self, selectable: bool) -> None:
        self.is_selectable = selectable
        self.properties['selectable'] = selectable

    def set_selected(self, selected: bool) -> None:
        self.is_selected = selected
        self.properties['selected'] = selected

    def update(self) -> None:
        raise NotImplementedError("update() method must be implemented")

    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        pass