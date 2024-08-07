import pygame
class Blocks:
    def __init__(self, screen):
        self.screen = screen

        self.blocks = {}
        for x in range(10):
            self.blocks[111, x] = Block(-0.66, x-2)
            self.blocks[222, x] = Block(12.66, x-2)

        for x in range(14):
            self.blocks[x, 111] = Block(x-1, 6.66)
            self.blocks[x, 222] = Block(x-1, -0.66)
        
        self.blocks[6, 3] = Block(6, 3)
        self.blocks[7, 3] = Block(7, 3)
    
    def render(self):
        for block in self.blocks:
            pygame.draw.rect(self.screen, ("grey"), self.blocks[block].rect)


class Block:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x*300, y*300, 300, 300)

    