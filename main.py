from typing import List, Dict, Optional, Tuple

from fio.path import PathBase


class VirtualPath(PathBase):

    def __init__(self, path: str, virtual_item: Optional['VirtualItem'] = None):
        self.path: str = path
        self.virtual_item: Optional['VirtualItem'] = virtual_item

    def set_virtual_item(self, virtual_item: Optional['VirtualItem']):
        self.virtual_item = virtual_item

    def get_path(self) -> str:
        return self.path

    def exists(self) -> bool:
        return self.virtual_item is not None

    def __virtual_item_to_path(self, pair: Tuple) -> 'VirtualPath':
        return VirtualPath(f'{self.get_path()}/{pair[0]}', pair[1])

    def get_items(self) -> List['PathBase']:
        if isinstance(self.virtual_item, VirtualDirectory):
            self.virtual_item: VirtualDirectory
            return list(map(self.__virtual_item_to_path, self.virtual_item.items.items()))
        pass

    def is_file(self):
        return isinstance(self.virtual_item, VirtualFile)

    def is_dir(self):
        return isinstance(self.virtual_item, VirtualDirectory)

    def get_content(self):
        pass

    def size(self):
        if isinstance(self.virtual_item, VirtualFile):
            self.virtual_item: VirtualFile
            return self.virtual_item.size
        return 0

    def mtime(self):
        if isinstance(self.virtual_item, VirtualFile):
            self.virtual_item: VirtualFile
            return self.virtual_item.mtime
        return 0

    def copy(self, target: 'PathBase'):
        if not isinstance(target, VirtualPath):
            raise Exception('not supported path')
        target: VirtualPath
        target.virtual_item = self.virtual_item

    def create_path(self, item_name: str) -> 'PathBase':
        existed_item = None
        if isinstance(self.virtual_item, VirtualDirectory):
            self.virtual_item: VirtualDirectory
            existed_item = self.virtual_item.items.get(item_name, None)
        return VirtualPath(f'{self.get_path()}/{item_name}', existed_item)

    def remove(self):
        self.virtual_item = None


class VirtualItem:
    pass


class VirtualFile(VirtualItem):

    def __init__(self, size: int, mtime: float):
        self.size = size
        self.mtime = mtime


class VirtualDirectory(VirtualItem):

    def __init__(self):
        self.items: Dict[str, VirtualItem] = {}

    def append(self, name: str, item: VirtualItem):
        self.items[name] = item

    def __getitem__(self, name: str) -> Optional[VirtualItem]:
        return self.items.get(name, None)


# test_dir2/2.txt -> 2.txt
def extract_name(path: str) -> str:
    rindex = path.rfind('/')
    if rindex == -1:
        return path
    return path[rindex + 1:]


#
def sync(source: PathBase, target: PathBase):
    if source.is_dir() and not target.exists():
        source.copy(target)
    elif source.is_dir() and target.is_dir():
        source_items = source.get_items()
        target_items = target.get_items()

        removed_items: List['PathBase'] = []  # TODO: implement
        new_items: List['PathBase'] = []  # TODO: implement
        modified_items: Dict['PathBase', 'PathBase'] = {}  # TODO: implement
        for item in removed_items:
            item.remove()
        for item in new_items:
            item_name = extract_name(item.get_path())
            new_path = target.create_path(item_name)
            item.copy(new_path)
        for (source_item, target_item) in modified_items.items():
            source_item.copy(target_item)
    elif source.is_dir() and target.is_file():
        target.remove()
        source.copy(target)


# Создаём виртуальный каталог, идентичный настоящему
test_dir2 = VirtualDirectory()
test_dir2.append('2.txt', VirtualFile(1, 0))
test_dir = VirtualDirectory()
test_dir.append('1.txt', VirtualFile(3, 0))
test_dir.append('test_dir2', test_dir2)

# pt = PathTest('test_dir', test_dir)
# print(pt['1.txt'].exists())

backup = VirtualPath('backup')
sync(VirtualPath('test_dir', test_dir), backup)  # Ожидается, что создастся каталог `backup` с копией содержимого каталога `test_dir`

assert backup['test_dir'].exists()
assert backup['test_dir'].is_dir()
assert backup['test_dir']['1.txt'].exists()
assert backup['test_dir']['1.txt'].is_file()
assert backup['test_dir']['test_dir2'].exists()
assert backup['test_dir']['test_dir2'].is_dir()
assert backup['test_dir']['test_dir2']['2.txt'].exists()
assert backup['test_dir']['test_dir2']['2.txt'].is_file()



