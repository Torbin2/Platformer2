import abc # 💀

import pygame
from math import sqrt
import json

from scripts.enums import Type, TileShapes, Events


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
            self.tiles[(tile["pos"][0], tile["pos"][1])] = Spike(tile["pos"][0], tile["pos"][1], tile["type"], self.images[int(tile["type"])], self.scale)
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
        
    Collision shape
        Circle
        Rect
    
    Collision: __init__(on_collision: typing.Callable)
        
    Rendering -> 

"""

class TileType(abc.ABC): # 💀

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def collision(self):
        pass

    @abc.abstractmethod
    def render(self):
        pass


class SolidBlock(TileType):

    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape

    def collision(self):
        pass

    def render(self):
        match (self.shape): # nu, Tschuss :tm:tm:t:tm dag ad
            case _:
                pass

# waar ben je