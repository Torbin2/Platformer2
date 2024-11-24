import pygame
from math import sqrt
import json

#FORMAT IN JSON: {"x;y" : [IsBlock?(bool) ,x ,y, type],
#                 "x;y" : [IsBlock?(bool),x ,y , type]}

class Tilemap:
    
    def __init__(self, screen):

        self.screen = screen
        
        # block creation (remove)
        self.tiles = {}
        self.tiles["1;1"] = [True, 1, 1, "default"]
        self.tiles["2;2"] = [True, 2, 2, "default"]
        # for x in range(120):
        #     screen is (64, 36)
        #     self.tiles[f"{x, 0}"] = Block(x, 0)
            # self.tiles[str(x + 120, 0)] = Block(x + 120, 0)
            # self.tiles[str(x + 180, 0)] = Block(x + 180, 0)
            # self.tiles[str(0, x)] = Block(0, x)
            # self.tiles[str(x, 26)] = Block(x, 26)

        # self.tiles[str(20, 15)] = Block(20, 15, color="red")
        # self.tiles[str(21, 15)] = Block(21, 15, color="green")

        # self.tiles[str(23, 16)] = Block(23, 16, color="skyblue")

        # for m in range(10):
        #     self.tiles[str(1 + m, 16 + m)] = Block(1 + m, 16 + m, color="forestgreen")
        #     self.tiles[str(1 + m, 16)] = Block(1 + m, 16, color="orange")
        #     self.tiles[str(10+m, 10+m)] = Spike(10+m, 10+m,"cheese_block" ,"yellow")
        #     self.tiles[str(35, 6 + m*2)] = Spike(35, 6 + m*2, "circle_spike", "yellow" )
        # self.tiles[str(45,  10)] = Spike(45, 10, "big_circle_spike", "yellow" )

        with open("levels.json" , "w") as f:
            json.dump(self.tiles, f)

        self.blocks = {} #because block collision is different
        for i in self.tiles:
            if isinstance(self.tiles[i], Block):
                self.blocks[i] = (self.tiles[i])

        for i in self.blocks:
            self.tiles.pop(i)
        
# ======================================================================================================================

    def render(self, camera, scale):

        onscreen_blocks = [key for key in self.blocks if -1 < key[0] - (camera[0] / 10) < 64 and -1 < key[1] - (camera[1] / 10) < 36]
        onscreen_tiles = [key for key in self.tiles if -1 < key[0] - (camera[0] / 10) < 64 and -1 < key[1] - (camera[1] / 10) < 36]

        for block in onscreen_blocks:
            self.blocks[block].render(self.screen, camera, scale)
        for tile in onscreen_tiles:
            self.tiles[tile].render(self.screen, camera, scale)

        

class Spike:
    def __init__(self, x, y, type_="block", color="grey"):
        
        self.type = type_
        self.shape = self.check_shape(self.type)
        #self.function = ("spike, block, button") add logic
        
        self.color = color

        if self.type in ("cheese_block"):
            self.rect = pygame.Rect(x * 10 , y * 10 , 10, 10)
        
        elif self.type == "circle_spike":
            self.circ = [x*10 + 5, y*10 + 5, 10] #centerx, centery, radius
        elif self.type == "big_circle_spike":
            self.circ = [x*10 + 5, y*10 + 5, 20]

        #if radius larger than 2 tile, colision doesn't function
    def check_shape(self, type):
        if type in ("cheese_block"):
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
        
        

    def render(self, screen, camera, scale):
        if self.shape == "square":
            draw_rect = pygame.Rect((self.rect.left - camera[0]) * scale, (self.rect.top - camera[1])* scale, self.rect.width* scale, self.rect.height* scale)
            pygame.draw.rect(screen, self.color, draw_rect)
        
        elif self.shape == "circle":
            pygame.draw.circle(screen, self.color, ((self.circ[0]- camera[0]) * scale, (self.circ[1]- camera[1]) * scale), self.circ[2] * scale)


class Block:
    def __init__(self, x, y, color="grey", _type = "default"):
        self.color = color
        self.rect = pygame.Rect(x * 10 , y * 10 , 10, 10)
        self.type = _type

    def render(self, screen, camera, scale):
        draw_rect = pygame.Rect((self.rect.left - camera[0]) * scale, (self.rect.top - camera[1])* scale, self.rect.width* scale, self.rect.height* scale)
        pygame.draw.rect(screen, self.color, draw_rect)