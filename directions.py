class Direction():
  direction_list = ["north", "east", "south", "west"]

  def __init__(self, name, coord, origin):
    self.name = name
    self.coord = coord
    self.origin = origin

  @classmethod
  def get_key(cls, name):
    return cls.direction_list.index(name)


class Directions(dict):
  def get_direction(self, name):
    for direction in self.values():
      if direction.name == name: return direction

directions = Directions({
  "north": Direction("nord", [0, -1], "south"),
  "east": Direction("est", [1, 0], "west"),
  "south": Direction("sud", [0, 1], "north"),
  "west": Direction("ouest", [-1, 0], "east")
})