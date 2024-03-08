from typing import Dict, Optional, List
from item import Item


class Room:
    """Class representing a room in the game"""

    def __init__(self, room_id: int, name: str, desc: str) -> None:
        """
        Initialize the Room class

        pre: room_id is the ID of the room: an int,
             name is the name of the room: a str,
             desc is the description of the room: a str
        """

        self.room_id = room_id
        self.name = name
        self.desc = desc
        self.connections: Dict[str, Room] = {}
        self.cond_connections: Dict[str, List[Dict[str, str]]] = {}
        self.items: List[Item] = []
        self.visited = False

    def add_connection(self, direction: str, room: 'Room') -> None:
        """
        Add a connection to another room

        pre: direction is the direction of the connection: a str,
             room is the connecting room: a Room object
        """

        self.connections[direction] = room

    def add_cond_connection(self, item: str, direction: str, room: str) -> \
            None:
        """
        Add a conditional connection to another room based on an item

        pre: item is the name of item required for connection: a str,
             direction is the direction of the connection: a str,
             room is the name of the room: a Room object
        """

        try:
            self.cond_connections[item].append({direction: room})
        except KeyError:
            self.cond_connections[item] = []
            self.cond_connections[item].append({direction: room})

    def add_item(self, item: Item) -> None:
        """
        Add an item to the room

        pre: item is the item to be added to the room: an Item object
        """

        self.items.append(item)

    def has_connection(self, direction: str) -> bool:
        """
        Check if the room has a connection in a given direction

        pre: direction is the direction of a connection: a str
        post: Return True if connection exists, else False
        """

        return direction in self.connections

    def get_connection(self, direction: str) -> Optional['Room']:
        """
        Get the connected room in a given direction

        pre: direction is the direction of a connection: a str
        post: Return the connected room: a Room object, or None if there is no
              connection
        """

        return self.connections.get(direction)

    def set_visited(self) -> None:
        """Set the visited flag of a room. Default is True"""

        self.visited = True

    def is_visited(self) -> bool:
        """
        Check if the room has been visited

        post: Return True if room has been visited, else False
        """

        return self.visited
