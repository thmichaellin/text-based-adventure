from room import Room
from item import Item


def test_room_init():
    """Test initialization of the Room class"""

    room = Room(1, "Living Room", "Room for living")
    assert room.room_id == 1
    assert room.name == "Living Room"
    assert room.desc == "Room for living"
    assert len(room.connections) == 0
    assert len(room.cond_connections) == 0
    assert len(room.items) == 0
    assert not room.is_visited()


def test_room_add_connection():
    """Test adding connections to room"""

    room1 = Room(1, "Living Room", "Room for living")
    room2 = Room(2, "Kitchen", "Room for kitching")
    room1.add_connection("EAST", room2)
    assert "EAST" in room1.connections
    assert room1.connections["EAST"] == room2


def test_room_add_cond_connection():
    """Test adding conditional connections to room"""

    room1 = Room(1, "Living Room", "Room for living")
    room2 = "Bedroom"
    item = "Key"
    room1.add_cond_connection(item, "NORTH", room2)
    assert item in room1.cond_connections
    assert len(room1.cond_connections[item]) == 1
    assert room1.cond_connections[item][0] == {"NORTH": room2}


def test_room_add_item():
    """Test adding items to room"""

    room = Room(1, "Living Room", "Room for living")
    item = Item("Book", "Book for reading")
    room.add_item(item)
    assert len(room.items) == 1
    assert room.items[0] == item


def test_room_has_connection():
    """Test if the room has a connection"""

    room1 = Room(1, "Living Room", "Room for living")
    room2 = Room(2, "Kitchen", "Room for kitching")
    room1.add_connection("EAST", room2)
    assert room1.has_connection("EAST")
    assert not room1.has_connection("WEST")


def test_room_get_connection():
    """Test getting connected room"""

    room1 = Room(1, "Living Room", "Room for living")
    room2 = Room(2, "Kitchen", "Room for kitching")
    room1.add_connection("EAST", room2)
    assert room1.get_connection("EAST") == room2
    assert room1.get_connection("WEST") is None


def test_room_visited():
    """Test setting and checking if the room has been visited"""

    room = Room(1, "Living Room", "Room for living")
    assert not room.is_visited()
    room.set_visited()
    assert room.is_visited()
