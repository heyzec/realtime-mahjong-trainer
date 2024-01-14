from ..utils.convert import tiles34_index_to_mpsz


class classproperty:
    def __init__(self, func):
        self.fget = func
    def __get__(self, instance, owner):
        return self.fget(owner)

class Tile:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Tile({self.name})"

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    @classproperty
    def all_tiles(cls):
        for i in range(34):
            yield Tile(tiles34_index_to_mpsz(i))

