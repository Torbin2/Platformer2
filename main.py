import pygame
from player import Player
from blocks import Blocks
from menu import Menu
pygame.init()

open_menu = True
menu = Menu()

class Game:
    def __init__(self):

        #self.screen = pygame.display.set_mode((3800, 2000), pygame.RESIZABLE)
        self.screen = pygame.display.set_mode((3800, 2000))
        pygame.display.set_caption('game')
        self.clock = pygame.time.Clock()
        

        self.player = Player(self.screen)
        self.blocks = Blocks(self.screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menu.main()

            self.screen.fill("black")

            self.blocks.render()
            self.player.update(self.blocks.blocks)

            self.clock.tick(60)
            pygame.display.update()

            
menu.main()
    
Game().run()
