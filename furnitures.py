from classes import Furniture, GameManager
from colored import fg, attr

reset = attr("reset")

class Chest(Furniture):
  examine_desc = "Il s'agit d'un coffre ayant subit les ravages du temps."
  closed = True

  def __init__(self, content=None, locked=False):
    super().__init__('coffre', "un coffre", self.examine_desc, content, locked)

class Shelf(Furniture):
  examine_desc = "C'est une étagère en bois massif."

  def __init__(self, content=None, locked=False):
    super().__init__('étagère', "une étagère", self.examine_desc, content, locked)


class Table(Furniture):
  examine_desc = "Une petite table ronde, en pierre."

  def __init__(self, content=None, locked=False):
    super().__init__('table', "une table", self.examine_desc, content, locked)

class Tapestry(Furniture):
  examine_desc = "Une immense tapisserie, qui semble conter les exploit d'un roi d'antan."
  room = None

  def __init__(self, hidden_furniture, content=None, locked=False):
    super().__init__('tapisserie', "une tapisserie", self.examine_desc, content, locked)
    hidden_furniture.hidden = True
    self.hidden_furniture = hidden_furniture
  
  def init_from_room(self, room):
    room.content.add(self.hidden_furniture)
    self.room = room

  def burn(self):
    print("La tapisserie s'embrase soudain, et en quelques minutes, il n'en reste rien. Elle devoile alors, encastre dans le mur, %s." %self.hidden_furniture.full_name)
    self.hidden_furniture.hidden = False
    self.room.content.remove(self)