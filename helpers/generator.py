from dataclasses import dataclass

from event_generator import Event, EventGenerator
from item_generator import Item, ItemGenerator


@dataclass
class BufferItem:
    events: list[Event] = []
    items: list[Item] = []


class Generator:
    """
    This class generates buffer items to be queued
    """

    def __init__(self, datapath) -> None:
        """
        The constructor for Generator class

        Parameters:
            data_path (str): Path to data folder
        """
        # Composed of two other generators
        self.item_generator = ItemGenerator(data_path=datapath)
        self.event_generator = EventGenerator(data_path=datapath)

        # Crete buffer item
        self.buffer_item = BufferItem()

    def generate_buffer_item(self, n_items: int) -> BufferItem:
        """
        This method generates n_items of events, creates items based
        on winning events, then returns a dict with events and
        items generated, and also how much exp.

        Parameters:
            n_items (int): Number of events to generate
        Returns:
            BufferItem: buffer item with events and items
        """
        win_count: int = 0

        # Generate events
        for _ in range(n_items):
            event = self.event_generator.get_event()

            if event.coins:
                win_count += 1

            self.buffer_item.events.append(event)

        # For each winning event generate an item
        for _ in range(win_count):
            item = self.item_generator.get_item()

            self.buffer_item.items.append(item)

        return self.buffer_item

    def generate_items(self, n_tems: int) -> list[Item]:
        """
        This method returns a list of n random Items

        Returns:
            list[Item]: List of Items
        """
        items: list[Item] = []

        for _ in range(n_tems):
            new_item = self.item_generator.get_item()
            items.append(new_item)

        return items
