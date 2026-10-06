import dataclasses
import time
import typing
if typing.TYPE_CHECKING:
    import levelmap

import pygame
import pygame.gfxdraw

import p2l


@dataclasses.dataclass
class Chunk:
    # In chunk coordinates
    points: list[tuple[pygame.Surface, pygame.Rect, list[tuple[int, int]]]]
    # In chunk coordinates
    other_tiles: list[tuple[int, int]]


    @staticmethod
    def generate_bounding_box(points: list[tuple[int, int]]) -> pygame.Rect:
        x_min = min(point[0] for point in points)
        x_max = max(point[0] for point in points)
        y_min = min(point[1] for point in points)
        y_max = max(point[1] for point in points)
        # assert x_min < x_max
        # assert y_min < y_max
        return pygame.Rect(x_min, y_min, x_max - x_min, y_max - y_min)


class LevelMapRenderer:
    def __init__(self, level: p2l.LevelStore, chunk_size: int):
        self._chunks: dict[tuple[int, int], Chunk] = {}

        self._level = level
        self._chunk_size = chunk_size

    def render(self, screen: pygame.Surface, tilemap: levelmap.TileMap, camera_: list[int]) -> None:
        width = int(screen.get_width() / 10 // tilemap.scale / self._chunk_size)
        height = int(screen.get_height() / 10 // tilemap.scale / self._chunk_size)

        if tilemap.max_tile_size > self._chunk_size:
            raise NotImplementedError('tilemap.max_tile_size > LevelMapRenderer._chunk_size')

        for sy in range(-1, height + 1):
            for sx in range(-1, width + 1):
                x = sx + round(camera_[0] / 10 / self._chunk_size)
                y = sy + round(camera_[1] / 10 / self._chunk_size)

                chunk = self._chunks.get((x, y), None)
                if chunk is None:
                    chunk = self._chunks[(x, y)] = self._mesh_chunk((x, y), tilemap)

                self._render_chunk(screen, chunk, camera_, tilemap, (x, y))


    def _mesh_chunk(self, chunk_pos: tuple[int, int], tilemap: levelmap.TileMap) -> Chunk:
        start_time = time.time()

        points: list[tuple[pygame.Surface, list[tuple[int, int]]]] = []
        other_tiles: list[tuple[int, int]] = []

        textures: dict[str, pygame.Surface] = {}
        chunk: dict[tuple[int, int], str] = {}
        for dy in range(self._chunk_size):
            for dx in range(self._chunk_size):
                x = dx + chunk_pos[0] * self._chunk_size
                y = dy + chunk_pos[1] * self._chunk_size
                if (tile := self._level.get(x, y)) is not None:
                    v = tile.renderer.static_texture(tilemap)
                    if v is not None:
                        chunk[(dx, dy)] = v[1]
                        if v[0] not in textures:
                            textures[v[1]] = v[0]
                    else:
                        other_tiles.append((dx, dy))

        _offsets = [
            (0, -1),
            (1, 0),
            (0, 1),
            (-1, 0)
        ]
        def offset(x: int) -> tuple[int, int]:
            return _offsets[x % len(_offsets)]

        meshed: set[tuple[int, int, int, int]] = set()
        todo: set[tuple[int, int]] = set(chunk.keys())
        new_points: list[tuple[int, int]] = []
        while True:
            try:
                # x, y = sorted([k for k in chunk.keys() if k not in meshed])[0]
                x, y = sorted(todo)[0]
            except IndexError:
                break

            s = chunk[(x, y)]
            d = 0
            rotations = 0
            while True:
                # print((x, y), repr(s), rotations, new_points)
                if (x, y) in todo:
                    todo.remove((x, y))
                dx, dy = offset(d)
                if s == chunk.get((x + dx, y + dy)):
                    # print('Yes')
                    # if (dx, dy, x + dx, y + dy) in meshed:
                    if (dx, dy, x, y) in meshed:
                        # print('    Completed loop')
                        if (x + dx, y + dy) in todo:
                            todo.remove((x + dx, y + dy))

                        meshed.add((dx, dy, x, y))
                        if len(new_points) >= 3:
                            points.append((textures[s], new_points))
                            assert len(new_points) >= 3
                            new_points = []
                        break

                    new_points.append((x + (dx == 1) + (dy == 1), y + (dy == 1) + (dx == -1)))

                    meshed.add((dx, dy, x, y))
                    rotations = 0
                    x += dx
                    y += dy
                    d -= 1
                else:
                    # print('No')
                    meshed.add((dx, dy, x, y))
                    d += 1
                    dx, dy = offset(d)
                    new_points.append((x + (dx == 1) + (dy == 1), y + (dy == 1) + (dx == -1)))

                    rotations += 1
                    if rotations == 4:
                        # print('    Max rotations')
                        if len(new_points) >= 3:
                            points.append((textures[s], new_points))
                            assert len(new_points) >= 3
                            new_points = []
                        break
            # break

        print('Vertex amount before optimising:', sum(len(p) for p in points))
        points = [(s, o) for s, p in points if (o := self._optimise_mesh(p))]

        print('Meshing took:', time.time() - start_time, 'Vertex amount:', sum(len(p) for p in points))

        return Chunk(
            [(s, Chunk.generate_bounding_box(p), p) for s, p in points],
            other_tiles
        )

    def _optimise_mesh(self, points: list[tuple[int, int]]) -> list[tuple[int, int]]:
        starting_point = points[0]
        for point in points:
            if point != starting_point:
                break
        else:
            return []

        points = [points[i] for i in range(len(points)) if points[i] != points[i - 1]]

        out = [points[0]]
        for i, point in enumerate(points):
            if i >= len(points) - 2:
                out.append(point)
                continue
            if i == 0:
                out.append(point)
                continue

            dx = points[i][0] - points[i - 1][0]
            dy = points[i][1] - points[i - 1][1]
            if points[i][0] + dx == points[i + 1][0] and points[i][1] + dy == points[i + 1][1]:
                continue
            out.append(point)

        return out

    def _render_chunk(self, screen: pygame.Surface, chunk: Chunk, camera_: list[int], tilemap: levelmap.TileMap, chunk_pos: tuple[int, int]):
        _render_bounding_box = False
        _render_wireframe = False
        _render_fill_texture = True

        for surface, bounding_box, points in chunk.points:
            r = (
                ((bounding_box.x + chunk_pos[0] * self._chunk_size) * 10 - camera_[0]) * tilemap.scale,
                ((bounding_box.y + chunk_pos[1] * self._chunk_size) * 10 - camera_[1]) * tilemap.scale,
                bounding_box.width * 10 * tilemap.scale,
                bounding_box.height * 10 * tilemap.scale,
            )
            if _render_bounding_box:
                pygame.draw.rect(screen, (255, 0, 0), r)
            if not screen.get_rect().colliderect(r):
                continue

            points = [
                (
                    ((x + chunk_pos[0] * self._chunk_size) * 10 - camera_[0]) * tilemap.scale,
                    ((y + chunk_pos[1] * self._chunk_size) * 10 - camera_[1]) * tilemap.scale,
                ) for x, y in points
            ]
            if _render_fill_texture:
                pygame.gfxdraw.textured_polygon(screen, points, surface, (-camera_[0] % (10 * tilemap.max_tile_size)) * tilemap.scale, (camera_[1] % (10 * tilemap.max_tile_size)) * tilemap.scale)

            if _render_wireframe:
                for i in range(len(points)):
                    if i == 0:
                        c = (255, 255, 255)
                    else:
                        c = (255, 0, 255)
                    pygame.draw.circle(screen, c, points[i], tilemap.scale * 2.5)
                    pygame.draw.line(screen, (255, 255, 255), points[i], points[(i + 1) % len(points)], tilemap.scale)

        for dx, dy in chunk.other_tiles:
            x = dx + chunk_pos[0] * self._chunk_size
            y = dy + chunk_pos[1] * self._chunk_size

            t = self._level.get(x, y)
            assert t is not None

            t.renderer.render(screen, camera_, tilemap)
