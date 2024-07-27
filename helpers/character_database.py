import os
import pickle
from collections import defaultdict

from helpers.character import Character


class CharacterDatabase:
    """
    This class manages the character database
    """

    def __init__(self, data_path):
        """
        The constructor for CharacterDatabase class

        Parameters:
            data_path (str): Path to data folder
        """
        self.db_path = os.path.join(data_path, "database.pkl")
        self.characters: defaultdict[int:Character] = self._load_database()

    def add_character(self, uid, character: Character):
        """
        This method adds a character to the associtated user id
        in the database

        Parameters:
            uid (int): user id
            character (Character): character object
        Returns:
            int: Returns 0 if uid already has a character
        """
        if uid in self.characters.keys():
            return -1
        else:
            self.characters[uid] = character
            self.cache_database()
            return 0

    def get_character_info(self, uid):
        """
        This method gets the character from the database

        Parameters:
            uid (int): user id
            character (Character): character object
        Returns:
            int: Returns -1 if uid already has a character
            or
            Character: Character object
        """
        if uid in self.characters.keys():
            return self.characters[uid]
        else:
            return -1

    def add_buffer_event(self, uid, buffer_item):
        """
        This method adds to the buffer of character in database

        Parameters:
            uid (int): user id
            buffer_item (BufferItem): BufferItem from generator
        Returns:
            int: Returns -1 if uid doesn't have a character
        """
        if uid in self.characters.keys():
            self.characters[uid].buffer.append(buffer_item)
            return 0
        else:
            return -1

    def get_character_leaderboard(self):
        """
        This method gets the top 20 characters in descending order of ranking points

        Returns:
            list: Sorted list of characters
        """
        leaderboard = sorted(
            self.characters.values(),
            key=lambda char: char.ranking_points,
            reverse=True,
        )
        return leaderboard[:20]

    def flush_buffer(self, uid):
        """
        This method flushes the buffer and adds all the
        events to quest log and items to character inventory

        Parameters:
            uid (int): user id
        Returns:
            int: Returns -1 if uid doesn't have a character
        """
        if uid in self.characters.keys():
            current_character = self.characters[uid]
        else:
            return -1

        for b_item in current_character.buffer:
            # Put items into inventory if any
            current_character.inventory.extend(b_item.items)
            # Add all events to the quest log
            current_character.quest_log.extend(b_item.events.name)

        # Equip best in slot items
        current_character.equip_best()
        current_character.buffer = []

        # Save the changes
        self.characters[uid] = current_character

        # Cache database just in case
        self.cache_database()
        return 0

    def cache_database(self):
        """
        This method saves the database to the file
        """
        with open(self.db_path, "wb") as db:
            pickle.dump(self.characters, db)

    def _load_database(self):
        """
        This method loads the database from the file
        """
        with open(self.db_path, "wb") as db:
            self.characters = pickle.load(db)
