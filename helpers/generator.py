from .event_generator import Event, EventGenerator
from .item_generator import Item, ItemGenerator


class BufferItem:
    """Class for keeping track of events and items added to buffer"""

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

    def generate_buffer_item(self, n_items: int) -> BufferItem:
        """
        This method generates n_items of events, creates items based
        on winning events, then returns a dict with events and
        items generated

        Parameters:
            n_items (int): Number of events to generate
        Returns:
            BufferItem: buffer item with events and items
        """
        buffer_item = BufferItem()
        win_count: int = 0

        # Generate events
        event_list = self.event_generator.get_event(n_items)

        # Count number of wins
        for event in event_list:
            if event.coins:
                win_count += 1

        # Get event names and add to buffer item
        event_names = [event.name for event in event_list]
        buffer_item.events.extend(event_names)

        # For each winning event generate an item
        item_list = self.item_generator.get_item(win_count)

        buffer_item.items.extend(item_list)

        return buffer_item

    def generate_items(self, n_items: int) -> list[Item]:
        """
        This method returns a list of n random Items

        Returns:
            list[Item]: List of Items
        """
        return self.item_generator.get_item(n_items)
