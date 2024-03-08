class Item:
    """Class representing an item in the game"""

    def __init__(self, name: str, desc: str) -> None:
        """
        Initialize a new Item object with a name and description

        pre: name is the name of the item: a str, desc is the description of
             the item: a str

        """

        self.name = name
        self.desc = desc
