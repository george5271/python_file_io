class File:

    def __init__(self, path: str):
        self.path = path

    def path(self):
        return self.path

    def content(self) -> str:
        with open(self.path, 'r') as file:
            return str(file)

    def exists(self) -> bool:
        pass