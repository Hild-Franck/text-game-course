""" Contains abstract classes """

from abc import ABC
from colored import fg, attr
from directions import directions

reset = attr("reset")


class Interactable(ABC):
    """ Abstract class for all objects player can interact with """

    __base_use_desc = "Tu ne peux pas utiliser ca."

    def __init__(self, name, full_name, examine_desc):
        self.name = name
        self.full_name = fg(172) + full_name + reset
        self.examine_desc = examine_desc

    def init_from_room(self, room):
        pass

    def examine(self):
        print(self.examine_desc)

    def use(self):
        print(self.__base_use_desc)

    def take(self):
        print("Tu ne peux pas prendre ca.")

    def open(self):
        print("Cela ne s'ouvre pas")

    def drink(self):
        print("Euuuh... Non, ca ne se boit pas ca.")

    def burn(self):
        print("Impossible de bruler ca.")


class Item(Interactable, ABC):
    """ Abstract class for all object player can put in its inventory """

    takable = True


class Furniture(Interactable, ABC):
    """ Abstract class for objects that can contains Items """

    locked = False
    closed = False
    hidden = False

    def __init__(self, name, full_name, examine_desc, content=None, locked=False, hidden=False):
        super().__init__(name, full_name, examine_desc)
        self.content = content if content else []
        self.locked = locked
        self.hidden = hidden

    def examine(self):
        desc = self.examine_desc + " C'est fermé" if self.closed else self.examine_desc
        if self.content and not self.closed:
            desc += " A l'interieur, vous remarquez "
            desc += ", ".join([item.full_name for item in self.content]) + "."
            desc += "\nVous mettez vos trouvailles dans votre inventaire"
            Inventory.instance.content.extend(self.content)
            self.content.clear()
        print(desc)

    def open(self):
        if self.locked:
            if Inventory.instance.check_key():
                self.locked = False
                print("Vous deverouillez le coffre avec votre cle.")
            else:
                return print("Vous tentez de l'ouvrir mais rien n'y fait. C'est fermé a clé")
        if self.closed:
            desc = "Vous parvenez a l'ouvrir !"
            if not self.content:
                print(
                    "%s Malheureusement, vous ne voyez aucun objet de valeur ou utile." % desc)
            else:
                print("%s Vous voyez " % desc, end='')
                for loot in self.content:
                    print(loot.full_name, end='')
                print('.')
            self.closed = False
            self.full_name += " ouvert"
        else:
            print("C'est deja ouvert.")


class Inventory(Interactable):
    """ Singleton class for the player inventory """

    instance = None

    def __init__(self, content):
        super().__init__("sac", "votre sac", "Votre inventaire")
        self.content = content if content else []
        Inventory.instance = self

    def get_inventory(self):
        return [self]+self.content

    def examine(self):
        if not self.content:
            return print("Votre inventaire est vide")
        print("Vous ouvrez votre vieux sac de voyage. Vous y trouvez %s." %
              ",".join([item.full_name for item in self.content]))

    def open(self):
        self.examine()

    def check_key(self):
        for item in self.content:
            if item.name == "cle":
                return True
        return False


class GameManager():
    """ Singleton class that control the game """

    x = 0
    y = 0
    current_room = None
    look_around = False
    interactables = []
    instance = None

    def __init__(self, room_layout):
        self.room_layout = room_layout
        GameManager.instance = self

    def print_full_desc(self, force=False):
        if self.look_around and not force:
            return
        full_desc = self.current_room.desc + "\n"
        full_desc += "Vous remarquez une porte direction "
        full_desc += ", ".join([fg(75) + "%s" % directions[card].name +
                                reset for card, door in self.current_room.doors.items() if door])
        full_desc += "."
        if self.current_room.floor:
            full_desc += "\nSur le sol, vous voyez "
            full_desc += ', '.join(
                [item.full_name for item in self.current_room.floor]) + ".\n"
        if self.current_room.content:
            full_desc += "\nLa piece contient également "
            full_desc += ', '.join(
                [item.full_name for item in self.current_room.content if not item.hidden]) + "."
        self.look_around = True
        print(full_desc)

    def get_room_content(self):
        return [item for item in self.current_room.content if not item.hidden]

    def move(self, coord):
        self.x += coord[1]*-1
        self.y += coord[0]*-1

        self.current_room = self.room_layout[self.x][self.y]
        self.look_around = False


class Character():
    """ Singleton class representing the player """

    hit_point = 10
    instance = None

    def __init__(self):
        Character.instance = self

    def use(self, interactable):
        interactable.use(self)

    def heal(self, hit_point):
        print("Vous regagnez %d HP !" % hit_point)
        self.hit_point += hit_point
    
    def end(self, weapon):
        if weapon:
            print(f'Vous utilisez {weapon.full_name} pour fuir votre condition de testeur.')
        else:
            print('Vous ne trouvez aucun moyen de fuir de ce jeu, dommage.')
        self.hit_point -= self.hit_point

    def handle_death(self):
        return True if self.hit_point > 0 else False