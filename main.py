# from fio.file import File
from fio.directory import Directory
from fio.file import File
from fio.path import Path, PathBase


def sync(source: PathBase, target: PathBase):
    pass



root_path = Path("test_dir")
print(Path("test_dir").mtime())
print(Path("test_dir/1.txt").size())
# print(root_path.exists())
# print(root_path.get_items())
# Написать тесты для всех функций в Path'е


# assert Directory("test_dir").exists()
# assert File("test_dir/1.txt").exists()
# assert not Directory("not_exists_dir").exists()
# assert not File("not_exists_file.txt").exists()


