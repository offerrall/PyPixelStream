from numpy import ndarray

from .cached_dict import CachedDict
from .filter import FiltersList

class Source:

    """
    This class is the basis for all sources that can be added to a scene.
    All objects that you want to add to a scene must inherit from this class.
    Each source has its common attributes and its own attributes.
    Its own attributes must be managed in a special dictionary called properties.
    This dictionary is a CachedDict, see the CachedDict documentation for more information.
    Each source also has a list of filters that can be applied to it. Check the Filter class for more information.

    This class is an abstract class, so you cannot instantiate it directly unless you know what you are doing.
    The update() method must be implemented in every class that inherits from Source.
    The connect() and disconnect() methods are optional and must be implemented if you require the source to do something when connecting or disconnecting.

    You can look at engine_2d/sources/ for examples of how sources can be implemented.
    After implementing a new source you should add to the engine_2d/sources/__init__.py file the import of the new source.
    """

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