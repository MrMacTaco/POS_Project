class item:
    """ Item class holds info for each item in inventory
    """
    def __init__(self,isbn,name,price,quantity):
        self.isbn = isbn
        self.name = name
        self.price = price
        self.quantity = quantity

def priceToString(value):
    """ Converts from cents into a readable string
    """
    if len(str(value)) == 1:
           return "$0.0" + str(value)
    elif len(str(value)[:-2]) == 0:
            return "$0." + str(value)[-2:]
    else:
        return "$" + str(value)[:-2] + "." + str(value)[-2:]
