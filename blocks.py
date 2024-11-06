import pygame
class Blocks:
    

    def __init__(self, screen, scale):
        
        global sc
        sc = scale
        
        self.screen = screen

        self.blocks = {}
        # for x in range(12):
        #     self.blocks[0, x] = Block(0, x)
        #     self.blocks[10, x] = Block(10, x)


        for x in range(90):
            #screen is (45, 27)
            self.blocks[x, 0] = Block(x, 0)
            self.blocks[0, x] = Block(0, x)
            self.blocks[x, 26] = Block(x, 26)
            self.blocks[44, x] = Block(44, x)
        
        self.blocks[20, 15] = Block(20, 15)
        self.blocks[21, 15] = Block(21, 15)
    
    def render(self):
        for block in self.blocks:
            pygame.draw.rect(self.screen, ("grey"), self.blocks[block].rect)

    def update_settings(self, scale):
        global sc
        sc = scale
        new_blocks = {}
        for i in self.blocks:
            new_blocks[i] = Block(i[0], i[1])
        
        self.blocks = new_blocks


class Block:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x *10*sc, y *10*sc, 10 *sc, 10 *sc)
        self.type = "block"

    