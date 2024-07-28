from .event_generator import Event, EventGenerator
from .item_generator import Item, ItemGenerator


class BufferItem:
    def __init__(self):
        self.events: list[Event] = []
        self.items: list[Item] = []


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
        event_list = self.event_generator.get_event(n_items)

        for event in event_list:
            if event.coins:
                win_count += 1

        event_list = [event.name for event in event_list]

        self.buffer_item.events.extend(event_list)

        # For each winning event generate an item
        item_list = self.item_generator.get_item(win_count)

        self.buffer_item.items.extend(item_list)

        return self.buffer_item

    def generate_items(self, n_items: int) -> list[Item]:
        """
        This method returns a list of n random Items

        Returns:
            list[Item]: List of Items
        """
        return self.item_generator.get_item(n_items)
