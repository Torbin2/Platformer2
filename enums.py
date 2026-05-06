from enum import Enum, auto


class BlockVariants(): #not an enum D:
    #where the surrounding blocks are = img_name - 1 (because zero-index)
    BOTTOM: int = 23 - 1
    LEFT: int = 35 - 1
    TOP: int = 31 - 1
    RIGHT: int = 27 - 1
    BOTTOMRIGHT: int = 5 - 1
    BOTTOMLEFT: int = 6 - 1
    TOPLEFT: int = 7 - 1
    TOPRIGHT: int = 8 - 1
    FREE: int = 9 - 1
    ALL: int = 10 - 1

    TOPLEFT_NO_OPPOSITE_CORNER : int = 11 - 1
    TOPRIGHT_NO_OPPOSITE_CORNER : int = 12 - 1
    BOTTOMRIGHT_NO_OPPOSITE_CORNER : int = 13 - 1
    BOTTOMLEFT_NO_OPPOSITE_CORNER : int = 14 - 1
    TOPRIGHTBOTTOMLEFT_NO_OPPOSITE_CORNER : int = 15 - 1
    TOPLEFTBOTTOMRIGHT_NO_OPPOSITE_CORNER: int  = 16 -1

    LEFTRIGHT: int = 17 - 1
    TOPBOTTOM: int = 18 - 1

    # TOP BOTTOM LEFT RIGHT
    BOTTOMRIGHT_CORNER: int = 19 - 1
    BOTTOMLEFT_CORNER: int = 20 - 1
    TOPLEFT_CORNER: int = 21 - 1
    TOPRIGHT_CORNER: int = 22 - 1

    BOTTOM_T: int = 24 - 1
    BOTTOM_T_BOTTOMLEFT: int = 25 - 1
    BOTTOM_T_BOTTOMRIGHT: int = 26 - 1
    BOTTOM_T_CORNERS: int = 1 - 1

    RIGHT_T: int = 28 - 1
    RIGHT_T_BOTTOMRIGHT: int = 29 - 1
    RIGHT_T_TOPRIGHT: int = 30 - 1
    RIGHT_T_CORNERS: int = 4 - 1

    TOP_T: int = 32 - 1
    TOP_T_TOPLEFT: int = 33 - 1
    TOP_T_TOPRIGHT: int = 34 - 1
    TOP_T_CORNERS: int = 3 - 1

    LEFT_T: int = 36 - 1
    LEFT_T_TOPLEFT: int = 37 - 1
    LEFT_T_BOTTOMLEFT: int = 38 - 1
    LEFT_T_CORNERS: int = 2 - 1

    PLUS: int = 39 - 1  # LEFT and TOP


class PlayerState(Enum):
    GROUNDED = auto()
    AIR = auto()


class Events(Enum):
    DEATH = auto()
    GET_CHECKPOINT = auto()
