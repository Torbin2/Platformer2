import pygame

class Player():

    def __init__(self, screen):
        self.rect = pygame.Rect(1600, 1000, 100, 100)
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
            self.speed[1] -= 90
            self.grounded = False

        if self.mouse_pressed != pygame.mouse.get_pressed():
            self.mouse_pressed = pygame.mouse.get_pressed()
            
            if self.mouse_pressed[0]:
                    self.speed[0] = self.speed[0] * -1
            if self.mouse_pressed[2]:
                self.speed[1] = self.speed[1] * -1
        else: pass

    def apply_mov(self, blocks):
        # left & right
        self.rect.centerx += self.speed[0]
        
        for i in blocks:
            if self.rect.colliderect(blocks[i].rect):
                if self.speed[0] > 0: 
                    self.rect.right = blocks[i].rect.left
                    self.speed[0] -= 8
                elif self.speed[0] < 0: 
                    self.rect.left = blocks[i].rect.right
                    self.speed[0] += 8

        if self.speed[0] > 0: self.speed[0] -= 2
        elif self.speed[0] < 0: self.speed[0] += 2

        # gravity

        if not self.grounded:
            if self.speed[1] <= 300: self.speed[1] += 3
            self.rect.y += self.speed[1]

        for i in blocks:
            if self.rect.colliderect(blocks[i].rect):
                if self.speed[1] > 0: 
                    self.rect.bottom = blocks[i].rect.top
                    self.speed[1] = 0
                    self.grounded = True
                elif self.speed[1] < 0: 
                    self.rect.top = blocks[i].rect.bottom
                    self.speed[1] += 12
            
            

        

    def draw(self):
        pygame.draw.rect(self.screen, 'white', self.rect)

    def update(self, blocks):
        self.input()
        self.apply_mov(blocks)
        self.draw()