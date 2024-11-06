import pygame
from player import Player
from blocks import Blocks
from menu import Menu
pygame.init()

open_menu = True
menu = Menu()

class Game:
    def __init__(self):


        self.apply_setting(True)


        pygame.display.set_caption('game')
        self.clock = pygame.time.Clock()
        
    def apply_setting(self, new = False):
        self.settings = menu.main()

        self.scale = self.settings["window_size"]
        self.screen = pygame.display.set_mode((480 * self.scale, 270* self.scale)) #16:9 ratio
        self.fps = 60 + (60 * self.settings["high_fps"])
        print(self.fps)

        if new:
            self.player = Player(self.screen, self.scale)
            self.blocks = Blocks(self.screen, self.scale)
        else:
            self.player.update_settings(self.scale)
            self.blocks.update_settings(self.scale)
        

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.apply_setting()



            self.screen.fill("black")

            self.blocks.render()
            self.player.update(self.blocks.blocks)

            self.clock.tick(self.fps)
            pygame.display.update()

    
        


    
Game().run()
