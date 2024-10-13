import pygame
class Blocks:
    

    def __init__(self, screen, scale):
        
        global sc #how better?
        sc = scale
        
        self.screen = screen

        self.blocks = {}
        # for x in range(12):
        #     self.blocks[0, x] = Block(0, x)
        #     self.blocks[10, x] = Block(10, x)


        for x in range(20):
            self.blocks[x-3, 9] = Block(x-3, 9)
            self.blocks[0, x] = Block(0, x)
            self.blocks[13, x] = Block(13, x)
        
        self.blocks[0] = Block(6, 5)
        self.blocks[1] = Block(7, 5)
    
    def render(self):
        for block in self.blocks:
            pygame.draw.rect(self.screen, ("grey"), self.blocks[block].rect)


class Block:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x *30*sc, y *30*sc, 30 *sc, 30 *sc)

    