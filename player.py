import pygame

class Player():

    def __init__(self, screen, scale):
        self.scale = scale
        
        self.rect = pygame.Rect(45 * scale, 80 * scale, 9 * scale, 16 * scale)
        self.speed = [0,0]
        self.screen = screen

        self.mouse_pressed = [False, False, False]
        self.keys_pressed = {"space" : False,
                             "shift": False}

        self.gravity = 1 #1 is down, -1 is up

        self.state = "grounded"
        self.jumps = 2
        self.flips = 1

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
            if self.speed[0] > -10:
                self.speed[0] -= 1
        elif keys[pygame.K_d] :
            if self.speed[0] < 10:
                self.speed[0] += 1

        if keys[pygame.K_SPACE] and self.jumps > 0:
                
                if not self.keys_pressed["space"]:
                    self.jumps -= 1

                    if self.gravity == 1:
                        self.speed[1] = -12
                    else: self.speed[1] = +12
                
                self.keys_pressed["space"] = True 
        else: self.keys_pressed["space"] = False

        if keys[pygame.K_LSHIFT] and self.flips > 0:
            
            if not self.keys_pressed["shift"]:

                self.flips -= 1
                self.gravity = -self.gravity
            
            self.keys_pressed["shift"] = True
        else: self.keys_pressed["shift"] = False

        if self.mouse_pressed[0] != pygame.mouse.get_pressed()[0] :
            self.mouse_pressed[0] = pygame.mouse.get_pressed()[0]
            
            if self.mouse_pressed[0] :
                self.gravity = -self.gravity
        


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
        if self.state == "grounded": num = 0.7
        else: num =0.3
        
        if self.speed[0] > 0:
            if self.speed[0] - num <0: self.speed[0] = 0
            else:self.speed[0] -= num
        
        elif self.speed[0] < 0:
            if self.speed[0] + num >0: self.speed[0] = 0
            else:self.speed[0] += num

        # gravity
        if abs(self.speed[1]) <= 15:
            self.speed[1] += 1 * self.gravity
        else: self.speed[1] = 15 * self.gravity #change this
        
              
        self.rect.y += self.speed[1] * self.scale

        colided = False
        for i in blocks:
            if self.rect.colliderect(blocks[i].rect):
                
                if self.speed[1] > 0: 
                    self.rect.bottom = blocks[i].rect.top   
                elif self.speed[1] < 0: 
                    self.rect.top = blocks[i].rect.bottom

                colided = True
        if colided:
            self.state = "grounded"
            self.speed[1] = 0
            self.flips = 1
            self.jumps = 2
            
    def update_settings(self, scale):
        old_center = self.rect.center # / scale 
        self.scale = scale           
        self.rect = pygame.Rect(0 ,0 , 9 * scale, 16 * scale)
        self.rect.center = old_center # * scale

        

    def draw(self):
        pygame.draw.rect(self.screen, 'white', self.rect)

    def update(self, blocks):
        self.input()
        self.apply_mov(blocks)
        self.draw()