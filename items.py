from classes import Item
from colored import fg, attr

reset = attr("reset")

class HealthPotion(Item):
  examine_desc = "Une fiole de potion. Elle contient un liquide rouge qui semble étincellant."
  hp = 10
  __empty = False

  def __init__(self):
    super().__init__('potion de soin', "une potion de soin", self.examine_desc)

  def drink(self, character):
    if self.__empty:
      return print("La fiole de potion est vide")
    print("Vous brisez le sceau fermant le gouleau et buvez le contenu.")
    character.heal(self.hp)
    self.__empty = True
    self.examine_desc = "Une fiole de potion. Elle est vide."
    self.full_name = fg(172) + "une potion de soin" + reset + " vide"
  
  def open(self):
    print("En enlevant le sceau de cire bouchant la potion, vous risquez d'en renverser dans votre inventaire. Mieux vaut ne pas faire ca.")

class Key(Item):
  examine_desc = "Une lourde cle rouillee."

  def __init__(self):
    super().__init__('cle', "une cle", self.examine_desc)

class Lighter(Item):
  examine_desc = "Un briquet rudimentaire. Il peut creer une flamme petite mais puissante."

  def __init__(self):
    super().__init__("briquet", "un briquet", self.examine_desc)
