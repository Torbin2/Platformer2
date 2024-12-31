"""

P2L = Platformer 2 Level Format

The old one ™™ (with arbitery code execution 🤯💀):
    "-177;516": {"pos": [-177.0, 516.0], "type": "Type.BLOCK", "variant": 1},
    "144;-26": {"pos": [144, -26], "type": "Type.SPIKE_CUBE"},
    "102;26": {"pos": [102, 26], "type": "Type.BLOCK", "variant": 1},

The mew one v1.0

    x, y, type, properties

    x = 0x0000 ~ 0xFFFF (with negatives, -32767 ~ 32767)
    y = 0x0000 ~ 0xFFFF (with negatives, -32767 ~ 32767)
    type = 0x00 ~ 0xFF (0 ~ 127)
    properties (size depending on type)
        0 (SOLID_BLOCK) = 0x00 ~ 0xFF
        1 (SPIKE) = None
        2 (...)

    "102;26": {"pos": [102, 26], "type": "Type.BLOCK", "variant": 1} = 64 characters ->

    66 1A 00 01 (in hex) = 4 characters (16x compression)


The new one v1.1️±±±
    # index: type(properties)
    # Level:
    #     XXXXYYYY: index
    #     XXXX+DX;YYYY+DY;index
    #
    # Hex: XXXXYYYYTT
    #
    # shape types? (?)
    # 0 = blok?
    # 1 = vierkant



# https://en.wikipedia.org/wiki/Run-length_encoding

"""
