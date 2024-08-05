import pygame
class Blocks:
    def __init__(self, screen):
        self.screen = screen

        self.blocks = {}
        for x in range(6):
            self.blocks[-1, x] = Block(-0.66, x)
            self.blocks[12, x] = Block(12.33, x)

        for x in range(14):
            self.blocks[x-1, 6] = Block(x-1, 6)
            self.blocks[x-1, 0] = Block(x-1, 0)
        
        self.blocks[6, 3] = Block(6, 3)
    
    def render(self):
        for block in self.blocks:
            pygame.draw.rect(self.screen, ("grey"), self.blocks[block].rect)


class Block:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x*300, y*300, 300, 300)

    