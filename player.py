import pygame
import enum
import math

OFFSETS = [(-1, -1),
           (-1, 0),
           (-1, 1),
           (0, -1),
           (0, 0),
           (0, 1),
           (1, -1),
           (1, 0),
           (1, 1)]
# str = "["
# for i in range(3):
#     for j in range(3):
#         str += f",({i-1}, {j-1})"
# str += "]"
# print(str)
class PlayerState(enum.Enum):
    GROUNDED = enum.auto()

class Player:

    def __init__(self, screen, scale):
        self.scale = scale
        
        self.rect = pygame.Rect(231 * scale,
                                109 * scale,
                                9 * scale,
                                16 * scale)
        self.speed = [0,0]
        self.screen = screen

        self.mouse_pressed = [False, False, False]
        self.keys_pressed = {"space" : False,
                             "shift": False,
                             "a/d": False,
                             "r": False}

        self.gravity = 1 #1 is down, -1 is up

        self.state = PlayerState.GROUNDED
        self.jumps = 2
        self.flips = 1


    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.speed[0] -= 1
            self.keys_pressed["a/d"] = True
        elif keys[pygame.K_d]:
            self.speed[0] += 1
            self.keys_pressed["a/d"] = True
        else:
            self.keys_pressed["a/d"] = False

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

        if keys[pygame.K_r]:

            if not self.keys_pressed["r"]:

                self.rect.x = 100
                self.rect.y = 100

            self.keys_pressed["r"] = True

        else: self.keys_pressed["r"] = False

    def apply_mov(self, blocks): #and collison
        # left & right

        repeats = math.ceil(abs(self.speed[0] * self.scale) / 10) + 1
        stepx = self.speed[0] * self.scale / repeats

        for i in range(repeats):
            
            self.rect.centerx += stepx
            
            player_pos = [self.rect.centerx // (10 * self.scale), self.rect.centery // (10*self.scale)]

            blocks_around = []

            for offset in OFFSETS:
                tile = (player_pos[0] + offset[0], player_pos[1] + offset[1])
                if tile in blocks:
                    blocks_around.append(tile)


            for i in blocks_around:
                if self.rect.colliderect(blocks[i].rect):
                    if self.speed[0] > 0: 
                        self.rect.right = blocks[i].rect.left
                        self.speed[0] -= 4
                        if self.speed[0] < 0: self.speed[0] = 0 #in case of direction shift by collision
                        break

                    elif self.speed[0] < 0:
                        self.rect.left = blocks[i].rect.right
                        self.speed[0] += 4
                        if self.speed[0] > 0: self.speed[0] = 0#in case of direction shift by collision
                        break
            else:
                continue
            break

        
        #friction 

        # if self.keys_pressed["a/d"] = True
        if self.state == PlayerState.GROUNDED: num = max(self.speed[0] / 10, 0.7)
        else: num = max(self.speed[0] / 15, 0.4)
        print(num)
        
        if self.speed[0] > 0:
            if self.speed[0] - num <0: self.speed[0] = 0
            else:self.speed[0] -= num

        elif self.speed[0] < 0:
            if self.speed[0] + num >0: self.speed[0] = 0
            else:self.speed[0] += num

        # gravity
        if self.speed[1] * self.gravity < 10: #grav is 1/-1
            self.speed[1] += 0.7 * self.gravity
        
              
        repeats = math.ceil(abs(self.speed[1] * self.scale) / 10) + 1
        stepy = self.speed[1] * self.scale/ repeats
        print(repeats, stepy, self.speed)

        ground_touch = False
        for i in range(repeats):

            self.rect.centery += stepy

            player_pos = [self.rect.centerx //(10 *self.scale), self.rect.centery // (10*self.scale)]

            blocks_around = []

            for offset in OFFSETS:
                tile = (player_pos[0] + offset[0], player_pos[1] + offset[1])
                if tile in blocks:
                    blocks_around.append(tile)


            for i in blocks_around:
                if self.rect.colliderect(blocks[i].rect):
                    if self.speed[1] > 0:
                        self.rect.bottom = blocks[i].rect.top
                        self.speed[1] = 0
                        if self.gravity == 1:
                            ground_touch = True
                        break
                    elif self.speed[1] < 0:
                        self.rect.top = blocks[i].rect.bottom
                        self.speed[1] = 0
                        if self.gravity == -1:
                            ground_touch = True
                        break
            else:
                continue
            break
        if ground_touch:
            self.state = PlayerState.GROUNDED
            self.flips = 1
            self.jumps = 2
            
    def update_settings(self, scale):
        old_center = self.rect.center # / scale 
        self.scale = scale           
        self.rect = pygame.Rect(0 ,0 , 9 * scale, 16 * scale)
        self.rect.center = old_center # * scale

    def update_camera(self, camera):
        camera[0] *= -1
        camera[1] *= -1

        delta = [camera[0] - (self.rect.centerx - self.scale * 240), camera[1] - (self.rect.centery - self.scale * 135)]
        camera[0] -= delta[0] / 10
        camera[1] -= delta[1] / 10

        camera[0] *= -1
        camera[1] *= -1

        return camera

    def draw(self, camera):
        drawn_rect = pygame.Rect(self.rect.left + camera[0], self.rect.top + camera[1], self.rect.width, self.rect.height)

        pygame.draw.rect(self.screen, 'white', drawn_rect)

    def update(self, blocks):
        self.input()
        self.apply_mov(blocks)
        