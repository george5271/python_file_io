# from fio.file import File
from fio.directory import Directory
from fio.file import File

assert Directory("test_dir").exists()
assert File("test_dir/1.txt").exists()
assert not Directory("not_exists_dir").exists()
assert not File("not_exists_file.txt").exists()


