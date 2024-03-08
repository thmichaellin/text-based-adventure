from room import Room, List
from history import History


def test_history_init():
    """Test initialization of the History class"""
    history = History()
    assert isinstance(history.rooms, List)


def test_history_push_and_pop():
    """Test the push() and pop() methods of the History class"""
    history = History()
    room1 = Room(1, "Living Room", "Room for living")
    room2 = Room(2, "Kitchen", "Room for cooking")

    history.push(room1)
    assert len(history.rooms) == 1
    assert history.rooms[0] == room1

    history.push(room2)
    assert len(history.rooms) == 2
    assert history.rooms[1] == room2

    popped_room = history.pop()
    assert popped_room == room2
    assert len(history.rooms) == 1
    assert history.rooms[0] == room1

    popped_room = history.pop()
    assert popped_room == room1
    assert len(history.rooms) == 0
