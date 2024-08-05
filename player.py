import pygame

class Player():

    def __init__(self, screen):
        self.rect = pygame.Rect(0, 0, 100, 100)
        self.speed = [0,0]
        self.screen = screen

        self.grounded = False
        self.mouse_pressed = [False, False, False]

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            if self.speed[0] > -60: self.speed[0] -= 4
        if keys[pygame.K_d]:
            if self.speed[0] < 60: self.speed[0] += 4
        if keys[pygame.K_SPACE] and self.grounded:
            self.speed[1] -= 120
            self.grounded = False

        if self.mouse_pressed != pygame.mouse.get_pressed():
            self.mouse_pressed = pygame.mouse.get_pressed()
            
            if self.mouse_pressed[0]:
                    self.speed[0] = self.speed[0] * -1
            if self.mouse_pressed[2]:
                self.speed[1] = self.speed[1] * -1
        else: pass

    def aply_mov(self):
        # left & right
        self.rect.centerx += self.speed[0]

        if self.speed[0] > 0: self.speed[0] -= 2
        elif self.speed[0] < 0: self.speed[0] += 2

        # gravity


        if self.rect.bottom > 2000:
            self.rect.bottom = 2000
            self.speed[1] = 0
            self.grounded = True
        if not self.grounded:
            self.speed[1] += 6
            self.rect.y += self.speed[1]

    def draw(self):
        pygame.draw.rect(self.screen, 'white', self.rect)

    def update(self):
        self.input()
        self.aply_mov()
        self.draw()