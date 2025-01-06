from __future__ import annotations

import abc # 💀
import typing

import pygame
from math import sqrt
import json
import collections

from enums import Type, TileShapes, Events
from load_images import load_image, load_images


class Tilemap:
    
    def __init__(self, screen, images_, scale_):
        
        self.images = images_
        self.screen = screen
        self.scale = scale_
  
        with open("json_files/levels.json" , "r") as f:
            level_data : dict = json.load(f)

        self.tiles = {}
        self.blocks = {}
        for num in level_data:
            self.convert_level(level_data[num])

    def convert_level(self, tile,):
        tile["type"] = eval(tile["type"])
    
        if tile["type"] == Type.BLOCK:
            self.blocks[(tile["pos"][0], tile["pos"][1])] = Block(tile["pos"][0], tile["pos"][1], self.images[Type.BLOCK][tile["variant"]], self.scale )
    
        elif tile["type"] in Type.SPIKES:
            self.tiles[(tile["pos"][0], tile["pos"][1])] = Spike(tile["pos"][0], tile["pos"][1], tile["type"], self.images[tile["type"]], self.scale)
# ======================================================================================================================

    def render_tiles(self, camera, use_textures:bool):

        find_onscreen = lambda l: [key for key in l if -1 < key[0] - (camera[0] / 10) < 64 and -1 < key[1] - (camera[1] / 10) < 36]

        onscreen_blocks = find_onscreen(self.blocks)
        for block in onscreen_blocks:
            self.blocks[block].render(self.screen, camera, use_textures)

        onscreen_tiles = find_onscreen(self.tiles)
        for tile in onscreen_tiles:
            self.tiles[tile].render(self.screen, camera, use_textures)

    def reload_level(self, scale_):
        with open("json_files/levels.json" , "r") as f:
            level_data : dict = json.load(f)

        self.tiles = {}
        self.blocks = {}
        self.scale = scale_

        for num in level_data:
            self.convert_level(level_data[num])
        
class Spike:
    def __init__(self, x, y, type_, image_, scale_):

        self.type: Type = type_
        self.shape = self.check_shape(self.type)
        self.scale: int = scale_
        self.image = pygame.transform.scale(image_, (10 * self.scale, 10 * self.scale))

        if self.shape == TileShapes.BLOCK:
            self.rect = pygame.Rect(x * 10 , y * 10 , 10, 10)   
        elif self.shape == TileShapes.CIRCLE:
            self.circ = [x*10 + 5, y*10 + 5, 10] #centerx, centery, radius


        #if radius larger than 2 tile, colision doesn't function
    def check_shape(self, type):
        if type in (Type.SPIKE_CUBE, Type.SPIKE_SNAKE):
            return TileShapes.BLOCK
        
        if type == Type.SPIKE_CIRCLE:
            return TileShapes.CIRCLE
    
    def collision_logic(self, player_rect):
        match self.shape:
            case TileShapes.BLOCK:
                if self.rect.colliderect(player_rect):
                    return Events.DEATH
            case TileShapes.CIRCLE:
                if sqrt((self.circ[0] - player_rect.centerx) ** 2 + (self.circ[1] - player_rect.centery)**2) <= self.circ[2]: 
                    return Events.DEATH #only hits if player center is in range of circle
        
    def render(self, screen, camera, use_texture):

        if self.shape == TileShapes.BLOCK:
            draw_rect = pygame.Rect((self.rect.left - camera[0]) * self.scale, (self.rect.top - camera[1])* self.scale, self.rect.width* self.scale, self.rect.height* self.scale)
            
            if use_texture: screen.blit(self.image, draw_rect.topleft)
            else: pygame.draw.rect(screen, "orange", draw_rect)
        
        # elif self.shape == TileShapes.CIRCLE:
        #     pygame.draw.circle(screen, self.color, ((self.circ[0]- camera[0]) * scale, (self.circ[1]- camera[1]) * scale), self.circ[2] * scale)

class Block:
    def __init__(self, x, y, image_, scale_): #0-9
        self.rect = pygame.Rect(x * 10, y * 10, 10, 10)

        self.scale = scale_
        self.image = pygame.transform.scale(image_, (10 * self.scale, 10 * self.scale))

    def render(self, screen, camera, use_texture):
        draw_rect = pygame.Rect((self.rect.left - camera[0]) * self.scale, (self.rect.top - camera[1])* self.scale, self.rect.width* self.scale, self.rect.height* self.scale)
        
        if use_texture: screen.blit(self.image, draw_rect.topleft) #-1,because 0-index
        else: pygame.draw.rect(screen, "blue", draw_rect)

"""

Tile

    Type
        Solid
        Spike
        ...
    
    Collision: __init__(on_collision: typing.Callable)
        Collision shape
            Circle
            Rect
        
    Rendering -> 

"""


class Collider(abc.ABC):
    @abc.abstractmethod
    def __init__(self, on_collision: collections.abc.Callable[[], None], *args, **kwargs):
        pass

    @abc.abstractmethod
    def check_collision(self, other: Collider) -> tuple[bool, Events | None]:
        pass


class Renderer(abc.ABC):
    @abc.abstractmethod
    def __init__(self, collider: Collider, *args, **kwargs):
        pass

    @abc.abstractmethod
    def render(self, screen: pygame.Surface, camera: list[int], tilemap: TileMap2) -> None:  # TODO: It would be better if the texture renderer was another class
        pass


class TileFactory:

    def __init__(self, **kwargs):
        # TODO: Deduplicate this code
        self._collider_type: typing.Type | None = kwargs.get('collider_type', None)
        self._collider_args: list | None = kwargs.get('collider_args', None)
        self._collider_kwargs: dict | None = kwargs.get('collider_kwargs', None)

        self._renderer_type: typing.Type | None = kwargs.get('renderer_type', None)
        self._renderer_args: list | None = kwargs.get('renderer_args', None)
        self._renderer_kwargs: dict | None = kwargs.get('renderer_kwargs', None)

        self._tile_type: typing.Type | None = kwargs.get('tile_type', None)

    def add_type(self, collider_type: typing.Type, *args, **kwargs):
        if not issubclass(collider_type, Collider):
            raise TypeError()
        self._collider_type = collider_type
        self._collider_args = args
        self._collider_kwargs = kwargs

    def add_renderer(self, renderer_type: typing.Type, *args, **kwargs):
        if not issubclass(renderer_type, Renderer):
            raise TypeError()
        self._renderer_type = renderer_type
        self._renderer_args = args
        self._renderer_kwargs = kwargs

    def add_tile(self, tile_type: typing.Type):
        if not issubclass(tile_type, Tile):
            raise TypeError()
        self._tile_type = tile_type

    def create(self, *args, **kwargs):
        collider = self._collider_type(self._tile_type.on_collision, *self._collider_args or [], *args, **self._collider_kwargs or {}, **kwargs)
        renderer = self._renderer_type(collider, *self._renderer_args or [], **self._renderer_kwargs or {})
        return self._tile_type(collider, renderer)


class Tile(abc.ABC):

    collider: Collider
    renderer: Renderer

    def __init__(self, collider, renderer, *args, **kwargs):
        self.collider = collider
        self.renderer = renderer

    def collision(self, other: Collider) -> tuple[bool, Events | None]:
        return self.collider.check_collision(other)

    @abc.abstractmethod
    def on_collision(self, other: Tile) -> tuple[bool, Events | None]:
        """:return If player should collide"""
        pass

    def render(self, screen: pygame.Surface, camera: list[int], tilemap: TileMap2) -> None:
        self.renderer.render(screen, camera, tilemap)


class SolidBlock(Tile):

    def __init__(self, collider: Collider, renderer: Renderer):
        super().__init__(collider, renderer)

    def on_collision(self, other: Tile):
        return True, None


class BlockCollider(Collider):

    def __init__(self, on_collision: collections.abc.Callable[[Collider], tuple[bool, Events | None]], x: int, y: int):
        self._on_collision = on_collision
        self._rect = pygame.Rect(x * 10, y * 10, 10, 10)

    def check_collision(self, other: Collider) -> tuple[bool, Events | None]:
        if not isinstance(other, self.__class__):
            raise NotImplemented
        if self._rect.colliderect(other._rect):
            return self._on_collision(other)


class SolidBlockRenderer(Renderer):

    def __init__(self, collider = BlockCollider):
        self.collider = collider

    def render(self, screen: pygame.Surface, camera: list[int], tilemap: TileMap2) -> None:
        if not isinstance(self.collider, BlockCollider):
            raise NotImplementedError()

        rect = self.collider._rect

        draw_rect = pygame.Rect((rect.left - camera[0]) * tilemap.scale, (rect.top - camera[1]) * tilemap.scale,
                                rect.width * tilemap.scale, rect.height * tilemap.scale)

        if tilemap.use_textures:
            screen.blit(tilemap.images[Type.BLOCK], draw_rect.topleft)
        else:
            pygame.draw.rect(screen, "orange", draw_rect)


class TileMap2:
    def __init__(self, screen_, scale_: int, use_textures: bool):

        self.screen = screen_
        self.scale = scale_
        self.use_textures = use_textures
        self.images = []

        class TileTypes:
            BLOCK = TileFactory(renderer_type=SolidBlockRenderer, collider_type=BlockCollider, tile_type=SolidBlock)

        self.TileTypes = TileTypes

        self.tiles: list[Tile] = [] # TODO

        for rx in range(10):
            self.tiles.append(self.TileTypes.BLOCK.create(rx, 0))

        self._images = {
            Type.SPIKE_SNAKE: load_images.load_image("snake.png"),
            Type.BLOCK: load_images.load_images("tiles/")[1],
            Type.SPIKE_CUBE: load_images.load_image("spike_cube.png")
        }
        self.images: dict
        self.scale_images()


    def render(self, camera_: list[int]):
        for tile in self.tiles:
            tile.render(self.screen, camera_, self)

    def scale_images(self) -> None:
        size = round(self.scale * 10)
        self.images = {
            key: pygame.transform.scale(
                self._images[key], (size, size)
            ) for key in self._images
        }