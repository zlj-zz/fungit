class Stash:
    def __init__(self, index: int, name: str) -> None:
        self.index = index
        self.name = name

    def ref_name(self):
        return "stash@{}".format(self.index)

    def id(self):
        return self.ref_name()

    def description(self):
        return f"{self.ref_name()}: {self.name}"
