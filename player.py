import pygame

class Player():

    def __init__(self, screen, scale):
        self.scale = scale
        
        self.rect = pygame.Rect(45 * scale, 80 * scale, 9 * scale, 16 * scale)
        self.speed = [0,0]
        self.screen = screen

        self.ground_timer = 0 #cyote_time
        self.mouse_pressed = [False, False, False]

        self.gravity = 1 #1 is down, 0 is up

        self.state = "grounded"


        # self.input_block = False
        # self.input_timer = 0

    def input(self):
        keys = pygame.key.get_pressed()
        # if not self.input_block:
        #     if keys[pygame.K_a]:
        #         if self.speed[0] > -60: self.speed[0] -= 4
        #     if keys[pygame.K_d]:
        #         if self.speed[0] < 60: self.speed[0] += 4
        # else:
        #     self.input_timer +=1
        #     if self.input_timer >= 30:
        #         self.input_block = False

        if keys[pygame.K_a]:
            if self.speed[0] > -9.9:
                self.speed[0] -= 1.9
        if keys[pygame.K_d] :
            if self.speed[0] < 9.9:
                self.speed[0] += 1.9

        if self.state == "grounded":
            self.ground_timer = 7 #cyote_time
        
        if keys[pygame.K_SPACE] and self.ground_timer > 0:
                
                if self.gravity == 1:
                    self.speed[1] = -13
                else: self.speed[1] = +13
                self.ground_timer = 0
            
        if self.ground_timer > 0: self.ground_timer -= 1


        if self.mouse_pressed[0] != pygame.mouse.get_pressed()[0] :
            self.mouse_pressed[0] = pygame.mouse.get_pressed()[0]
            
            if self.mouse_pressed[0] :
                self.gravity = -self.gravity

        # if keys[pygame.K_LSHIFT]:
        #     self.gravity = -self.gravity
        
        if self.mouse_pressed[2] != pygame.mouse.get_pressed()[2]:
            self.mouse_pressed[2] = pygame.mouse.get_pressed()[2]            
            
            if self.mouse_pressed[2]:
                self.speed[1] = self.speed[1] * -1.5
            else: pass

    def apply_mov(self, blocks):
        # left & right
        self.rect.centerx += self.speed[0] * self.scale
        
        for i in blocks:
            if self.rect.colliderect(blocks[i].rect):
                if self.speed[0] > 0: 
                    self.rect.right = blocks[i].rect.left
                    self.speed[0] -= 4
                    if self.speed[0] < 0: self.speed[0] = 0 #in case of direction shift by collision

                elif self.speed[0] < 0: 
                    self.rect.left = blocks[i].rect.right
                    self.speed[0] += 4
                    if self.speed[0] > 0: self.speed[0] = 0#in case of direction shift by collision
        
        #friction 
        if self.state == "grounded": num = 1.5
        else: num =1.4
        if self.speed[0] > 0:
            if self.speed[0] - num <0: self.speed[0] = 0
            else:self.speed[0] -= num
        
        elif self.speed[0] < 0:
            if self.speed[0] + num >0: self.speed[0] = 0
            else:self.speed[0] += num

        # gravity

        if self.speed[1] <= 60:
            if self.gravity == 1: 
                self.speed[1] += 1
            else: self.speed[1] -= 1
        self.rect.y += self.speed[1] * self.scale

        self.state = "air"
        for i in blocks:
            if self.rect.colliderect(blocks[i].rect):
                
                if self.speed[1] > 0: 
                    self.rect.bottom = blocks[i].rect.top   
                elif self.speed[1] < 0: 
                    self.rect.top = blocks[i].rect.bottom

                self.speed[1] = 0
                self.state = "grounded"
            
            

        

    def draw(self):
        pygame.draw.rect(self.screen, 'white', self.rect)

    def update(self, blocks):
        self.input()
        self.apply_mov(blocks)
        self.draw()