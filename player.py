import pygame
from enums import Type, PlayerState, Events
from math import ceil

OFFSETS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0),(1, 1),
           (0, 2), (0,-2)]


PhYSICS_MOD = 1
SPEED_MOD = 1


class Player:

    def __init__(self, screen):
        
        self.rect = pygame.Rect(231, 109, 9, 19)
        self.speed = [0,0]
        self.screen = screen

        self.mouse_pressed = [False, False, False]
        self.keys_pressed = {"space" : False,
                             "shift": False,
                             "a/d": False,
                             "r": False}

        self.gravity = -1 #1 is down, -1 is up

        self.state = PlayerState.GROUNDED
        self.jumps = 2
        self.flips = 1

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.speed[0] -= 0.4 * PhYSICS_MOD * SPEED_MOD
            self.keys_pressed["a/d"] = True
        elif keys[pygame.K_d]:
            self.speed[0] += 0.4 * PhYSICS_MOD * SPEED_MOD
            self.keys_pressed["a/d"] = True
        else:
            self.keys_pressed["a/d"] = False

        if keys[pygame.K_SPACE] and self.jumps > 0:
                
                if not self.keys_pressed["space"]:
                    self.jumps -= 1

                    if self.gravity == 1:
                        self.speed[1] = -12 * PhYSICS_MOD
                    else: self.speed[1] = +12 * PhYSICS_MOD
                
                self.keys_pressed["space"] = True 
        else: self.keys_pressed["space"] = False

        if keys[pygame.K_LSHIFT]:
            if self.flips > 0:
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

    def apply_mov(self, blocks): #and collison with blocks
        # left & right (back and forth (Sisphus reference>!!!!!!???))

        repeats = ceil(abs(self.speed[0]) / 10) + 1
        stepx = self.speed[0] / repeats

        for i in range(repeats):
            
            self.rect.centerx += stepx
            
            player_pos = [self.rect.centerx // 10, self.rect.centery // 10]

            blocks_around = []

            for offset in OFFSETS:
                tile = (player_pos[0] + offset[0], player_pos[1] + offset[1])
                if tile in blocks:
                    blocks_around.append(tile)


            for i in blocks_around:
                if self.rect.colliderect(blocks[i].rect):
                    if self.speed[0] > 0: 
                        self.rect.right = blocks[i].rect.left
                        self.speed[0] -= 4 * PhYSICS_MOD
                        if self.speed[0] < 0: self.speed[0] = 0 #in case of direction shift by collision
                        break

                    elif self.speed[0] < 0:
                        self.rect.left = blocks[i].rect.right
                        self.speed[0] += 4 * PhYSICS_MOD
                        if self.speed[0] > 0: self.speed[0] = 0#in case of direction shift by collision
                        break
            else:
                continue
            break

        # gravity,
        if self.speed[1] * self.gravity < 10: #grav is 1/-1
            self.speed[1] += 0.7 * self.gravity * PhYSICS_MOD
              
        repeats = ceil(abs(self.speed[1]) / 10) + 1
        stepy = self.speed[1]/ repeats

        ground_touch = False

        for i in range(repeats):

            self.rect.centery += stepy
            ground_check_rect = pygame.Rect(self.rect.x,
                                            self.rect.top - 9 + (22 * (self.gravity + 1) / 2),
                                            9, 12) # Makes player grounded earlier

            player_pos = [self.rect.centerx // 10, self.rect.centery // 10]

            blocks_around = []

            for offset in OFFSETS:
                tile = (player_pos[0] + offset[0], player_pos[1] + offset[1])
                if tile in blocks:
                    blocks_around.append(tile)

            for i in blocks_around:
                if ground_check_rect.colliderect(blocks[i].rect):
                    if (self.speed[1] > 0 and self.gravity == 1) or (self.speed[1] < 0 and self.gravity == -1):
                        ground_touch = True

                if self.rect.colliderect(blocks[i].rect):
                    if self.speed[1] > 0:
                        self.rect.bottom = blocks[i].rect.top
                        self.speed[1] = 0
                        break
                    elif self.speed[1] < 0:
                        self.rect.top = blocks[i].rect.bottom
                        self.speed[1] = 0
                        break
            else:
                continue
            break

        if ground_touch:
            self.state = PlayerState.GROUNDED
            self.flips = 1
            self.jumps = 2
        else: self.state = PlayerState.AIR

    def friction(self):
        #higher if not pressing a/d, (could remove)
        if self.keys_pressed["a/d"] == True:
            mult = 1
        else: mult = 10

        #higher if grounded
        if self.state == PlayerState.GROUNDED: num = abs(self.speed[0]) /  20 * mult #makes friction 1/50 * mul from speed
        else: num = abs(self.speed[0]) / 25 * mult

        #check if speed is positive
        try:polarity = (self.speed[0] / abs(self.speed[0]))
        except ZeroDivisionError: polarity = False

        #apply speed based on all of the above
        if abs(self.speed[0]) - num < 0: self.speed[0] = 0
        else: self.speed[0] -= num * polarity


    def update_camera(self, camera):

        delta = [camera[0] - (self.rect.centerx -320), camera[1] - (self.rect.centery - 180)]
        camera[0] -= delta[0] / 10
        camera[1] -= delta[1] / 10

        return camera

    def collison(self, tiles): #with non-blocks
        player_pos = [self.rect.centerx // 10 , self.rect.centery // 10]

        tiles_around = []

        for offset in OFFSETS:
            tile = (player_pos[0] + offset[0], player_pos[1] + offset[1])
            if tile in tiles:
                if tiles[tile].type != "block":
                    tiles_around.append(tile)

        for tile in tiles_around:
            event = tiles[tile].collision_logic(self.rect)
            match event:
                case Events.DEATH:
                    print(f"hit by {tile}")
                    self.rect.center = (20, 20)

    def draw(self, camera, scale):
        drawn_rect = pygame.Rect((self.rect.left - camera[0]) * scale, (self.rect.top - camera[1])* scale, self.rect.width* scale, self.rect.height* scale)
        
        colors = [(255, 0), (255, 128), (255, 255)]
        # FF8000 128

        color = colors[self.jumps]
        # if self.jumps < 2
        #     color = "blue"
        color += ((0, 255)[self.flips],)
        pygame.draw.rect(self.screen, color, drawn_rect)


    def update(self, tiles, blocks):
        self.input()
        self.apply_mov(blocks)
        self.friction()
        self.collison(tiles)