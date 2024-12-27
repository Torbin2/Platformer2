from enum import Enum, auto, Flag

class Type(Flag):
    BLOCK = auto()
    SPIKE_SNAKE = auto()
    SPIKE_CUBE = auto()
    SPIKE_CIRCLE = auto()

    SPIKES = SPIKE_SNAKE | SPIKE_CUBE | SPIKE_CIRCLE

class BlockVariants(Enum):
    TOP:str = "1"
    RIGHT:str = "2"
    BOTTOM:str = "3"
    LEFT:str = "4"
    TOPLEFT:str = "5"
    TOPRIGHT:str = "6"
    BOTTOMRIGHT:str = "7"
    BOTTOMLEFT:str = "8"
    FREE:str = "9"
    ALL :str= "10"

class PlayerState(Enum):
    GROUNDED = auto()
    AIR = auto()
