import pygame
from math import sqrt
import json
from enum import Enum

def convert_level(pos: list[int, int], class_type: str, variant: str, blocks:dict, tiles : dict):
    match class_type:
        case "block":
            blocks[(pos[0], pos[1])] = Block(pos[0], pos[1], variant)
        case "spike":
            tiles[(pos[0], pos[1])] = Spike(pos[0], pos[1], variant)

class Tilemap:
    
    def __init__(self, screen):

        self.screen = screen
  
        with open("json_files/levels.json" , "r") as f:
            level_data : dict = json.load(f)

        self.tiles = {}
        self.blocks = {}
        for num in level_data:
            data = level_data[num]
            convert_level(data["pos"], data["type"], data["variant"], self.blocks, self.tiles)



        
# ======================================================================================================================

    def render(self, camera, scale, images:dict):

        onscreen_blocks = [key for key in self.blocks if -1 < key[0] - (camera[0] / 10) < 64 and -1 < key[1] - (camera[1] / 10) < 36]
        onscreen_tiles = [key for key in self.tiles if -1 < key[0] - (camera[0] / 10) < 64 and -1 < key[1] - (camera[1] / 10) < 36]

        for block in onscreen_blocks:
            self.blocks[block].render(self.screen, camera, scale, images["blocks"])
        for tile in onscreen_tiles:
            self.tiles[tile].render(self.screen, camera, scale, images["snake"])

        
class Spike:
    def __init__(self, x, y, type_="cheese_block", color="yellow"):
        
        self.type = type_
        self.shape = self.check_shape(self.type)
        #self.function = ("spike, block, button") add logic
        
        self.color = color

        if self.shape == "square":
            self.rect = pygame.Rect(x * 10 , y * 10 , 10, 10)
        
        elif self.type == "circle_spike":
            self.circ = [x*10 + 5, y*10 + 5, 10] #centerx, centery, radius
        elif self.type == "big_circle_spike":
            self.circ = [x*10 + 5, y*10 + 5, 20]

        #if radius larger than 2 tile, colision doesn't function
    def check_shape(self, type):
        if type in ("cheese_block" ,"snake"):
            return "square"
        
        if type in ("circle_spike", "big_circle_spike"):
            return "circle"
        
        if type == "spike":
            return "triangle"
    
    def collision_logic(self, player_rect):
        match self.shape:
            case "square":
                if self.rect.colliderect(player_rect):
                    return "death"
            case "circle":
                if sqrt((self.circ[0] - player_rect.centerx) ** 2 + (self.circ[1] - player_rect.centery)**2) <= self.circ[2]: 
                    return "death" #only hits if playercenter is in range of circle, may change this
        
    def render(self, screen, camera, scale, image):
        if self.shape == "square":
            draw_rect = pygame.Rect((self.rect.left - camera[0]) * scale, (self.rect.top - camera[1])* scale, self.rect.width* scale, self.rect.height* scale)
            pygame.draw.rect(screen, self.color, draw_rect)
            screen.blit(pygame.transform.scale(image, (draw_rect.width, draw_rect.height )), draw_rect.topleft)
        
        elif self.shape == "circle":
            pygame.draw.circle(screen, self.color, ((self.circ[0]- camera[0]) * scale, (self.circ[1]- camera[1]) * scale), self.circ[2] * scale)

class Block:
    def __init__(self, x, y, image_num:str):
        self.image_num = int(image_num) #0-9
        self.rect = pygame.Rect(x * 10 , y * 10 , 10, 10)

    def render(self, screen, camera, scale, images):
        draw_rect = pygame.Rect((self.rect.left - camera[0]) * scale, (self.rect.top - camera[1])* scale, self.rect.width* scale, self.rect.height* scale)
        
        screen.blit(pygame.transform.scale(images[self.image_num - 1], (draw_rect.width, draw_rect.height )), draw_rect.topleft) #-1,because 0-index

        