# from fio.file import File
from typing import List

from fio.directory import Directory
from fio.file import File
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


def sync(source: PathBase, target: PathBase):
    if source.is_dir() and target.is_dir():
        source_items = source.get_items()
        target_items = target.get_items()

    pass


test_dir2 = VirtualDirectory('test_dir2')
test_dir2.append(VirtualFile('2.txt', 1, 0))
source_dir = VirtualDirectory('test_dir')
source_dir.append(VirtualFile('1.txt', 3, 0))
source_dir.append(test_dir2)

print(source_dir['test_dir2'].path())

print(source_dir)
root_path = Path("test_dir")
print(Path("test_dir").mtime())
print(Path("test_dir/1.txt").size())
print(root_path.exists())
print(root_path.get_items())

# Написать тесты для всех функций в Path'е


# assert Directory("test_dir").exists()
# assert File("test_dir/1.txt").exists()
# assert not Directory("not_exists_dir").exists()
# assert not File("not_exists_file.txt").exists()
