from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class UserRoles(BaseEnum):
    staff = 'Staff'
    buyer = 'Buyer'
    dealership = 'Dealership'
    supplier = 'Supplier'
    unknown = 'Unknown'


class Engine(BaseEnum):
    gas = 'Gas'
    diesel = 'Diesel'
    electric = 'Electric'


class Transmission(BaseEnum):
    at = 'Automatic Transmission'
    mt = 'Manual Transmission'
    am = 'Automated Manual Transmission'


class Color(BaseEnum):
    green = 'Green'
    yellow = 'Yellow'
    red = 'Red'
    blue = 'Blue'
    pink = 'Pink'
    grey = 'Grey'
    orange = 'Orange'
    gold = 'Gold'
    silver = 'Silver'
    black = 'Black'


class OfferStatus(BaseEnum):
    close = 'Closed success!'
    open = 'Still open...'
