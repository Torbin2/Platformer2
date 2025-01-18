from enum import Enum, auto, Flag

class Type(Flag):

    BLOCK = auto()
    SPIKE_SNAKE = auto()
    SPIKE_CUBE = auto()
    SPIKE_CIRCLE = auto()

    SPIKES = SPIKE_SNAKE | SPIKE_CUBE | SPIKE_CIRCLE

class BlockVariants(): #not a enum D:

    BOTTOM: int = 1 - 1
    LEFT: int = 2 - 1
    TOP: int = 3 - 1
    RIGHT: int = 4 - 1
    BOTTOMRIGHT: int = 5 - 1
    BOTTOMLEFT: int = 6 - 1
    TOPLEFT: int = 7 - 1
    TOPRIGHT: int = 8 - 1
    FREE: int = 9 - 1
    ALL: int = 10 - 1

    

class PlayerState(Enum):
    GROUNDED = auto()
    AIR = auto()

class Events(Enum):
    DEATH = auto()

class TileShapes(Enum):
    BLOCK = auto()
    CIRCLE = auto()
    SPIKE = auto()