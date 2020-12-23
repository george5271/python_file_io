from typing import List
import os
import shutil


class PathBase:

    def __init__(self, path: str):
        self.path = path

    def path(self) -> str:
        return self.path

    def exists(self) -> bool:
        pass

    def get_items(self) -> List['PathBase']:
        pass

    def is_file(self):
        pass

    def is_dir(self):
        pass

    def get_content(self):
        pass

    def size(self):
        pass

    def mtime(self):
        pass

    def copy(self, target: 'PathBase'):
        pass

    def remove(self):
        pass

    def create_path(self, item_name):
        pass

    def __getitem__(self, name: str):
        return Path(f'{self.path}/{name}')

    def __str__(self):
        return self.path

    def __repr__(self):
        return self.path


class Path(PathBase):
    def __init__(self, path: str):
        super().__init__(path)

    def exists(self) -> bool:
        return os.path.isfile(self.path) or os.path.isdir(self.path)

    def get_items(self) -> List['Path']:
        if os.path.isdir(self.path):
            items_list = []
            for element in os.listdir(self.path):
                f_path = self.path + '/' + element
                items_list.append(Path(f_path))
            return items_list
        else:
            raise KeyError("Путь не существует или не является директорией")

    def is_file(self):
        return os.path.isfile(self.path)

    def is_dir(self):
        return os.path.isdir(self.path)

    def get_content(self):
        if os.path.isfile(self.path):
            with open(self.path, 'r') as file:
                return str(file)
        else:
            raise KeyError("Путь не существует или не является файлом")

    def size(self):
        return os.stat(self.path).st_size

    def mtime(self):
        return os.stat(self.path).st_mtime

    def copy(self, target: 'PathBase'):
        shutil.copy2(self.path, target.path)  # TODO: Возможно стоить заменить на специализированное копирование файлов / каталогов

    def remove(self):
        os.remove(self.path)

    def create_path(self, item_name: str):
        return Path(f"{self.path}/{item_name}")
