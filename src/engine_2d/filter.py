from numpy import ndarray

from .cached_dict import CachedDict


class Filter:

    """
    This class is the basis for all filters that can be added to a source or a scene.
    All objects that you want to add to a source or a scene must inherit from this class.
    Each filter has its common attributes and properties.
    Its properties must be managed in a special dictionary called properties. More information in the CachedDict documentation.

    This class is an abstract class, so you cannot instantiate it directly unless you know what you are doing.
    The apply() method must be implemented in every class that inherits from Filter.
    After implementing a new filter you should add to the engine_2d/filters/__init__.py file the import of the new filter.

    You can look at engine_2d/filters/ for examples of how filters can be implemented.
    """

    def __init__(self, name: str, order: int = 0):
        self.name: str = name
        self.order: int = order
        self.is_visible: bool = True
        self.properties: CachedDict = CachedDict()
    
    def set_visible(self, visible: bool) -> None:
        self.is_visible = visible
        self.properties['visible'] = visible

    def apply(self,
              frame: ndarray,
              mask: ndarray | None = None
              ) -> tuple[ndarray, ndarray]:
        raise NotImplementedError("Child classes must implement this method.")

class FiltersList:

    """
    This class is a list of filters of a source or scene.
    """

    def __init__(self):
        self.filters: list[Filter] = []

    def check_name_exists(self, name: str) -> bool:
        for f in self.filters:
            if f.name == name:
                return True
        return False
    
    def sort(self) -> None:
        self.filters.sort(key=lambda f: f.order)
        for i, f in enumerate(self.filters):
            f.order = i
    
    def add(self, new_filter: Filter) -> None:
        """
        This method adds a filter to the list of filters, if the filter already exists it raises a ValueError.
        """
        name_new_filter = new_filter.name
        if self.check_name_exists(name_new_filter):
            raise ValueError(f"Filter with name '{name_new_filter}' already exists")

        self.filters.append(new_filter)
        self.sort()
    
    def getfilters(self) -> list[Filter]:
        return self.filters

    def remove(self, name: str) -> None:
        """
        This method removes a filter from the list of filters, if the filter is not found it raises a ValueError.
        """
        for i, f in enumerate(self.filters):
            if f.name == name:
                self.filters.pop(i)
                self.sort()
                return
        raise ValueError(f"Filter with name '{name}' not found")

    def apply(self,
              frame: ndarray,
              mask: ndarray | None = None
              ) -> tuple[ndarray, ndarray]:
        
        if not self.filters:
            return frame, mask
        frame = frame.copy()
        mask = mask.copy() if mask is not None else None
        for f in self.filters:
            if f.is_visible:
                frame, mask = f.apply(frame, mask)
    
        return frame, mask