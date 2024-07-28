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
