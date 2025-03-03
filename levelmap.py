from __future__ import annotations

import abc # 💀
import enum
import typing

import pygame
import collections

import p2l
from enums import Events
from load_images import load_image, load_images


class Collider(abc.ABC):
    @abc.abstractmethod
    def __init__(self, on_collision: collections.abc.Callable[[], None], *args, **kwargs):
        pass

    @abc.abstractmethod
    def check_collision(self, other: pygame.Rect) -> tuple[bool, Events | None]:
        pass

    def serialise(self) -> dict[str, typing.Any]:
        """Return the **kwargs that can be used to create an object like this one."""
        return {}


class Renderer(abc.ABC):
    @abc.abstractmethod
    def __init__(self, collider: Collider, *args, **kwargs):
        pass

    @abc.abstractmethod
    def render(self, screen: pygame.Surface, camera: list[int], tilemap: TileMap) -> None:  # TODO: It would be better if the texture renderer was another class  # What and why?
        pass

    def serialise(self) -> dict[str, typing.Any]:
        """Return the **kwargs that can be used to create an object like this one."""
        return {}


class TileFactory:

    def __init__(self, **kwargs):
        # TODO: Deduplicate this code
        self._tile_type: typing.Type[Tile] | None = kwargs.get('tile_type', None)
        self._tile_args: list = kwargs.get('tile_args', [])
        self._tile_kwargs: dict = kwargs.get('tile_kwargs', {})

        self._collider_type: typing.Type | None = kwargs.get('collider_type', None)
        self._collider_args: list = kwargs.get('collider_args', [])
        self._collider_kwargs: dict = kwargs.get('collider_kwargs', {})

        self._renderer_type: typing.Type | None = kwargs.get('renderer_type', None)
        self._renderer_args: list = kwargs.get('renderer_args', [])
        self._renderer_kwargs: dict = kwargs.get('renderer_kwargs', {})

        self._tile_type_name: str | None = kwargs.get('tile_type_name', None)

    def add_type(self, tile_type: typing.Type | None, args: list | None, kwargs: dict | None):
        if tile_type is not None and not issubclass(tile_type, Tile):
            raise TypeError()
        self._tile_type = tile_type or self._tile_type
        self._tile_args += (args or [])
        self._tile_kwargs |= (kwargs or {})

    def add_renderer(self, renderer_type: typing.Type | None, args: list | None, kwargs: dict | None):
        if renderer_type is not None and not issubclass(renderer_type, Renderer):
            raise TypeError()
        self._renderer_type = renderer_type or self._renderer_type
        self._renderer_args += (args or [])
        self._renderer_kwargs |= (kwargs or {})

    def add_collider(self, collider_type: typing.Type | None, args: list | None, kwargs: dict | None):
        if collider_type is not None and not issubclass(collider_type, Collider):
            raise TypeError()
        self._collider_type = collider_type or self._collider_type
        self._collider_args += (args or [])
        self._collider_kwargs |= (kwargs or {})

    def add_tile(self, tile_type: typing.Type):
        if not issubclass(tile_type, Tile):
            raise TypeError()
        self._tile_type = tile_type

    def add_tile_type_name(self, type_name: str):
        self._tile_type_name = type_name

    def create(self, *args, **kwargs):
        if self._tile_type_name is None:
            raise ValueError('Cannot create tile without name')

        collider = self._collider_type(self._tile_type.on_collision, *self._collider_args or [], *args, **self._collider_kwargs or {}, **kwargs)
        renderer = self._renderer_type(collider, *self._renderer_args or [], **self._renderer_kwargs or {})
        return self._tile_type(collider, renderer, self._tile_type_name)

    def duplicate(self) -> TileFactory:
        return TileFactory(
            collider_type=self._collider_type,
            collider_args=self._collider_args.copy(),
            collider_kwargs=self._collider_kwargs.copy(),

            renderer_type=self._renderer_type,
            renderer_args=self._renderer_args.copy(),
            renderer_kwargs=self._renderer_kwargs.copy(),

            tile_type=self._tile_type,
            tile_type_name=self._tile_type_name,
        )


class Tile(abc.ABC):

    collider: Collider
    renderer: Renderer

    def __init__(self, collider, renderer, type_name: str, *args, **kwargs):
        self.collider = collider
        self.renderer = renderer
        self.type_name = type_name

    def collision(self, other: pygame.Rect) -> tuple[bool, Events | None]:
        return self.collider.check_collision(other)

    @classmethod
    @abc.abstractmethod
    def on_collision(cls, other: pygame.Rect) -> tuple[bool, Events | None]:
        """:return If player should collide"""
        pass

    def render(self, screen: pygame.Surface, camera: list[int], tilemap: TileMap) -> None:
        self.renderer.render(screen, camera, tilemap)

    def serialise(self) -> dict[str, typing.Any]:
        """Return the **kwargs that, in combination with the right collider and renderer, can be used to create an object like this one"""
        return {}


class SolidBlock(Tile):

    # def __init__(self, collider: Collider, renderer: Renderer):
    #     super().__init__(collider, renderer)

    @classmethod
    def on_collision(cls, other: pygame.Rect):
        return True, None


class SpikeBlock(Tile):
    @classmethod
    def on_collision(cls, other: pygame.Rect):
        return True, Events.DEATH


class CheckPoint(Tile):
    @classmethod
    def on_collision(cls, other: pygame.Rect):
        return True, Events.GET_CHECKPOINT


class BlockCollider(Collider):
    def __init__(self, on_collision: collections.abc.Callable[[pygame.Rect], tuple[bool, Events | None]], x: int, y: int, size: tuple[int, int] = (10, 10)):
        self._on_collision = on_collision
        self._rect = pygame.Rect(x * 10, y * 10, size[0], size[1])

    def check_collision(self, other: pygame.Rect) -> tuple[bool, Events | None]:
        if self._rect.colliderect(other):
            return self._on_collision(other)
        else:
            return False, None

    # TODO: should we save the size?


class SolidBlockRenderer(Renderer):
    _DEFAULT_TEXTURE_NUM = 0
    _DEFAULT_COLOR = "orange"

    def __init__(self, collider: BlockCollider, texture_num: int | None = None, image_name: str = None, color=_DEFAULT_COLOR):
        if image_name is None:
            raise ValueError('SolidBlockRenderer needs a texture')
        self._image_name = image_name

        self._color = color

        self.collider = collider

        if texture_num is None:
            texture_num = self._DEFAULT_TEXTURE_NUM
        self.texture_num = texture_num

    def render(self, screen: pygame.Surface, camera: list[int], tilemap: TileMap) -> None:
        if not isinstance(self.collider, BlockCollider):
            raise NotImplementedError(self.collider, )

        rect = self.collider._rect

        draw_rect = pygame.Rect(int((rect.left - camera[0]) * tilemap.scale),
                                int((rect.top - camera[1]) * tilemap.scale),
                                rect.width * tilemap.scale, rect.height * tilemap.scale)

        if tilemap.use_textures:
            textures = tilemap.images[getattr(Images, self._image_name)]
            if type(textures) is list:
                texture = textures[self.texture_num]
            else:
                texture = textures
            screen.blit(texture, draw_rect.topleft)

        else:
            pygame.draw.rect(screen, self._color, draw_rect)

    def serialise(self) -> dict[str, typing.Any]:
        out = {
            'image_name': self._image_name
        }

        if self.texture_num != self._DEFAULT_TEXTURE_NUM:
            out.update({
                'texture_num': self.texture_num
            })
        if self._color != self._DEFAULT_COLOR:
            out.update({
                'color': self._color
            })

        return out


class ConnectedSolidBlockRenderer(SolidBlockRenderer):
    pass


class Images(enum.StrEnum):
    SNAKE = enum.auto()
    BLOCKS = enum.auto()
    SPIKE_BLOCK = enum.auto()
    CHECKPOINT = enum.auto()


class TileMap:
    def __init__(self, screen_: pygame.Surface, scale_: int, use_textures: bool, level_name: str):

        self.screen = screen_
        self.scale = scale_
        self.use_textures = use_textures

        self._max_tile_size = 1

        class TileTypes:
            BLOCK = TileFactory(
                renderer_type=ConnectedSolidBlockRenderer,
                renderer_kwargs={'image_name': 'BLOCKS', 'color': [28, 81, 117]},
                collider_type=BlockCollider,
                tile_type=SolidBlock
            )
            SPIKE = TileFactory(
                renderer_type=SolidBlockRenderer,
                renderer_kwargs={'image_name': 'SPIKE_BLOCK'},
                collider_type=BlockCollider,
                tile_type=SpikeBlock
            )
            CHECKPOINT = TileFactory(
                renderer_type=SolidBlockRenderer,
                renderer_kwargs={'image_name': 'CHECKPOINT', "texture_num" : 0 },
                collider_type=BlockCollider,
                collider_kwargs={"size": (30, 30)},
                tile_type=CheckPoint
            )

        for tile_name in dir(TileTypes):
            if tile_name.startswith('_'):
                continue
            getattr(TileTypes, tile_name).add_tile_type_name(tile_name)

        self.TileTypes = TileTypes

        self.level = p2l.LevelStore(level_name)
        self.level.load(self)

        # for rx in range(-5, 10):
        #     self.level.set(rx, 0, self.TileTypes.BLOCK.create(rx, 0))
        # self.level.save(self)

        self._images = {
            Images.SNAKE: load_image("snake.png"),
            Images.BLOCKS: load_images("tiles/"),
            Images.SPIKE_BLOCK: load_image("spike_cube.png") , # TODO: This is a duplicate of Images
            Images.CHECKPOINT : load_images("checkpoint/"),
        }
        self.images: dict
        self.scale_images()

    def get_tile_factory(self, name: str) -> TileFactory:
        if name.startswith('_'):
            raise ValueError(name)
        return getattr(self.TileTypes, name).duplicate()

    def render(self, camera_: list[int]):
        width = int(self.screen.get_width() / 10 // self.scale - 3)
        height = int(self.screen.get_height() / 10 // self.scale - 1)
        for sy in range(-self._max_tile_size, height + self._max_tile_size):
            for sx in range(-self._max_tile_size, width + self._max_tile_size):
                x = sx + round(camera_[0] / 10)
                y = sy + round(camera_[1] / 10)

                tile = self.level.get(x, y)
                if tile is None:
                    continue

                tile.render(self.screen, camera_, self)

    def collide(self, player: pygame.Rect) -> list[tuple[Collider, Events | None]]:
        out = []
        for x in range((player.left // 10) - self._max_tile_size, (player.right // 10) + self._max_tile_size):
            for y in range((player.top // 10) - self._max_tile_size,
                           (player.bottom // 10) + self._max_tile_size):
                if (tile := self.level.get(x, y)) is not None:
                    collided, event = tile.collider.check_collision(player)
                    if collided or event is not None:
                        out.append((tile.collider, event))
        return out

    def scale_images(self) -> None:
        self.images = {}
        for key in self._images:
            size = lambda x : round(pygame.Surface.get_width(x) * self.scale)
            if type(self._images[key]) is list:
                self.images[key] = [pygame.transform.scale(image, (size(image), size(image))) for image in self._images[key]]
            else:
                self.images[key] = pygame.transform.scale(self._images[key], (size(self._images[key]), size(self._images[key])))
