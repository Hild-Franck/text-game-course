# Cours de programmation

# Creation d'une aventure textuelle

from classes import *
from directions import *
from items import Lighter
from rooms import room_layout

player = Character()
actions = ["Examiner", "Observer", "Ouvrir",
           "Boire", "Lacher", "Aller", "Bruler"]
inventory = Inventory([])
game_manager = GameManager(room_layout)


def get_obj(obj_dict, verb="examiner", obj=""):
    # obj_list_str = " | ".join([item.name for item in obj_dict.values()])
    obj = obj.replace(" ", "") or input(
        "Que voulez vous %s ?\n> " % verb).upper().replace(" ", "")
    if not obj in obj_dict:
        return print("Il n'y a rien de tel ici.")
    return obj_dict[obj]


def go(direction=""):
    direction = direction.replace(" ", "") or input(
        "Ou voulez vous aller ?\n> ").upper().replace(" ", "")

    if not direction in [d.name.upper() for d in directions.values()]:
        return print("Cette direction n'existe pas")

    if direction not in [directions[d].name.upper() for d, c in game_manager.current_room.doors.items() if c]:
        return print("C'est un mur. Vous ne pouvez pas passer.")

    return game_manager.move(directions.get_direction(direction.lower()).coord)


def parse_action(user_choice):
    array = user_choice.split()
    return (array.pop(0), " ".join(array))


def handle_action(action, obj_choice):
    objs = {item.name.upper().replace(" ", ""): item for item in (
        inventory.get_inventory()+game_manager.get_room_content())}
    if action == "EXAMINER":
        obj = get_obj(objs, "examiner", obj_choice)
        if not obj:
            return
        return obj.examine()
    elif action == "OBSERVER":
        game_manager.print_full_desc(True)
    elif action == "OUVRIR":
        obj = get_obj(objs, "ouvrir", obj_choice)
        if not obj:
            return
        return obj.open()
    elif action == "BOIRE":
        obj = get_obj(objs, "boire", obj_choice)
        if not obj:
            return
        return obj.drink(player)
    elif action == "LACHER":
        obj = get_obj(objs, "lacher", obj_choice)
        if not obj:
            return
        if obj not in inventory.content:
            return print("Ce n'est pas dans votre inventaire, vous ne pouvez le lacher")
        print("Vous lachez %s au sol." % obj.full_name)
        game_manager.current_room.floor.add(obj)
        inventory.content.remove(obj)
    elif action == "ALLER":
        return go(obj_choice)
    elif action == "BRULER":
        for item in inventory.content:
            if isinstance(item, Lighter):
                obj = get_obj(objs, "bruler", obj_choice)
                return obj.burn()
        return print("Tu ne possede rien pour bruler quoique se soit.")


game_manager.current_room = room_layout[0][0]

print(("Vous revenez a vous peu a peu. Tout est flou dans votre esprit. " +
       "A votre droite, vous remarquez %s sur le sol" % inventory.full_name + ". " +
       "Vous le mettez sur le dos, et attendez que vos yeux s'habituent a la luminosite."))

while True:
    game_manager.print_full_desc()
    user_choice = input("\n\nQue voulez vous faire ?\n( %s )\n> " %
                        " | ".join(actions)).upper()
    action, obj = parse_action(user_choice)
    if action == "QUITTER":
        print("Vous avez abandonné le jeu. SHAME. SHAAAAAAAAAAME")
        break
    if action not in [a.upper() for a in actions]:
        print("Cette action n'éxiste pas\n")
        continue
    print('')
    handle_action(action, obj)
