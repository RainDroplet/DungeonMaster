class Item:
    def __init__(self, name, craft_mat, coin_value, quantity, flavor_text):
        self.name = name
        self.craft_mat = craft_mat
        self.coin_value = coin_value
        self.quantity = quantity
        self.flavor_text = flavor_text

    def get_name(self):
        return self.name

    def get_craft_mat(self):
        return self.craft_mat

    def get_coin_value(self):
        return self.coin_value

    def get_quantity(self):
        return self.quantity

    def get_flavor_text(self):
        return self.flavor_text

    def change_quantity(self, change_value):
        self.quantity = self.quantity + change_value
        if self.quantity <= 0:
            self.quantity = 0
        return self.quantity


itemIndex = {
    0: Item('Diamond', False, 10, 1, 'Looks like it\'s only good for selling!'),
    1: Item('Apple', False, 5, 1, 'It\'s a god damn apple'),
    2: Item('Bone', True, 2, 1, 'A bone from the Skelington!')
}


def get_item(key):
    try:
        return itemIndex[key]
    except IndexError:
        pass
