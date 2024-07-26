import os  # noqa: F401
from collections import defaultdict


class CharacterDatabase:
    def __init__(self):
        self.characters = defaultdict(dict)

    def get_character_info(self, uid):
        print(self.characters.keys())
        
        if uid in self.characters.keys():
            return self.characters[uid]["info"]
        else:
            print(f"{uid} does not have a character")
            return -1

    def add_character(self, character):
        if character["uid"] in self.characters.keys():
            print("Character", character["uid"], " already added")
            return
        else:
            self.characters[character["uid"]] = {
                "info": character["info"],
                "inventory": character["inventory"],
            }
            print("Added " + str(self.characters))

    def add_buffer_event(self, uid, buffer_item):
        self.characters[str(uid)]["buffer"].append(buffer_item)

    def get_character_leaderboard():
        pass

    def flush_buffer():
        # Put items into inventory if any

        # Randomly allocate exp to stats

        # Include events that happened in character log

        pass
