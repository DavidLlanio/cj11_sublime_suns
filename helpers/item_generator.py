import os
from random import choice, choices


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
        self.data_path = data_path
        self.weapon_fronts = self._get_weapon_front_list()
        self.weapon_names = self._get_weapon_names()
        self.weapon_rarities = ["Common", "Uncommon", "Rare",\
                                 "Epic", "Legendary", "Mythical", "Godly"]
        self.weapon_mult = {
            "Common": {
                "mult": 1,
            },
            "Uncommon": {
                "mult": 1,
            },
            "Rare": {
                "mult": 1,
            },
            "Epic": {
                "mult": 1,
            },
            "Legendary": {
                "mult": 1,
            },
            "Mythical": {
                "mult": 1,
            },
            "Godly": {
                "mult": 1,
            },
        }
        self.weapon_rates = [0.559484, 0.25, 0.125, 0.0625, 0.003, 0.000015, 0.000001]


    def get_item(self):
        """
        This method returns a random item name

        Returns:
            str: Random item name
        """
        return f"{choice(self.weapon_fronts)}{choice(self.weapon_names)}"

    def _get_weapon_front_list(self):
        """
        This method returns a list of weapons descriptions that go before the name

        Returns:
            list: List of weapon descriptions
        """
        with open(os.path.join(self.data_path, "weapon_front.txt"), "r") as wf:
            weapon_fronts = wf.readlines()
            weapon_fronts = [x.replace("\n", "") for x in weapon_fronts]

        return weapon_fronts

    def _get_weapon_names(self):
        """
        This method returns a list of weapon names

        Returns:
            list: Weapon names
        """
        with open(os.path.join(self.data_path, "names.txt"), "r") as n:
            names = n.readlines()
            names = [x.replace("\n", "") for x in names]

        return names
