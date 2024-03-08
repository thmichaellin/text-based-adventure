from typing import Any, List
from room import Room


class History:
    """Class responsible for storing history of visited rooms"""

    def __init__(self) -> None:
        """Initialize a new History object with an empty list of rooms"""
        self.rooms: List[Room] = []

    def push(self, room: Any) -> None:
        """
        Add a room to the history

        pre: room is a room to be added to the history: a Room object
        """
        self.rooms.append(room)

    def pop(self) -> Room:
        """
        Remove and return the most recent room from the history

        post: Return the most recent room that was added to the history:
              a Room object.
        """
        return self.rooms.pop()
