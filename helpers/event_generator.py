import os
from random import choice, choices


class EventGenerator:
    """
    This class generates random events
    """

    def __init__(self, data_path) -> None:
        """
        The constructor for EventGenerator

        Parameters:
            data_path (os.Path): Path to data folder
        """
        self.data_path = data_path
        self.location_front = self._get_location_front_list()
        self.generic_names = self._get_generic_names()
        self.city_names = self._get_city_names()
        self.visiting_verbs = self._get_visitng_verbs()
        self.winning_verbs = self._get_winning_verbs()

    def get_event(self):
        """
        This method returns a random event and bool if it is a winning event
        30% chance of being a winning event

        Returns:
            str event: Event name
            bool points: True if winning event, False if not winning event
        """
        event_type = ["visiting", "winning"]
        event_odds = [0.7, 0.3]
        event_type = choices(event_type, event_odds)

        if event_type == "visiting":
            event = f"{choice(self.visiting_verbs)} the city of {choice(self.city_names)}"
            points = False
        elif event_type == "winning":
            event = f"{choice(self.winning_verbs)}{choice(self.location_front)}{choice(self.generic_names)}"
            points = True

        return event, points

    def _get_location_front_list(self):
        """
        This method returns a list of location descriptions that go before the name

        Returns:
            list: List of location descriptions
        """
        with open(
            os.path.join(self.data_path, "locaiton_front.txt"), "r"
        ) as f:
            location_fronts = f.readlines()
            location_fronts = [x.replace("\n", "") for x in location_fronts]

        return location_fronts

    def _get_generic_names(self):
        """
        This method returns a list of generic names

        Returns:
            list: Weapon names
        """
        with open(os.path.join(self.data_path, "names.txt"), "r") as n:
            names = n.readlines()
            names = [x.replace("\n", "") for x in names]

        return names

    def _get_city_names(self):
        """
        This method returns a list of city names

        Returns:
            list: Weapon names
        """
        with open(os.path.join(self.data_path, "city_names.txt"), "r") as c:
            city_names = c.readlines()
            city_names = [x.replace("\n", "") for x in city_names]

        return city_names

    def _get_visitng_verbs(self):
        """
        This method returns a list of visiting verbs

        Returns:
            list: Visiting words
        """
        with open(
            os.path.join(self.data_path, "visiting_actions.txt"), "r"
        ) as v:
            visit = v.readlines()
            visit = [x.replace("\n", "") for x in visit]

        return visit

    def _get_winning_verbs(self):
        """
        This method returns a list of winning verbs

        Returns:
            list: Winning words
        """
        with open(
            os.path.join(self.data_path, "winning_actions.txt"), "r"
        ) as w:
            win = w.readlines()
            win = [x.replace("\n", "") for x in win]

        return win
