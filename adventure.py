from room import Room
from item import Item
from history import History
from typing import Dict, List


class Adventure:
    """Class representing the text-based adventure game"""

    # Create rooms and items for the appropriate 'game' version.
    def __init__(self, game: str) -> None:
        """
        Initialize the Adventure class

        pre: game is the name of a game file: a str
        """

        # Dictionary to store rooms
        self.rooms: Dict[int, Room] = {}

        # Dictionary to store synonyms
        self.synonyms: Dict[str, str] = {}

        # List to store inventory items
        self.inventory: List[Item] = []

        # Load room structures
        self.load_rooms(f"data/{game}Adv.dat")

        self.load_synonyms()

        # Game always starts in room number 1, so we'll set it after loading
        assert 1 in self.rooms, "First room not found."
        self.current_room: Room = self.rooms[1]

    def load_rooms(self, filename: str) -> None:
        """
        Load rooms and items from file

        pre: filename is the path to the game: a str
        """

        with open(filename) as f:

            # Load rooms
            while True:
                line: str = f.readline().strip()
                if not len(line):
                    break
                room_data = line.split("\t")
                self.rooms[int(room_data[0])] = Room(int(room_data[0]),
                                                     room_data[1],
                                                     room_data[2])

            # Load connections between rooms
            while True:
                line = f.readline().strip()
                if not len(line):
                    break
                connection_data = line.split("\t")
                for i in range(1, len(connection_data), 2):
                    source_room = self.rooms[int(connection_data[0])]
                    try:
                        destination_room: Room = self.rooms[
                            int(connection_data[i + 1])]
                        source_room.add_connection(connection_data[i],
                                                   destination_room)
                    except ValueError:
                        conditional_line = connection_data[i + 1].split("/")
                        conditional_item = conditional_line[1]
                        cond_destination_room: str = conditional_line[0]
                        source_room.add_cond_connection(conditional_item,
                                                        connection_data[i],
                                                        cond_destination_room)

            # Load items in rooms
            while True:
                line = f.readline().strip()
                if not len(line):
                    break
                item_data = line.split("\t")
                for i in range(1, len(item_data), 2):
                    item: Item = Item(item_data[0], item_data[1])
                    self.rooms[int(item_data[2])].add_item(item)

    def load_synonyms(self) -> None:
        """Load synonyms from a file"""
        synonyms = "Synonyms"
        with open(f"data/{synonyms}.dat") as f:
            while True:
                line = f.readline().strip()
                if len(line) == 0:
                    break
                synonym_data = line.split("=")
                self.synonyms[synonym_data[0]] = synonym_data[1]

    def get_description(self) -> str:
        """
        Return the long or short description of the current room.

        post: Return the name of the room if visited or description of room if
              not: a str
        """

        if self.current_room.is_visited():
            return self.current_room.name
        self.current_room.set_visited()
        return self.current_room.desc

    def get_long_description(self) -> str:
        """
        Return the long description of the current room.

        post: Return the long description of the room: a str
        """
        return self.current_room.desc

    def move(self, direction: str, history: History) -> bool:
        """
        Move to a different room based on the given direction

        pre: direction is a direction to move toward: a str and history is
             a stack holding previous rooms: a History object
        post: Return True if move was successful, else False: a bool
        """
        if self.conditional_move(direction, history):
            return True

        if self.current_room.has_connection(direction):
            if direction == "FORCED":
                self.current_room = self.current_room.get_connection(direction)
            else:
                history.push(self.current_room)
                self.current_room = self.current_room.get_connection(direction)
            return True

        return False

    def conditional_move(self, direction: str, history: History) -> bool:
        """
        Move to a different room based on conditional connections

        pre: direction is a direction to move toward: a str and history is
             a stack holding previous rooms: a History object
        post: Return True if move was successful, else False: a bool
        """

        for item in self.inventory:
            if item.name in self.current_room.cond_connections:
                for movement in self.current_room.cond_connections[item.name]:
                    try:
                        previous_room = self.current_room
                        self.current_room = self.rooms[
                            int(movement[direction])]
                        history.push(previous_room)
                        return True
                    except KeyError:
                        break
        return False

    def is_forced(self) -> bool:
        """
        Check if the current room has a forced connection.

        post: Returns True if forced connection is present, else False: a bool
        """

        return "FORCED" in self.current_room.connections

    def take(self, item: str) -> str:
        """
        Take an item from the current room and add it to the inventory

        pre: item is an item in the current room: a str
        post: Return a message indicating the results of the operation: a str
        """

        for room_item in self.current_room.items:
            if room_item.name == item:
                self.inventory.append(room_item)
                self.current_room.items.remove(room_item)
                return item + " taken."
        return "No such item."

    def drop(self, item: str) -> str:
        """
        Drop an item from the inventory and add it to the current room

        pre: item is an item in the current room: a str
        post: Return a message indicating the results of the operation: a str
        """

        for inventory_item in self.inventory:
            if inventory_item.name == item:
                self.current_room.items.append(inventory_item)
                self.inventory.remove(inventory_item)
                return item + " dropped."
        return "No such item."

    def help(self) -> str:
        """
        Return the help text

        post: Return the help text: a str
        """

        help_text = "You can move by typing directions such as " \
                    "EAST/WEST/IN/OUT\n" \
                    "QUIT quits the game.\n" \
                    "HELP prints instructions for the game.\n" \
                    "INVENTORY lists the item in your inventory.\n" \
                    "LOOK lists the complete description of the room " \
                    "and its contents.\n" \
                    "TAKE <item> take item from the room.\n" \
                    "DROP <item> drop item from your inventory.\n"
        return help_text


def init_game() -> 'Adventure':
    """
    Initialize the game by loading the requested game or default game.

    post: Return a game instance: an Adventure object.
    """

    from sys import argv

    # Check command line arguments
    if len(argv) not in [1, 2]:
        print("Usage: python adventure.py [name]")
        exit(1)

    # Load the requested game or else Tiny
    if len(argv) == 1:
        game_name = "Tiny"
    elif len(argv) == 2:
        game_name = argv[1]

    # Create game
    return Adventure(game_name)


def play_game(adventure: 'Adventure') -> None:
    """
    Game logic for playing the provided adventure.

    post: Display the welcome message: a str.
          Display description of initial room: a str.
          Process user commands, update game state, and display relevant
          message.
    """

    # Welcome user
    print("Welcome to Adventure.\n")

    # Print very first room description
    print(adventure.get_description())

    # Initialize game history
    history = History()

    # Prompt the user for commands until they type QUIT
    while True:

        if adventure.is_forced():
            adventure.move("FORCED", history)
            print(adventure.get_description())
            continue

        # Prompt
        command = input("> ").upper()

        if command in adventure.synonyms:
            command = adventure.synonyms[command]

        # Help text
        if command == "HELP":
            print(adventure.help())
            continue

        # Long description
        if command == "LOOK":
            print(adventure.get_long_description())
            for item in adventure.current_room.items:
                print(item.name + ": " + item.desc)
            continue

        # Go back
        if command == "BACK":
            try:
                adventure.current_room = history.pop()
                print(adventure.get_description())
            except IndexError:
                print("Can't go back.")
            continue

        # Take item
        if "TAKE" in command:
            if len(command.split()) == 2:
                command = command.split(" ")
                print(adventure.take(command[1]))
            else:
                print("No such item.")
            continue

        # Drop item
        if "DROP" in command:
            if len(command.split()) == 2:
                command = command.split(" ")
                print(adventure.drop(command[1]))
            else:
                print("No such item.")
            continue

        # Inventory
        if command == "INVENTORY":
            if not adventure.inventory:
                print("Your inventory is empty.")
                continue
            for item in adventure.inventory:
                print(item.name + ": " + item.desc)
            continue

        # Escape route
        if command == "QUIT":
            break

        # Perform move or other command
        if not adventure.move(command, history):
            print("Invalid command.")
            continue

        print(adventure.get_description())
        for item in adventure.current_room.items:
            print(item.name + ": " + item.desc)


if __name__ == "__main__":
    adventure = init_game()
    play_game(adventure)
