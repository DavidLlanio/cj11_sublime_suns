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

    def equip_best(self) -> None:
        """
        Equips the best item of each type in the inventory
        """
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

    def get_pretty_quest_log(self) -> str:
        """
        Returns:
            str: A formatted string of the character's quest log
        """
        return "\n".join(list(filter(None, self.quest_log)))

    def get_pretty_equipment_list(self) -> str:
        """
        Returns:
            str: A formatted string of the character's equipment list
        """
        helmet = (
            f"Helmet: {' '.join(str(self.equipped_helmet).split('\n')[:-1])} ({self.equipped_helmet.rarity})"
            if self.equipped_helmet.rarity
            else "Helmet: *None*"
        )
        armor = (
            f"Armor: {' '.join(str(self.equipped_armor).split('\n')[:-1])} ({self.equipped_armor.rarity})"
            if self.equipped_armor.rarity
            else "Armor: *None*"
        )

        necklace = (
            f"Necklace: {' '.join(str(self.equipped_necklace).split('\n')[:-1])} ({self.equipped_necklace.rarity})"
            if self.equipped_necklace.rarity
            else "Necklace: *None*"
        )

        boots = (
            f"Boots: {' '.join(str(self.equipped_boots).split('\n')[:-1])} ({self.equipped_boots.rarity})"
            if self.equipped_boots.rarity
            else "Boots: *None*"
        )

        weapon = (
            f"Weapon: {' '.join(str(self.equipped_weapon).split('\n')[:-1])} ({self.equipped_weapon.rarity})"
            if self.equipped_weapon.rarity
            else "Weapon: *None*"
        )

        formatted_string = f"{helmet}\n{armor}\n{necklace}\n{boots}\n{weapon}"

        return formatted_string
