class CachedDict(dict):

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
