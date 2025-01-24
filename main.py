import pygame
from player import Player
from levelmap import TileMap
from menu import Menu

pygame.init()
pygame.display.set_caption('platformer2')



open_menu = True
menu = Menu()

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
        self.screen = pygame.display.set_mode((640 * self.scale , 360 * self.scale)) #16:9 ratio

        self.fps = 60 + (60 * self.settings["high_fps"])
        self.use_textures: bool = self.settings["textures"]

        try:
            self.tilemap.refresh(self.scale, self.tilemap)
        except Exception:
            pass


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
            self.camera = self.player.update_camera(self.camera)
            camera = [round(self.camera[i]) for i in range(2)]

            #self.tilemap.render_tiles(camera, self.use_textures)
            self.tilemap.render(camera)
            self.player.draw(camera, self.scale)

            self.clock.tick(self.fps)
            pygame.display.update()


Game().run()