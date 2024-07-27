import os
import pickle
from collections import defaultdict
from datetime import datetime

from helpers.character import Character
from helpers.generator import Generator


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
        self.generator = Generator(data_path)

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

    def character_checkin(self, uid):
        """
        This method fills the character buffer with latest buffer item and flushes it

        Parameters:
            uid (int): user id
        Returns:
            int: Returns -1 if uid doesn't have a character
        """
        if uid in self.characters.keys():
            current_character = self.characters[uid]
        else:
            return -1

        current_character = self.fill_buffer(current_character)
        current_character = self.flush_buffer(current_character)

        # Save the current character in active database
        self.characters[uid] = current_character

        # Cache the database
        self.cache_database()
        return 0

    def fill_buffer(self, current_character):
        """
        This method fills the character buffer with buffer items based on last checkin time

        Parameters:
            current_character (Character): Character of user calling
        """
        # Calculate how many minutes since last checkin
        now = datetime.now()
        time_diff = now - current_character.last_checkin
        minutes = int(time_diff.total_seconds() // 60)

        buffer_item = self.generator.generate_buffer_item(minutes)

        current_character.last_checkin = now

        current_character.buffer.append(buffer_item)
        return current_character

    def flush_buffer(self, current_character):
        """
        This method flushes the buffer and adds all the
        events to quest log and items to character inventory

        Parameters:
            current_character (Character): Character of user calling
        """
        for b_item in current_character.buffer:
            # Put items into inventory if any
            current_character.inventory.extend(b_item.items)
            # Add all events to the quest log
            for event in b_item.events:
                current_character.quest_log.append(event.name)

        # Equip best in slot items
        current_character.equip_best()
        current_character.buffer = []

        return current_character

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
        if os.path.exists(self.db_path):
            with open(self.db_path, "rb") as db:
                database = pickle.load(db)
        else:
            database = {}

        return database
