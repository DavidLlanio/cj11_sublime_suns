from event_generator import EventGenerator
from item_generator import ItemGenerator


class Generator:
    """
    This class generates buffer items to be queued
    """

    def __init__(self, datapath):
        """
        The constructor for Generator class

        Parameters:
            data_path (os.Path): Path to data folder
        """
        # Composed of two other generators
        self.item_generator = ItemGenerator(data_path=datapath)
        self.event_generator = EventGenerator(data_path=datapath)

    def generate_buffer_item(self, n_items):
        """
        This method generates n_items of events, creates items based
        on winning events, then returns a dict with events and
        items generated, and also how much exp.

        Parameters:
            n_items (int): Number of events to generate
        Returns:
            dict: buffer item with events, items, and exp
        """
        event_buffer = list(str)
        item_buffer = list(str)
        exp = 0

        # Generate events
        for _ in range(0, n_items):
            event, points = self.event_generator.get_event()

            if points:
                exp += 1

            event_buffer.append(event)

        # For each winning event generate an item
        for _ in range(0, exp):
            item = self.item_generator.get_item()

            item_buffer.append(item)

        # Create dict representing buffer item
        buffer_item = {
            "events": event_buffer,
            "items": item_buffer,
            "exp": exp,
        }

        return buffer_item
