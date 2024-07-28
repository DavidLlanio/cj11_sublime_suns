import os
import random
import time
from dataclasses import dataclass
from random import choice, choices


@dataclass
class Item:
    """Class for keeping track of item information"""

    name: str = ""
    type_: str = ""
    rarity: str = ""

    def __str__(self) -> str:
        return f"{self.name}\n{self.type_}\n{self.rarity}"

    def enumerate_rarity(self):
        """
        Function that enumerates item rarity

        Returns:
            int value: Enumerated item rarity
        """
        value = 0
        if self.rarity == "Common":
            value = 1
        elif self.rarity == "Uncommon":
            value = 2
        elif self.rarity == "Rare":
            value = 3
        elif self.rarity == "Epic":
            value = 4
        elif self.rarity == "Legendary":
            value = 5
        elif self.rarity == "Mythical":
            value = 6
        elif self.rarity == "Godly":
            value = 7
        else:
            value = 0
        return value


class ItemGenerator:
    """
    This class generates random item names. Does not take into account
    type of weapon.
    """

    def __init__(self, data_path):
        """
        The constructor for ItemGenerator

        Parameters:
            data_path (os.Path): Path to data folder
        """
        # Set the random seed
        random.seed(time.time())

        # Item dataclass
        self.item = Item()

        # Get all lists
        self.data_path = data_path
        self.weapon_fronts = self._get_weapon_front_list()
        self.armor_fronts = self._get_armor_front_list()
        self.boots_fronts = self._get_boots_front_list()
        self.helmet_fronts = self._get_helmet_front_list()
        self.necklace_fronts = self._get_necklace_front_list()
        self.item_names = self._get_item_names()

        # Pools and odds
        self.item_rarities = [
            "Common",
            "Uncommon",
            "Rare",
            "Epic",
            "Legendary",
            "Mythical",
            "Godly",
        ]
        self.item_rarity_rates = [
            0.559484,
            0.25,
            0.125,
            0.0625,
            0.003,
            0.000015,
            0.000001,
        ]
        self.item_types = ["Weapon", "Helmet", "Armor", "Boots", "Necklace"]

    def get_item(self, n_items):
        """
        This method n_items number of random items

        Parameters:
            n_items (int): Number of items to generate
        Returns:
            list[Item] item_list: list of randomly generated items
        """
        item_list = []
        for _ in range(n_items):
            # Roll the item type
            self.item.type_ = self.get_item_type()
            # Roll the item rarity
            self.item.rarity = self.get_item_rarity()
            # Get the item name
            self.item.name = self.get_item_name(self.item.type_)

            item_list.append(self.item)

        return item_list

    def get_item_name(self, item_t):
        """
        This method returns a random item name given the item type

        Parameters:
            item_t (str): Item type
        Returns:
            str: Item name
        """
        if item_t == "Weapon":
            item_name = (
                f"{choice(self.weapon_fronts)} {choice(self.item_names)}"
            )
        elif item_t == "Helmet":
            item_name = (
                f"{choice(self.helmet_fronts)} {choice(self.item_names)}"
            )
        elif item_t == "Armor":
            item_name = (
                f"{choice(self.armor_fronts)} {choice(self.item_names)}"
            )
        elif item_t == "Boots":
            item_name = (
                f"{choice(self.boots_fronts)} {choice(self.item_names)}"
            )
        elif item_t == "Necklace":
            item_name = (
                f"{choice(self.necklace_fronts)} {choice(self.item_names)}"
            )

        return item_name

    def get_item_rarity(self):
        """
        This method returns a random item rarity

        Returns:
            str: Item rarity from rarity list
        """
        item_rarity = choices(self.item_rarities, self.item_rarity_rates)
        return item_rarity[0]

    def get_item_type(self):
        """
        This method returns a random item type

        Returns:
            str: Item type from type list
        """
        item_type = choice(self.item_types)
        return item_type

    def _get_weapon_front_list(self):
        """
        This method returns a list of weapons descriptions that go before the name

        Returns:
            list: List of weapon descriptions
        """
        with open(os.path.join(self.data_path, "weapon_front.txt"), "r") as wf:
            weapon_fronts = wf.readlines()
            weapon_fronts = [x.strip() for x in weapon_fronts]

        return weapon_fronts

    def _get_helmet_front_list(self):
        """
        This method returns a list of helmet descriptions that go before the name

        Returns:
            list: List of helmet descriptions
        """
        with open(os.path.join(self.data_path, "helmet_front.txt"), "r") as hf:
            helmet_fronts = hf.readlines()
            helmet_fronts = [x.strip() for x in helmet_fronts]

        return helmet_fronts

    def _get_armor_front_list(self):
        """
        This method returns a list of armor descriptions that go before the name

        Returns:
            list: List of armor descriptions
        """
        with open(os.path.join(self.data_path, "armor_front.txt"), "r") as af:
            armor_fronts = af.readlines()
            armor_fronts = [x.strip() for x in armor_fronts]

        return armor_fronts

    def _get_boots_front_list(self):
        """
        This method returns a list of boots descriptions that go before the name

        Returns:
            list: List of boots descriptions
        """
        with open(os.path.join(self.data_path, "boots_front.txt"), "r") as bf:
            boots_fronts = bf.readlines()
            boots_fronts = [x.strip() for x in boots_fronts]

        return boots_fronts

    def _get_necklace_front_list(self):
        """
        This method returns a list of necklace descriptions that go before the name

        Returns:
            list: List of necklace descriptions
        """
        with open(
            os.path.join(self.data_path, "necklace_front.txt"), "r"
        ) as nf:
            necklace_fronts = nf.readlines()
            necklace_fronts = [x.strip() for x in necklace_fronts]

        return necklace_fronts

    def _get_item_names(self):
        """
        This method returns a list of names

        Returns:
            list: Names
        """
        with open(os.path.join(self.data_path, "names.txt"), "r") as n:
            names = n.readlines()
            names = [x.strip() for x in names]

        return names
