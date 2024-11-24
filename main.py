import pygame
from player import Player
from blocks import Tilemap
from menu import Menu

pygame.init()
pygame.display.set_caption('platformer2')


open_menu = True
menu = Menu()

class Game:

    def __init__(self):
        self.clock = pygame.time.Clock()

        self.apply_setting(True)

        
        self.player = Player(self.screen)
        self.tilemap = Tilemap(self.screen)
        
        self.camera = [0, 0]
        
        
    def apply_setting(self, new = False):
        self.settings = menu.main()

        self.scale = self.settings["window_size"]
        self.screen = pygame.display.set_mode((640 * self.scale , 360 * self.scale)) #16:9 ratio

        self.fps = 60 + (60 * self.settings["high_fps"])


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
            self.player.update(self.tilemap.tiles, self.tilemap.blocks)
            
            #draw
            self.camera = self.player.update_camera(self.camera)
            camera = [round(self.camera[i]) for i in range(2)]

            self.tilemap.render(camera, self.scale)
            self.player.draw(camera, self.scale)

            self.clock.tick(self.fps)
            pygame.display.update()


Game().run()