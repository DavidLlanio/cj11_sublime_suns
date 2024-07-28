from datetime import datetime
from .generator import BufferItem
from .item_generator import Item


class Character:
    """Class for keeping track of character information"""

    def __init__(self):
        self.name: str = ""
        self.sex: str = ""
        self.race: str = ""
        self.class_: str = ""
        self.coins: int = 0
        self.equipped_helmet: Item = Item()
        self.equipped_armor: Item = Item()
        self.equipped_boots: Item = Item()
        self.equipped_necklace: Item = Item()
        self.equipped_weapon: Item = Item()
        self.inventory: list[Item] = []
        self.buffer: list[BufferItem] = []
        self.quest_log: list[str] = []
        self.ranking_points: int = 0
        self.last_checkin = datetime.now()

    def equip_best(self):
        for item in self.inventory:
            item_t = item.type_
            if (
                item_t == "Weapon"
                and item.enumerate_rarity()
                > self.equipped_weapon.enumerate_rarity()
            ):
                self.equipped_weapon = item
            elif (
                item_t == "Helmet"
                and item.enumerate_rarity()
                > self.equipped_helmet.enumerate_rarity()
            ):
                self.equipped_helmet = item
            elif (
                item_t == "Armor"
                and item.enumerate_rarity()
                > self.equipped_armor.enumerate_rarity()
            ):
                self.equipped_armor = item
            elif (
                item_t == "Boots"
                and item.enumerate_rarity()
                > self.equipped_boots.enumerate_rarity()
            ):
                self.equipped_boots = item
            elif (
                item_t == "Necklace"
                and item.enumerate_rarity()
                > self.equipped_necklace.enumerate_rarity()
            ):
                self.equipped_necklace = item

    def get_pretty_quest_log(self):
        return "\n".join(self.quest_log)

    def get_pretty_equipment_list(self):
        formatted_string = f"Helmet = {self.equipped_helmet}({self.equipped_helmet.rarity})\nArmor = {self.equipped_armor.name}({self.equipped_armor.rarity})\nNecklace = {self.equipped_necklace.name}({self.equipped_necklace.rarity})\nBoots = {self.equipped_boots.name}({self.equipped_boots.rarity})\nWeapon = {self.equipped_weapon.name}({self.equipped_weapon.rarity})\n"
        return formatted_string
