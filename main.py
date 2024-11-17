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

        self.camera = [0, 0]
        pygame.display.set_caption('game')
        self.clock = pygame.time.Clock()
        
    def apply_setting(self, new = False):
        self.settings = menu.main()

        self.scale = self.settings["window_size"]
        self.screen = pygame.display.set_mode((640 * self.scale , 360 * self.scale)) #16:9 ratio

        self.fps = 60 + (60 * self.settings["high_fps"])
        print(self.fps)

        if new:
            self.player = Player(self.screen)
            self.blocks = Blocks(self.screen, self.scale)
        else:
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
            self.player.update(self.blocks.blocks)
            
            #draw
            self.camera = self.player.update_camera(self.camera)
            camera = [round(self.camera[i]) for i in range(2)]

            self.blocks.render(camera)
            self.player.draw(camera, self.scale)

            self.clock.tick(self.fps)
            pygame.display.update()


Game().run()