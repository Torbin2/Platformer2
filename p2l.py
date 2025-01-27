"""

P2L = Platformer 2 Level Format

The old one ™™ (with arbitery code execution 🤯💀):
    "-177;516": {"pos": [-177.0, 516.0], "type": "Type.BLOCK", "variant": 1},
    "144;-26": {"pos": [144, -26], "type": "Type.SPIKE_CUBE"},
    "102;26": {"pos": [102, 26], "type": "Type.BLOCK", "variant": 1},

The mew one v1.0

    len, x, y, type, properties

    len = 0x00 ~ 0xFF (0 ~ 127)
    x = 0x0000 ~ 0xFFFF (with negatives, -32767 ~ 32767)
    y = 0x0000 ~ 0xFFFF (with negatives, -32767 ~ 32767)
    type = 0x00 ~ 0xFF (0 ~ 127)
    properties (size depending on type)
        0 (SOLID_BLOCK) = 0x00 ~ 0xFF
        1 (SPIKE) = None
        2 (...)

    "102;26": {"pos": [102, 26], "type": "Type.BLOCK", "variant": 1} = 64 characters ->

    06 00 66 00 1A 00 01 (in hex) = 7 characters (10.6x compression)


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
from __future__ import annotations

import os
import json
import typing

import levelmap

LEVELS_DIR = 'levels'


class LevelStore:
    _magic = b'p2l v1.2'

    def __init__(self, level_name: str):
        self._level_name = level_name
        self._level_path = os.path.join(LEVELS_DIR, self._level_name + '.p2l')
        print('level_path:', self._level_path)

        self._tiles: dict[tuple[int, int], levelmap.Tile] = {}

        self._chunk_size = 256

    def save(self, tilemap: 'levelmap.TileMap2') -> None:
        # dict[tile_params: str::json, index: int]
        tile_to_index: dict[str, int] = {}
        current_index = 1  # The first index is air

        # dict[chunk_pos, dict[chunk_mod_pos, tile_index]]
        chunks: dict[tuple[int, int], dict[tuple[int, int], int]] = {}
        for x, y in self._tiles:
            cx = x // self._chunk_size
            cy = y // self._chunk_size

            if (cx, cy) not in chunks:
                chunks[(cx, cy)] = {}

            tile = self._tiles[(x, y)]
            params = json.dumps(self._serialise_tile(tile))

            if params in tile_to_index:
                index = tile_to_index[params]
            else:
                index = current_index
                tile_to_index[params] = index
                current_index += 1

            chunks[(cx, cy)][(x % self._chunk_size, y % self._chunk_size)] = index

        index_to_tile: dict[int, str] = {v: k for k, v in tile_to_index.items()}
        with open(self._level_path, 'wb') as file:
            def write_str(s: str) -> None:
                s = s.encode('utf-8')
                file.write(len(s).to_bytes(4))
                file.write(s)

            file.write(self._magic)

            # TODO: Implement the ability to use more than 2**16 different tiles
            file.write(len(index_to_tile).to_bytes(2))
            for index in index_to_tile:
                write_str(index_to_tile[index])

            for chunk_pos, chunk in chunks.items():
                file.write(b'\x01')
                file.write(chunk_pos[0].to_bytes(4, signed=True))
                file.write(chunk_pos[1].to_bytes(4, signed=True))

                last: int | None = None
                length = 0
                for y in range(self._chunk_size):
                    for x in range(self._chunk_size):
                        index: int = chunk.get((x, y), 0)
                        if last is not None and last != index:
                            if length != 0:
                                file.write((1 << 7).to_bytes(1))
                                file.write(length.to_bytes(2))
                            length = 0
                            last = None

                        if last is None:
                            file.write((0).to_bytes(1))
                            file.write(index.to_bytes(2))
                            last = index

                        elif last == index:
                            length += 1
                if length != 0:
                    assert last is not None
                    file.write((1 << 7).to_bytes(1))
                    file.write(length.to_bytes(2))

            file.write(b'\x00')  # EOF marker

    @staticmethod
    def _serialise_tile(tile: 'levelmap.Tile') -> dict[str, str]:
        return {
            'type': tile.type_name,
            'tile': tile.serialise(),
            'renderer': tile.renderer.serialise(),
            'collider': tile.collider.serialise()
        }

    def load(self, tilemap: 'levelmap.TileMap2') -> None:
        self._tiles = {}
        if not os.path.exists(self._level_path):
            print('Level not found, creating a new, empty level')
            return

        with open(self._level_path, 'rb') as file:
            if file.read(len(self._magic)) != self._magic:
                raise ValueError(f'File {self._level_path} is not a valid p2l file')

            def read_str() -> str:
                length = int.from_bytes(file.read(4))
                return file.read(length).decode('utf-8')

            # Load int to Tile here
            index_to_tile: dict[int, dict[str, typing.Any]] = {}
            for index in range(1, int.from_bytes(file.read(2)) + 1):
                params = json.loads(read_str())
                index_to_tile[index] = params

            def create_tile_from_params(x: int, y: int, params: dict[str, str | dict]):
                f = tilemap.get_tile_factory(params['type'])
                f.add_type(None, None, params['tile'])
                f.add_renderer(None, None, params['renderer'])
                f.add_collider(None, None, params['collider'])
                return f.create(x, y)

            def create_tile_from_index(index: int, x: int, y: int) -> levelmap.Tile:
                params = index_to_tile[index]
                return create_tile_from_params(x, y, params)

            while (marker := file.read(1)) == b'\x01':
                chunk_x = int.from_bytes(file.read(4), signed=True)
                chunk_y = int.from_bytes(file.read(4), signed=True)

                last_value: int | None = None

                x: int = 0
                y: int = 0

                def next_xy() -> tuple[int, int]:
                    nonlocal x, y
                    old_x, old_y = x, y
                    x += 1
                    if x >= self._chunk_size:
                        x = 0
                        y += 1
                    return old_x, old_y

                def calc_pos() -> tuple[int, int]:
                    return x + chunk_x * self._chunk_size, y + chunk_y * self._chunk_size

                while y < self._chunk_size:
                    type_ = int.from_bytes(file.read(1))
                    if type_ >> 7 == 0:  # Value
                        if (type_ >> 6) & 1 == 0:  # Int
                            value = int.from_bytes(file.read(2))
                            if value != 0:
                                self._tiles[calc_pos()] = create_tile_from_index(value, *calc_pos())
                            next_xy()
                            last_value = value
                        elif (type_ >> 6) & 1 == 1:  # Tile
                            last_value = None
                            params = json.loads(read_str())
                            self._tiles[calc_pos()] = create_tile_from_params(*calc_pos(), params)
                            next_xy()
                        else:
                            raise NotImplementedError(f'Tile value with type {bin(type_)}')

                    elif type_ >> 7 == 1:  # Repeat
                        if last_value is None:
                            raise ValueError()

                        count = int.from_bytes(file.read(2))
                        for _ in range(count):
                            if last_value != 0:
                                self._tiles[calc_pos()] = create_tile_from_index(last_value, *calc_pos())
                            next_xy()

                    else:
                        raise NotImplementedError(f'Type {bin(type_)}')

                if x != 0 or y != self._chunk_size:
                    raise ValueError(f'The loaded chunk is not the right size (Final x: {x} and y: {y})')

            if marker != b'\x00':
                raise ValueError(f'Expected end marker, got {marker}')

    def get(self, x: int, y: int) -> 'levelmap.Tile' | None:
        if type(x) is not int:
            raise ValueError()
        if type(y) is not int:
            raise ValueError()

        if (x, y) in self._tiles:
            return self._tiles[(x, y)]
        else:
            return None

    def set(self, x: int, y: int, value: 'levelmap.Tile' | None) -> None:
        if type(x) is not int:
            raise ValueError()
        if type(y) is not int:
            raise ValueError()

        if value is None:
            if (x, y) in self._tiles:
                self._tiles.pop((x, y))
        else:
            self._tiles[(x, y)] = value
