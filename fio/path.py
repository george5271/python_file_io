from typing import List


class Path:

    def __init__(self, path: str):
        self.path = path

    def path(self):
        return self.path

    def exists(self):
        pass

    def get_items(self) -> List['Path']:
        pass

    def is_file(self):
        pass

    def is_dir(self):
        pass

    def get_content(self):
        pass

    def __str__(self):
        return self.path

    def __repr__(self):
        return self.path
