import pygame

class Menu:
    def __init__(self):
        self.screen = pygame.display.set_mode((1000, 1000), pygame.FULLSCREEN)
        pygame.display.set_caption('game')
        self.clock = pygame.time.Clock()
        # self.font = pygame.font.Font((), 50) how to set default font?
        self.close = True #change this

        self.options = {"start" : 25,
                        "options" : 50,
                         "quit" : 60 }
        self.selected = 0

    def input(self):   
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            if self.selected != 0:
                self.selected -= 1
        elif keys[pygame.K_s]:
            if self.selected != len(self.options):
                self.selected += 1


    def render(self):
        pass

    def main(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.input()

            self.clock.tick(60)
            pygame.display.update()

            return self.close


