import pygame

from player import Player
from levelmap import TileMap
from menu import Menu, render_loading_screen

pygame.init()
pygame.display.set_caption('platformer2')

open_menu = True
menu = Menu()

SCREEN_SIZE = (640, 360)

class Game:

    def __init__(self):
        self.clock = pygame.time.Clock()

        self.apply_setting()

        self.player = Player(self.screen)
        self.tilemap = TileMap(self.screen, self.scale, self.use_textures, self.settings['level'])

        self.camera = [0, 0]

    def apply_setting(self):
        menu.main(restart = True)
        self.settings = menu.settings

        self.scale = self.settings["window_size"]
        new_size = (SCREEN_SIZE[0] * self.scale, SCREEN_SIZE[1] * self.scale)
        if new_size != menu.screen.get_size():
            self.screen = pygame.display.set_mode(new_size) #16:9 ratio
        else:
            self.screen = menu.screen

        render_loading_screen(self.screen, menu.font)

        self.fps = 60 + (60 * self.settings["high_fps"])
        self.use_textures: bool = self.settings["textures"]

        self.tilemap = TileMap(self.screen, self.scale, self.use_textures, self.settings['level'])
        # try:
        #     self.tilemap = TileMap(self.screen, self.scale, self.use_textures, self.settings['level'])
        # except Exception:
        #     pass

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.apply_setting()
                    if event.key == pygame.K_r:
                        self.tilemap.level.load(self.tilemap)

            self.screen.fill("black")
            self.player.update(self.tilemap)
            
            #draw
            self.camera = self.player.update_camera(self.camera, list(map(lambda x: x/self.scale/2,self.screen.get_size())))
            camera = [round(self.camera[i]) for i in range(2)]

            #self.tilemap.render_tiles(camera, self.use_textures)
            self.tilemap.render(camera)
            self.player.draw(camera, self.scale)

            self.clock.tick(self.fps)
            pygame.display.update()


Game().run()
