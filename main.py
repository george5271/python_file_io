# from fio.file import File
from typing import List, Dict

from fio.path import Path, PathBase


class PathTest(PathBase):

    def __init__(self, virtual_path: 'VirtualPath'):
        super().__init__(virtual_path.name)
        self.virtual_path = virtual_path


    def exists(self) -> bool:
        return self.virtual_path is not None

    def get_items(self) -> List['PathBase']:
        if self.virtual_path is VirtualDirectory:
            return self.virtual_path.items
        pass

    def is_file(self):
        return self.virtual_path is VirtualFile

    def is_dir(self):
        return self.virtual_path is VirtualDirectory

    def get_content(self):
        pass

    def size(self):
        if self.virtual_path is VirtualFile:
            return self.virtual_path.size
        return 0

    def mtime(self):
        if self.virtual_path is VirtualFile:
            return self.virtual_path.mtime
        return 0

    def copy(self, target: 'Path'):
        pass


class VirtualPath:

    parent_dir: str = None

    def __init__(self, name: str):
        self.name = name


    def path(self):
        if self.parent_dir is None:
            return self.name
        return f"{self.parent_dir}/{self.name}"


class VirtualFile(VirtualPath):

    def __init__(self, name: str, size: int, mtime: float):
        super().__init__(name)
        self.size = size
        self.mtime = mtime

    def __str__(self) -> str:
        return f"name: {self.name}, size: {self.size}, mtime: {self.mtime}, path: {self.path()}"

    def __repr__(self) -> str:
        return self.__str__()


class VirtualDirectory(VirtualPath):

    items: List[VirtualPath] = []

    def __init__(self, name: str):
        super().__init__(name)

    def append(self, path: VirtualPath):
        path.parent_dir = self.path()
        self.items.append(path)

    def __str__(self) -> str:
        return f"name: {self.name}, items: {self.items}, path: {self.path()}"

    def __repr__(self) -> str:
        return self.__str__()

    def __getitem__(self, name: str):
        for item in self.items:
            if item.name == name:
                return item
        return None

# test_dir2/2.txt -> 2.txt
def extract_name(path):
    return str(path.split('/')[-1])

#
def sync(source: PathBase, target: PathBase):
    if source.is_dir() and not target.exists():
        source.copy(target)
    elif source.is_dir() and target.is_dir():
        source_items = source.get_items()
        target_items = target.get_items()

        removed_items: List['PathBase'] = list(set(source_items)-set(target_items))
        new_items: List['PathBase'] = list(set(target_items)-set(source_items))
        modified_items: Dict['PathBase', 'PathBase'] = {}   # TODO: implement
        for item in removed_items:
            item.remove()
        for item in new_items:
            item_name = extract_name(item.path())
            new_path = target.create_path(item_name)
            item.copy(new_path)
        for (source_item, target_item) in modified_items.items():
            source_item.copy(target_item)
    elif source.is_dir() and target.is_file():
        target.remove()
        source.copy(target)


test_dir2 = VirtualDirectory('test_dir2')
test_dir2.append(VirtualFile('2.txt', 1, 0))
source_dir = VirtualDirectory('test_dir')
source_dir.append(VirtualFile('1.txt', 3, 0))
source_dir.append(test_dir2)


sync(Path('test_dir'), Path('backup'))  # Ожидается, что создастся каталог `backup` с копией содержимого каталога `test_dir`
