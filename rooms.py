from directions import Direction, directions
from items import *
from furnitures import *

class Room():
  floor = set()
  doors = {
    "north": False,
    "east": False,
    "south": False,
    "west": False
  }
  def __init__(self, content, desc):
    self.content = content
    self.desc = desc
    self.doors = self.doors.copy()
    for item in self.content.copy(): item.init_from_room(self)
  
  def set_connections(self, connection_tuple):
    for index, direction in enumerate(connection_tuple):
      if direction: self.doors[Direction.direction_list[index]] = True

data = [
  [
    (set([Shelf([HealthPotion(), Lighter()])]), "Vous vous trouvez dans une piece mal eclairée. Les murs et le sol sont constitués de blocs de granit mal taillés."),
    (set([Chest(locked=True), Tapestry(Shelf())]), "Vous arrivez dans une grande salle. Un plancher recouvre le sol, tandis que les murs de granit sont cache par une seule et immense tapisserie")
  ],
  [
    (set([Table([Key()])]), "Une grande piece de pierres grisatres. De la mousse en recouvre ca et la les paroies humides"),
    ([], "Vous arrivez dans une grande salle. Un plancher recouvre le sol, tandis que les murs de granit sont cache par une seule et immense tapisserie")
  ]
]

connections = [
  [[0, 1, 0, 0], [0, 0, 1, 0]],
  [[0, 0, 0, 0], [0, 0, 0, 1]]
]

room_layout = []

# Create rooms
for x, room_column in enumerate(data):
  for y, room_data in enumerate(room_column):
    if len(room_layout) < x+1:
      room_layout.append([])
    room_layout[x].append(Room(room_data[0], room_data[1]))

# Create rooms connections
for x, room_column in enumerate(room_layout):
  for y, room in enumerate(room_column):
    connection = connections[x][y]
    room.set_connections(connection)

    for index, direction in enumerate(Direction.direction_list):
      if connection[index]:
        [ox, oy] = directions[direction].coord
        room_layout[x+oy][y+ox].doors[directions[direction].origin] = True