from numpy import ndarray

from .cached_dict import CachedDict


class Filter:
    
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
        name_new_filter = new_filter.name
        if self.check_name_exists(name_new_filter):
            raise ValueError(f"Filter with name '{name_new_filter}' already exists")

        self.filters.append(new_filter)
        self.sort()
    
    def getfilters(self) -> list[Filter]:
        return self.filters

    def remove(self, name: str) -> None:
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