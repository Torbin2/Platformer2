import pygame
from player import Player

pygame.init()


class Game:
    def __init__(self):

        self.screen = pygame.display.set_mode((3800, 2000), pygame.RESIZABLE)
        pygame.display.set_caption('game')
        self.clock = pygame.time.Clock()
        self.player = Player(self.screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.screen.fill("black")
            self.player.update()

            self.clock.tick(60)
            pygame.display.update()

Game().run()
