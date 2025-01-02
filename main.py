import pygame
from scripts.player import Player
from scripts.blocks import TileMap2 as Tilemap
from scripts.menu import Menu
from scripts.load_images import load_image, load_images
from scripts.enums import Type

pygame.init()
pygame.display.set_caption('platformer2')


open_menu = True
menu = Menu()

class Game:

    def __init__(self):
        self.clock = pygame.time.Clock()

        self.apply_setting()

        self.player = Player(self.screen)
        self.tilemap = Tilemap(self.screen, self.scale, self.use_textures)


        self.camera = [0, 0]

    def apply_setting(self):
        self.settings = menu.main()

        self.scale = self.settings["window_size"]
        self.screen = pygame.display.set_mode((640 * self.scale , 360 * self.scale)) #16:9 ratio

        self.fps = 60 + (60 * self.settings["high_fps"])
        self.use_textures: bool = self.settings["textures"]

        try:
            self.tilemap.reload_level(self.scale)
        except:
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
                    # if event.key == pygame.K_r:
                        # self.tilemap.reload_level(self.scale)

            self.screen.fill("black")
            # self.player.update(self.tilemap.tiles, self.tilemap.blocks)
            
            #draw
            self.camera = self.player.update_camera(self.camera)
            camera = [round(self.camera[i]) for i in range(2)]

            #self.tilemap.render_tiles(camera, self.use_textures)
            self.tilemap.render(camera)
            self.player.draw(camera, self.scale)

            self.clock.tick(self.fps)
            pygame.display.update()


Game().run()