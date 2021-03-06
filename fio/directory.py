import os
from typing import List
from fio.file import File


class Directory:

    def __init__(self, path: str):
        self.path = path

    def path(self):
        return self.path

    def get_files(self) -> List['File']:
        file_list = []
        for element in os.listdir(self.path):
            f_path = self.path + '/' + element
            if os.path.isfile(f_path):
                file_list.append(File(f_path))
        return file_list

    def get_directories(self) -> List['Directory']:
        directory_list = []
        for element in os.listdir(self.path):
            dir_path = self.path + '/' + element
            if os.path.isdir(dir_path):
                directory_list.append(Directory(dir_path))
        return directory_list

    def __str__(self):
        return(self.path)

    def __repr__(self):
        return(self.path)

    def exists(self) -> bool:
        return os.path.isdir(self.path)
