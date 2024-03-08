

class CachedDict(dict):
    """
    This class is a dictionary that keeps track of the keys that are being added and deleted.
    This is in order to be able to react to changes in source properties more efficiently.

    Example:
        def update(self) -> None:
            if self.properties.cache:
                edit_if = ['image_path', 'width', 'height']

                for prop in self.properties.cache:
                    if prop in edit_if:
                        self.create_image()
                        break

                self.properties.reset_cache()

    This is a snippet from the Image source class. The update method is called every time the source is updated.
    The CachedDict is used to keep track of the properties that have been changed. If the properties that have been changed
    are in the edit_if list, then the source is updated. This is a way to avoid updating if no changes have been made.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache: list[str] = []

    def reset_cache(self) -> None:
        self.cache = []

    def __setitem__(self, key, value):
        if not key in self.cache:
            self.cache.append(key)
        super().__setitem__(key, value)

    def __delitem__(self, key):
        if key in self:
            self.cache.append(key)
        super().__delitem__(key)
