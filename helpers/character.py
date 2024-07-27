from dataclasses import dataclass

from generator import BufferItem
from item_generator import Item


@dataclass
class Character:
    """Class for keeping track of character information"""

    name: str = ""
    sex: str = ""
    race: str = ""
    class_: str = ""
    coins: int = 0
    equipped_helmet: Item = None
    equipped_armor: Item = None
    equipped_boots: Item = None
    equipped_necklace: Item = None
    equipped_weapon: Item = None
    inventory: list[Item] = []
    buffer: list[BufferItem] = []
    quest_log: list[str] = []
    ranking_points: int = 0

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
