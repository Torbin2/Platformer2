import pygame
import enum


class BlockType(enum.Enum):
    BLOCK = enum.auto()

class Blocks:

    def __init__(self, screen, scale_):

        self.screen = screen

        global scale
        scale = scale_

# block creation (remove)
        self.blocks = {}

        for x in range(120):
            #screen is (64, 36)
            self.blocks[x, 0] = Block(x, 0)
            self.blocks[x + 120, 0] = Block(x + 120, 0)
            self.blocks[x + 180, 0] = Block(x + 180, 0)
            self.blocks[0, x] = Block(0, x)
            self.blocks[x, 26] = Block(x, 26)

        self.blocks[20, 15] = Block(20, 15, color="red")
        self.blocks[21, 15] = Block(21, 15, color="green")

        self.blocks[23, 16] = Block(23, 16, color="skyblue")

        for m in range(10):
            self.blocks[1 + m, 16 + m] = Block(1 + m, 16 + m, color="forestgreen")
            self.blocks[1 + m, 16] = Block(1 + m, 16, color="orange")
#########################

    def render(self, camera):

        onscreen_blocks = [key for key in self.blocks if -1 < key[0] + (camera[0] / 10) < 64 and -1 < key[1] + (camera[1] / 10) < 36]

        for block in onscreen_blocks:
            self.blocks[block].render(self.screen, camera)

    def update_settings(self, scale_):

        global scale
        scale = scale_

        new_blocks = {}

        for i in self.blocks:
            new_blocks[i] = Block(i[0], i[1], type_=self.blocks[i].type_, color=self.blocks[i].color)
        
        self.blocks = new_blocks


class Block:

    def __init__(self,x,y, type_=BlockType.BLOCK, color="grey"):

        self.rect = pygame.Rect(x * 10 , y * 10 , 10, 10)
        self.type_ = type_
        self.color = color

    def render(self, screen, camera):
        pygame.draw.rect(screen, self.color, pygame.Rect((self.rect.left + camera[0]) * scale, (self.rect.top + camera[1])* scale,
                                                          self.rect.width* scale, self.rect.height* scale))
        print(pygame.Rect((self.rect.left + camera[0]) * scale, (self.rect.top + camera[1])* scale,self.rect.width* scale, self.rect.height* scale))
