from item import Item


def test_item_init():
    """Test initialization of the Item class"""

    name = "Flower"
    desc = "Dangerous looking flower"
    item = Item(name, desc)
    assert item.name == name
    assert item.desc == desc
