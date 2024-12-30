from enum import Enum, auto, Flag

class Type(Flag):

    BLOCK = auto()
    SPIKE_SNAKE = auto()
    SPIKE_CUBE = auto()
    SPIKE_CIRCLE = auto()

    SPIKES = SPIKE_SNAKE | SPIKE_CUBE | SPIKE_CIRCLE

class BlockVariants(Enum):
    TOP: int = 1
    RIGHT: int = 2
    BOTTOM: int = 3
    LEFT: int = 4
    TOPLEFT: int = 5
    TOPRIGHT: int = 6
    BOTTOMRIGHT: int = 7
    BOTTOMLEFT: int = 8
    FREE: int = 9
    ALL: int = 10

class PlayerState(Enum):
    GROUNDED = auto()
    AIR = auto()

class Events(Enum):
    DEATH = auto()

class TileShapes(Enum):
    BLOCK = auto()
    CIRCLE = auto()
    SPIKE = auto()