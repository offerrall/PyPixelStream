from numpy import ndarray

from .source import Source
from .filter import FiltersList
from .canvas import apply_source_to_background
from .serialize.serialize import source_to_dict, dict_to_source, save_scene_to_file
from random import choices
from string import ascii_letters, digits


class Scene:

    """
    This class manages the scenes of the application, it is in charge of managing the sources and the filters of the Scene.
    It is also in charge of saving the state of the scene in a json file.
    """

    def __init__(self,
                 name: str,
                 order: int = 0,
                 internal_id: str | None = None) -> None:
        self.sources: list[Source] = []
        self.name: str = name
        self.order: int = order
        self.filters: FiltersList = FiltersList()
        self.internal_id: str = internal_id
        if self.internal_id is None:
            self.internal_id: str = ''.join(choices(ascii_letters + digits, k=60))

    def save(self, folder: str) -> None:
        save_scene_to_file(self.name,
                           self.internal_id,
                           self.order,
                           self.sources,
                           self.filters.filters,
                           folder)

    def update_order(self) -> None:
        self.sources.sort(key=lambda s: s.order)
        for i, source in enumerate(self.sources):
            source.order = i + 1

    def check_name_exists(self, name: str, strip: bool = True) -> bool:
        if strip:
            name = name.strip()
        for source in self.sources:
            if source.name == name:
                return True
        return False

    def add_source(self, source: Source) -> None:
        """
        This method adds a source to the scene, if the source already exists it raises a ValueError.
        """
        if self.check_name_exists(source.name):
            raise ValueError(f"Source with name '{source.name}' already exists")

        self.sources.append(source)
        self.update_order()

    def remove_source(self, source: Source) -> None:
        """
        This method removes a source from the scene, if the source is not found it raises a ValueError.
        """
        try:
            source.disconnect()
            self.sources.remove(source)
        except ValueError:
            raise ValueError(f"Source with name '{source.name}' not found")
        self.update_order()

    def get_source(self, name: str) -> Source:
        """
        This method returns a source with the name given, if the source is not found it raises a ValueError.
        """
        for source in self.sources:
            if source.name == name:
                return source
        raise ValueError(f"Source with name '{name}' not found")

    def up_source(self, source: Source) -> None:
        source.order += 1.5
        self.update_order()
    
    def down_source(self, source: Source) -> None:
        source.order -= 1.5	
        self.update_order()

    def duplicate_source(self, source: Source) -> None:
        new_name = f"{source.name} copy"
        while True:
            try:
                self.get_source(new_name)
                new_name += " copy"
            except ValueError:
                break
        
        copy_source = dict_to_source(source_to_dict(source))
        copy_source.name = new_name
        copy_source.order = source.order - 0.5
        self.add_source(copy_source)

    def disconnect(self) -> None:
        for source in self.sources:
            source.set_selected(False)
            source.disconnect()

    def connect(self) -> None:
        for source in self.sources:
            source.connect()

    def update(self, background: ndarray) -> None:
        """
        This method updates the scene by updating the sources and applying the filters to the background.
        is basically the main loop of the scene and is called by the engine.
        """
        selected_mode = False
        
        for source in self.sources:
            if source.is_selected:
                selected_mode = True
            source.update()
            frame = source.frame
            mask = source.mask

            if frame is None:
                continue
            
            if source.filters.filters:
                frame, mask = source.filters.apply(frame, mask)

            if source.is_visible:    
                apply_source_to_background(background, source, frame, mask)
        
        if self.filters.filters and not selected_mode:
            frame, mask = self.filters.apply(background)
            background[...] = frame
            if mask is not None:
                background[mask] = 0