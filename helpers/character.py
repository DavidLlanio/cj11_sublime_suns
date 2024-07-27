from dataclasses import dataclass

from generator import BufferItem
from item_generator import Item


@dataclass
class Character:
    """Class for keeping track of character information"""

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
