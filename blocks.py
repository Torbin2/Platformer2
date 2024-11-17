import pygame

class Tilemap:

    def __init__(self, screen):

        self.screen = screen

        # block creation (remove)

        self.tiles = {}

        for x in range(120):
            #screen is (64, 36)
            self.tiles[x, 0] = Block(x, 0)
            self.tiles[x + 120, 0] = Block(x + 120, 0)
            self.tiles[x + 180, 0] = Block(x + 180, 0)
            self.tiles[0, x] = Block(0, x)
            self.tiles[x, 26] = Block(x, 26)

        self.tiles[20, 15] = Block(20, 15, color="red")
        self.tiles[21, 15] = Block(21, 15, color="green")

        self.tiles[23, 16] = Block(23, 16, color="skyblue")

        for m in range(10):
            self.tiles[1 + m, 16 + m] = Block(1 + m, 16 + m, color="forestgreen")
            self.tiles[1 + m, 16] = Block(1 + m, 16, color="orange")

# ======================================================================================================================

    def render(self, camera, scale):

        onscreen_blocks = [key for key in self.tiles if -1 < key[0] - (camera[0] / 10) < 64 and -1 < key[1] - (camera[1] / 10) < 36]

        for block in onscreen_blocks:
            self.tiles[block].render(self.screen, camera, scale)

class Block:

    def __init__(self,
                 x,
                 y,
                 type_="block",
                 color="grey"):

        self.rect = pygame.Rect(x * 10,
                                y * 10,
                                10,
                                10)
        self.type = type_
        self.color = color

    def render(self, screen, camera, scale):
        pygame.draw.rect(screen, self.color, pygame.Rect((self.rect.left - camera[0]) * scale,
                                                         (self.rect.top - camera[1]) * scale,
                                                          self.rect.width * scale,
                                                         self.rect.height * scale)
        )
        
